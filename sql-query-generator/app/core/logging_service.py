import logging
import logging.handlers
import os
from datetime import datetime
from app.schemas.models import AuditLogEntry
import psycopg2
from typing import Optional

# Create logs directory if it doesn't exist
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def setup_logging(log_level: str = 'INFO', log_file: str = None):
    """Configure logging for the application"""
    
    if log_file is None:
        log_file = os.path.join(LOG_DIR, 'sql_generator.log')
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10_485_760,  # 10MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


class AuditLogger:
    """Log query execution for auditing purposes"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.logger = logging.getLogger(__name__)
    
    def log_query(self, audit_entry: AuditLogEntry) -> bool:
        """Log a query execution to both file and database"""
        
        try:
            # Log to file/console
            log_message = (
                f"USER: {audit_entry.user_email or 'unknown'} | "
                f"STATUS: {audit_entry.execution_status} | "
                f"ROWS: {audit_entry.rows_returned or 0} | "
                f"TIME: {audit_entry.execution_time_ms}ms"
            )
            
            if audit_entry.execution_status == 'success':
                self.logger.info(log_message)
            else:
                self.logger.warning(f"{log_message} | ERROR: {audit_entry.error_message}")
            
            # Also log the generated SQL (for debugging)
            self.logger.debug(f"QUESTION: {audit_entry.question}")
            self.logger.debug(f"SQL: {audit_entry.generated_sql}")
            
            # Log to database
            self._log_to_database(audit_entry)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error logging query: {e}")
            return False
    
    def _log_to_database(self, audit_entry: AuditLogEntry) -> bool:
        """Save audit log to database"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connect_timeout=5
            )
            cursor = conn.cursor()
            
            query = """
                INSERT INTO audit_logs 
                (user_email, question, generated_sql, execution_status, 
                 error_message, rows_returned, execution_time_ms, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                audit_entry.user_email,
                audit_entry.question,
                audit_entry.generated_sql,
                audit_entry.execution_status,
                audit_entry.error_message,
                audit_entry.rows_returned,
                audit_entry.execution_time_ms,
                audit_entry.created_at
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving to audit logs: {e}")
            return False
    
    def get_logs(self, user_email: Optional[str] = None, limit: int = 100, 
                 offset: int = 0) -> list:
        """Retrieve audit logs"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connect_timeout=5
            )
            cursor = conn.cursor()
            
            if user_email:
                query = """
                    SELECT id, user_email, question, generated_sql, execution_status,
                           error_message, rows_returned, execution_time_ms, created_at
                    FROM audit_logs
                    WHERE user_email = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (user_email, limit, offset))
            else:
                query = """
                    SELECT id, user_email, question, generated_sql, execution_status,
                           error_message, rows_returned, execution_time_ms, created_at
                    FROM audit_logs
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limit, offset))
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            logs = [dict(zip(columns, row)) for row in rows]
            
            cursor.close()
            conn.close()
            
            return logs
        
        except Exception as e:
            self.logger.error(f"Error retrieving logs: {e}")
            return []
    
    def get_log_stats(self, hours: int = 24) -> dict:
        """Get statistics on recent queries"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connect_timeout=5
            )
            cursor = conn.cursor()
            
            # Get stats for last N hours
            query = f"""
                SELECT 
                    COUNT(*) as total_queries,
                    SUM(CASE WHEN execution_status = 'success' THEN 1 ELSE 0 END) as successful_queries,
                    SUM(CASE WHEN execution_status = 'error' THEN 1 ELSE 0 END) as failed_queries,
                    AVG(execution_time_ms) as avg_execution_time,
                    MAX(execution_time_ms) as max_execution_time,
                    SUM(rows_returned) as total_rows_returned
                FROM audit_logs
                WHERE created_at >= NOW() - INTERVAL '{hours} hours'
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            
            stats = dict(zip(columns, row)) if row else {}
            
            cursor.close()
            conn.close()
            
            return stats
        
        except Exception as e:
            self.logger.error(f"Error getting log stats: {e}")
            return {}
