from typing import Dict, Any
from datetime import datetime
import json


def serialize_result(obj: Any) -> Any:
    """Serialize objects for JSON response"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_result(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_result(item) for item in obj]
    return obj


def format_execution_result(success: bool, data: Any = None, 
                           error: str = None, **kwargs) -> Dict:
    """Format execution result for API response"""
    return {
        'success': success,
        'data': data,
        'error': error,
        **kwargs
    }


def paginate_results(results: list, page: int, page_size: int) -> Dict:
    """Calculate pagination information"""
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        'items': results[start:end],
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'has_next': end < total,
        'has_prev': page > 1
    }


def build_schema_string(schema_dict: Dict) -> str:
    """Build a human-readable schema string for prompts"""
    schema_lines = []
    
    for table_name, table_info in schema_dict.items():
        schema_lines.append(f"\n{table_name}:")
        
        for col_name, col_info in table_info['columns'].items():
            col_type = col_info['type']
            nullable = 'NULL' if col_info['nullable'] else 'NOT NULL'
            pk = ' (PK)' if col_info.get('primary_key') else ''
            
            schema_lines.append(f"  {col_name}: {col_type} {nullable}{pk}")
    
    return '\n'.join(schema_lines)
