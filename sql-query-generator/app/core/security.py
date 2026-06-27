import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Tables and columns that should NEVER be exposed
RESTRICTED_TABLES = {
    'pg_catalog',
    'information_schema',
    'pg_stat_statements',
    'audit_logs'  # Don't let LLM query logs directly
}

# Dangerous SQL keywords to block
DANGEROUS_KEYWORDS = [
    'DROP',
    'DELETE',
    'INSERT',
    'UPDATE',
    'ALTER',
    'CREATE',
    'TRUNCATE',
    'GRANT',
    'REVOKE',
    'EXEC',
    'EXECUTE',
]

# Tables and columns that can be exposed to the LLM
EXPOSED_TABLES = {
    'users': ['id', 'email', 'first_name', 'last_name', 'phone', 'status', 'created_at', 'last_login'],
    'products': ['id', 'sku', 'name', 'description', 'category', 'price', 'stock_quantity', 'status', 'created_at'],
    'orders': ['id', 'user_id', 'order_number', 'status', 'total_amount', 'tax_amount', 'shipping_cost', 'discount_amount', 'created_at', 'shipped_at', 'delivered_at'],
    'order_items': ['id', 'order_id', 'product_id', 'quantity', 'unit_price', 'discount_percent', 'line_total'],
    'payments': ['id', 'order_id', 'payment_method', 'amount', 'status', 'transaction_id', 'created_at', 'processed_at'],
    'reviews': ['id', 'product_id', 'user_id', 'rating', 'title', 'comment', 'helpful_count', 'created_at'],
    'categories': ['id', 'name', 'description'],
}

# Business rules and constraints
BUSINESS_RULES = {
    'min_order_value': 0,
    'max_query_rows': 10000,
    'allowed_aggregations': ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'STRING_AGG', 'ARRAY_AGG'],
    'tax_rate': 0.08,
}


def validate_sql_syntax(sql_query: str) -> Tuple[bool, str]:
    """
    Validate SQL query for dangerous operations and syntax issues
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    
    # Check for dangerous keywords
    sql_upper = sql_query.upper()
    
    for keyword in DANGEROUS_KEYWORDS:
        if re.search(rf'\b{keyword}\b', sql_upper):
            return False, f"Operation '{keyword}' is not allowed for security reasons"
    
    # Check for table access restrictions
    for restricted_table in RESTRICTED_TABLES:
        if re.search(rf'\b{restricted_table}\b', sql_upper):
            return False, f"Access to table '{restricted_table}' is restricted"
    
    # Check for SQL injection patterns (basic heuristic)
    if re.search(r'(;[\s]*(?:DROP|DELETE|INSERT|UPDATE|ALTER)|--|/\*)', sql_query, re.IGNORECASE):
        return False, "Potential SQL injection detected"
    
    # Check for -- or /* */ comments with dangerous content
    if re.search(r'--\s*(DROP|DELETE|INSERT|UPDATE)', sql_query, re.IGNORECASE):
        return False, "Dangerous operation in comment"
    
    # Must start with SELECT
    if not re.match(r'^\s*SELECT\b', sql_upper):
        return False, "Only SELECT queries are allowed"
    
    # Check for common syntax errors
    if sql_query.count('(') != sql_query.count(')'):
        return False, "Mismatched parentheses"
    
    if sql_query.count("'") % 2 != 0:
        return False, "Unclosed string literal"
    
    # Check LIMIT is reasonable
    limit_match = re.search(r'\bLIMIT\s+(\d+)', sql_query, re.IGNORECASE)
    if limit_match:
        limit_value = int(limit_match.group(1))
        if limit_value > BUSINESS_RULES['max_query_rows']:
            return False, f"LIMIT exceeds maximum of {BUSINESS_RULES['max_query_rows']} rows"
    
    return True, ""


def is_table_exposed(table_name: str) -> bool:
    """Check if table is allowed to be accessed"""
    return table_name.lower() in EXPOSED_TABLES


def filter_schema_for_llm(full_schema: dict) -> dict:
    """Filter schema to only expose safe tables and columns"""
    filtered_schema = {}
    
    for table_name, table_info in full_schema.items():
        if not is_table_exposed(table_name):
            continue
        
        # Filter columns
        allowed_columns = EXPOSED_TABLES.get(table_name.lower(), [])
        
        filtered_columns = {}
        for col_name, col_info in table_info['columns'].items():
            if col_name in allowed_columns:
                filtered_columns[col_name] = col_info
        
        if filtered_columns:
            filtered_schema[table_name] = {
                'columns': filtered_columns,
                'row_count': table_info.get('row_count')
            }
    
    return filtered_schema


def sanitize_query_output(results: list) -> list:
    """Sanitize query results before returning to user"""
    if not results:
        return results
    
    # Convert timestamps and other special types to strings
    sanitized = []
    for row in results:
        sanitized_row = {}
        for key, value in row.items():
            if value is None:
                sanitized_row[key] = None
            elif isinstance(value, (int, float, str, bool)):
                sanitized_row[key] = value
            else:
                # Convert other types (datetime, UUID, etc.) to string
                sanitized_row[key] = str(value)
        
        sanitized.append(sanitized_row)
    
    return sanitized


def rate_limit_check(user_email: str, queries_per_minute: int = 10) -> bool:
    """
    Rate limiting check per user (basic implementation)
    In production, use Redis or similar
    """
    # TODO: Implement proper rate limiting with redis
    return True


def mask_sensitive_data(results: list, sensitive_fields: list = None) -> list:
    """Mask sensitive fields in results"""
    if sensitive_fields is None:
        sensitive_fields = ['password', 'credit_card', 'ssn', 'api_key']
    
    masked_results = []
    for row in results:
        masked_row = {}
        for key, value in row.items():
            if any(field in key.lower() for field in sensitive_fields):
                masked_row[key] = "***MASKED***"
            else:
                masked_row[key] = value
        
        masked_results.append(masked_row)
    
    return masked_results
