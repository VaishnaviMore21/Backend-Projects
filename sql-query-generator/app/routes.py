from flask import Blueprint, request, jsonify, render_template
from flask_cors import cross_origin
import logging
from typing import Optional

from app.core.schema_extractor import SchemaExtractor
from app.core.query_generator import QueryGenerator
from app.core.query_executor import QueryExecutor
from app.core.security import validate_sql_syntax, filter_schema_for_llm, sanitize_query_output
from app.core.logging_service import AuditLogger
from app.schemas.models import QueryRequest, AuditLogEntry
from app.config import Config
from app.utils import serialize_result

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize services (will be set in main.py)
schema_extractor: Optional[SchemaExtractor] = None
query_generator: Optional[QueryGenerator] = None
query_executor: Optional[QueryExecutor] = None
audit_logger: Optional[AuditLogger] = None


def init_services(config: Config):
    """Initialize all services"""
    global schema_extractor, query_generator, query_executor, audit_logger
    
    # Initialize schema extractor
    schema_extractor = SchemaExtractor(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )
    
    # Get schema and filter for LLM
    full_schema = schema_extractor.get_schema_dict()
    filtered_schema = filter_schema_for_llm(full_schema)
    
    # Initialize query generator
    query_generator = QueryGenerator(
        ollama_url=config.OLLAMA_API_URL,
        model=config.OLLAMA_MODEL,
        schema_dict=filtered_schema
    )
    
    # Initialize query executor
    query_executor = QueryExecutor(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )
    
    # Initialize audit logger
    audit_logger = AuditLogger(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )


@api_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SQL Query Generator is running'
    })


@api_bp.route('/schema', methods=['GET'])
@cross_origin()
def get_schema():
    """Get database schema"""
    try:
        if not schema_extractor:
            return jsonify({'error': 'Services not initialized'}), 500
        
        full_schema = schema_extractor.get_schema_dict()
        relationships = schema_extractor.get_relationships()
        
        return jsonify({
            'tables': serialize_result(full_schema),
            'relationships': serialize_result(relationships)
        })
    
    except Exception as e:
        logger.error(f"Error retrieving schema: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/query/generate', methods=['POST'])
@cross_origin()
def generate_query():
    """Generate SQL query from natural language (without execution)"""
    try:
        data = request.get_json()
        question = data.get('question')
        explain = data.get('explain', False)
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if not query_generator:
            return jsonify({'error': 'Services not initialized'}), 500
        
        # Generate query
        sql_query, confidence = query_generator.generate_query(question)
        
        # Validate query
        is_valid, error_msg = validate_sql_syntax(sql_query)
        
        if not is_valid:
            return jsonify({
                'error': 'Generated query failed validation',
                'message': error_msg,
                'query': sql_query
            }), 400
        
        # Generate explanation if requested
        explanation = None
        if explain:
            explanation = query_generator.explain_query(sql_query)
        
        return jsonify({
            'query': sql_query,
            'confidence': confidence,
            'explanation': explanation,
            'is_valid': True
        })
    
    except Exception as e:
        logger.error(f"Error generating query: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/query/execute', methods=['POST'])
@cross_origin()
def execute_query():
    """Generate and execute SQL query"""
    try:
        data = request.get_json()
        
        try:
            query_request = QueryRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Invalid request: {str(e)}'}), 400
        
        if not all([query_generator, query_executor, audit_logger]):
            return jsonify({'error': 'Services not initialized'}), 500
        
        user_email = request.headers.get('X-User-Email', 'anonymous')
        
        # Generate query
        sql_query, confidence = query_generator.generate_query(query_request.question)
        
        # Validate query
        is_valid, error_msg = validate_sql_syntax(sql_query)
        
        if not is_valid:
            # Log failed validation
            audit_entry = AuditLogEntry(
                user_email=user_email,
                question=query_request.question,
                generated_sql=sql_query,
                execution_status='validation_failed',
                error_message=error_msg
            )
            audit_logger.log_query(audit_entry)
            
            return jsonify({
                'error': 'Generated query failed security validation',
                'message': error_msg
            }), 400
        
        # Execute query
        success, results, total_rows, execution_time_ms, exec_error = query_executor.execute_query(
            sql_query,
            page=query_request.page,
            page_size=query_request.page_size
        )
        
        # Log execution
        audit_entry = AuditLogEntry(
            user_email=user_email,
            question=query_request.question,
            generated_sql=sql_query,
            execution_status='success' if success else 'error',
            error_message=exec_error,
            rows_returned=len(results) if results else 0,
            execution_time_ms=execution_time_ms
        )
        audit_logger.log_query(audit_entry)
        
        if not success:
            return jsonify({
                'error': exec_error,
                'execution_time_ms': execution_time_ms
            }), 400
        
        # Sanitize results
        sanitized_results = sanitize_query_output(results) if results else []
        
        return jsonify({
            'results': serialize_result(sanitized_results),
            'total_rows': total_rows,
            'page': query_request.page,
            'page_size': query_request.page_size,
            'execution_time_ms': execution_time_ms,
            'query': sql_query,
            'confidence': confidence
        })
    
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/query/preview', methods=['POST'])
@cross_origin()
def preview_query():
    """Preview generated query without full execution"""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if not all([query_generator, query_executor]):
            return jsonify({'error': 'Services not initialized'}), 500
        
        # Generate query
        sql_query, confidence = query_generator.generate_query(question)
        
        # Validate query
        is_valid, error_msg = validate_sql_syntax(sql_query)
        
        if not is_valid:
            return jsonify({
                'error': 'Generated query failed validation',
                'message': error_msg
            }), 400
        
        # Get preview (first 5 rows)
        success, preview_results, preview_error = query_executor.preview_query(sql_query, limit=5)
        
        if not success:
            return jsonify({
                'error': preview_error,
                'query': sql_query
            }), 400
        
        sanitized = sanitize_query_output(preview_results) if preview_results else []
        
        return jsonify({
            'query': sql_query,
            'preview': serialize_result(sanitized),
            'confidence': confidence,
            'row_count': len(sanitized)
        })
    
    except Exception as e:
        logger.error(f"Error previewing query: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/logs', methods=['GET'])
@cross_origin()
def get_logs():
    """Get audit logs"""
    try:
        if not audit_logger:
            return jsonify({'error': 'Services not initialized'}), 500
        
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        user_email = request.args.get('user_email')
        
        limit = page_size
        offset = (page - 1) * page_size
        
        logs = audit_logger.get_logs(user_email=user_email, limit=limit, offset=offset)
        
        return jsonify({
            'logs': serialize_result(logs),
            'page': page,
            'page_size': page_size,
            'total': len(logs)
        })
    
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/logs/stats', methods=['GET'])
@cross_origin()
def get_log_stats():
    """Get audit log statistics"""
    try:
        if not audit_logger:
            return jsonify({'error': 'Services not initialized'}), 500
        
        hours = request.args.get('hours', 24, type=int)
        stats = audit_logger.get_log_stats(hours=hours)
        
        return jsonify({
            'stats': serialize_result(stats),
            'period_hours': hours
        })
    
    except Exception as e:
        logger.error(f"Error retrieving stats: {e}")
        return jsonify({'error': str(e)}), 500
