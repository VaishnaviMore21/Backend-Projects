import logging
import requests
import json
from typing import Optional, Tuple
from app.core.security import validate_sql_syntax

logger = logging.getLogger(__name__)


class QueryGenerator:
    """Generate SQL queries from natural language using Ollama"""
    
    def __init__(self, ollama_url: str, model: str, schema_dict: dict):
        self.ollama_url = ollama_url.rstrip('/')
        self.model = model
        self.schema_dict = schema_dict
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with database schema"""
        schema_text = self._format_schema_for_prompt()
        
        return f"""You are an expert SQL query generator for a PostgreSQL database.

DATABASE SCHEMA:
{schema_text}

INSTRUCTIONS:
1. Generate ONLY valid PostgreSQL SQL queries
2. Return ONLY the SQL query, no explanation or markdown
3. Use appropriate JOINs when needed
4. Include WHERE, ORDER BY, LIMIT clauses as needed
5. Always use table aliases for clarity
6. Handle date/time operations correctly
7. Use proper aggregation functions (SUM, COUNT, AVG, etc.)
8. Do NOT use INSERT, UPDATE, DELETE, or DROP statements
9. Do NOT use any table or column that is not in the schema above
10. For pagination, include LIMIT and OFFSET clauses
11. Ensure queries are optimized and readable

When generating queries:
- Be precise with data types
- Use the exact column and table names provided
- Include necessary JOINs based on foreign key relationships
- Return meaningful results that answer the question"""
    
    def _format_schema_for_prompt(self) -> str:
        """Format schema dictionary into readable prompt text"""
        schema_text = ""
        
        for table_name, table_info in self.schema_dict.items():
            schema_text += f"\nTable: {table_name}\n"
            schema_text += "Columns:\n"
            
            for col_name, col_info in table_info['columns'].items():
                col_type = col_info['type']
                nullable = 'NULL' if col_info['nullable'] else 'NOT NULL'
                pk = ' [PRIMARY KEY]' if col_info.get('primary_key') else ''
                row_count = table_info.get('row_count', 'N/A')
                
                schema_text += f"  - {col_name}: {col_type} ({nullable}){pk}\n"
            
            schema_text += f"  - Row count: {table_info.get('row_count', 'N/A')}\n"
        
        return schema_text
    
    def generate_query(self, question: str, max_retries: int = 2) -> Tuple[str, float]:
        """
        Generate SQL query from natural language question
        
        Args:
            question: Natural language question
            max_retries: Number of retries if generation fails
        
        Returns:
            Tuple of (sql_query, confidence_score)
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{self.system_prompt}\n\nUser Question: {question}",
                    "stream": False,
                    "temperature": 0.1,  # Low temperature for deterministic SQL
                    "top_k": 40,
                    "top_p": 0.9,
                },
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code}")
                raise Exception(f"Ollama API failed: {response.status_code}")
            
            result = response.json()
            generated_text = result.get('response', '').strip()
            
            # Extract SQL from response (might have extra text)
            sql_query = self._extract_sql_from_response(generated_text)
            
            # Validate SQL
            is_valid, error_msg = validate_sql_syntax(sql_query)
            
            if not is_valid and max_retries > 0:
                logger.warning(f"Invalid SQL generated, retrying. Error: {error_msg}")
                # Append error feedback to the question and retry
                feedback_question = f"{question}\n[Previous attempt failed with error: {error_msg}. Please fix and try again.]"
                return self.generate_query(feedback_question, max_retries - 1)
            
            # Calculate confidence score based on various factors
            confidence = self._calculate_confidence(sql_query, is_valid)
            
            logger.info(f"Generated SQL: {sql_query}")
            return sql_query, confidence
        
        except Exception as e:
            logger.error(f"Error generating query: {e}")
            raise
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from LLM response"""
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith('```sql'):
            response = response[6:]
        elif response.startswith('```'):
            response = response[3:]
        
        if response.endswith('```'):
            response = response[:-3]
        
        return response.strip()
    
    def _calculate_confidence(self, sql_query: str, is_valid: bool) -> float:
        """Calculate confidence score for generated query"""
        confidence = 0.5
        
        if is_valid:
            confidence += 0.3
        
        # Check for common indicators of good queries
        if 'SELECT' in sql_query.upper():
            confidence += 0.1
        
        if 'FROM' in sql_query.upper():
            confidence += 0.05
        
        if 'WHERE' in sql_query.upper() or 'JOIN' in sql_query.upper():
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def explain_query(self, sql_query: str) -> str:
        """Generate plain English explanation of SQL query"""
        try:
            prompt = f"""Explain this SQL query in simple terms for a non-technical user:

SQL Query:
{sql_query}

Provide a brief explanation of what this query does."""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Unable to explain query').strip()
            
            return "Unable to generate explanation"
        
        except Exception as e:
            logger.error(f"Error explaining query: {e}")
            return "Unable to generate explanation"
