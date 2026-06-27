import logging
import time
from typing import List, Dict, Any, Tuple, Optional
import psycopg2
from psycopg2 import sql

logger = logging.getLogger(__name__)


class QueryExecutor:
    """Execute SQL queries securely against PostgreSQL"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str, 
                 readonly_user: str = None, readonly_password: str = None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        # Use readonly user if provided, otherwise use main user
        self.exec_user = readonly_user or user
        self.exec_password = readonly_password or password
        self.query_timeout = 30000  # 30 seconds in milliseconds
    
    def get_connection(self, readonly: bool = True):
        """Create a database connection"""
        try:
            exec_user = self.exec_user if readonly else self.user
            exec_password = self.exec_password if readonly else self.password
            
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=exec_user,
                password=exec_password,
                connect_timeout=10
            )
            
            # Set query timeout
            conn.set_session(options=f"-c statement_timeout={self.query_timeout}")
            
            return conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def execute_query(self, sql_query: str, page: int = 1, 
                     page_size: int = 20) -> Tuple[bool, Optional[List[Dict]], Optional[int], int, Optional[str]]:
        """
        Execute a SQL query with pagination
        
        Returns:
            Tuple of (success, results, total_rows, execution_time_ms, error_message)
        """
        try:
            start_time = time.time()
            conn = self.get_connection(readonly=True)
            cursor = conn.cursor()
            
            # Get total row count first (without LIMIT)
            count_query = self._build_count_query(sql_query)
            total_rows = None
            
            try:
                cursor.execute(count_query)
                total_rows = cursor.fetchone()[0]
            except Exception as e:
                logger.warning(f"Could not get total row count: {e}")
                total_rows = None
            
            # Add pagination to query
            paginated_query = self._add_pagination(sql_query, page, page_size)
            
            # Execute the query
            cursor.execute(paginated_query)
            
            # Fetch results
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = [dict(zip(columns, row)) for row in rows]
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            cursor.close()
            conn.close()
            
            logger.info(f"Query executed successfully in {execution_time_ms}ms, returned {len(results)} rows")
            
            return True, results, total_rows, execution_time_ms, None
        
        except psycopg2.errors.QueryCanceled as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Query timeout after {self.query_timeout}ms"
            logger.error(error_msg)
            return False, None, None, execution_time_ms, error_msg
        
        except psycopg2.Error as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Database error: {str(e)}"
            logger.error(error_msg)
            return False, None, None, execution_time_ms, error_msg
        
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, None, None, execution_time_ms, error_msg
    
    def _build_count_query(self, sql_query: str) -> str:
        """Build a COUNT query to get total rows"""
        try:
            # Remove LIMIT and OFFSET clauses
            sql_upper = sql_query.upper()
            
            # Simple heuristic: wrap original query
            if sql_upper.startswith('SELECT'):
                # Remove ORDER BY (not needed for count)
                count_query = f"SELECT COUNT(*) FROM ({sql_query.rstrip(';')}) as t"
                return count_query
            
            return sql_query
        except Exception as e:
            logger.warning(f"Could not build count query: {e}")
            return sql_query
    
    def _add_pagination(self, sql_query: str, page: int, page_size: int) -> str:
        """Add LIMIT and OFFSET to query for pagination"""
        try:
            # Remove trailing semicolon if present
            sql_query = sql_query.rstrip(';')
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Add LIMIT and OFFSET
            paginated_query = f"{sql_query} LIMIT {page_size} OFFSET {offset};"
            
            return paginated_query
        except Exception as e:
            logger.warning(f"Error adding pagination: {e}")
            return sql_query
    
    def execute_count_query(self, sql_query: str) -> int:
        """Execute a query and return only the count"""
        try:
            conn = self.get_connection(readonly=True)
            cursor = conn.cursor()
            
            count_query = f"SELECT COUNT(*) FROM ({sql_query.rstrip(';')}) as t"
            cursor.execute(count_query)
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count
        
        except Exception as e:
            logger.error(f"Error executing count query: {e}")
            return 0
    
    def preview_query(self, sql_query: str, limit: int = 5) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
        """Get a preview of query results (first few rows only)"""
        try:
            conn = self.get_connection(readonly=True)
            cursor = conn.cursor()
            
            # Add LIMIT to query
            preview_query = f"{sql_query.rstrip(';')} LIMIT {limit};"
            cursor.execute(preview_query)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            results = [dict(zip(columns, row)) for row in rows]
            
            cursor.close()
            conn.close()
            
            return True, results, None
        
        except Exception as e:
            logger.error(f"Error previewing query: {e}")
            return False, None, str(e)
