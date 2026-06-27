import os
import logging
from typing import Dict, List, Optional
import psycopg2
from psycopg2 import sql
from app.schemas.models import TableInfo, ColumnInfo, DatabaseSchema, ColumnInfo as ColumnSchema

logger = logging.getLogger(__name__)


class SchemaExtractor:
    """Extract database schema from PostgreSQL"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    def get_connection(self):
        """Create a database connection"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def extract_schema(self, exposed_tables: Optional[List[str]] = None) -> DatabaseSchema:
        """Extract schema for all tables or specific tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get list of tables
            query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """
            
            if exposed_tables:
                placeholders = ','.join(['%s'] * len(exposed_tables))
                query += f" AND table_name IN ({placeholders})"
                cursor.execute(query, exposed_tables)
            else:
                cursor.execute(query)
            
            tables_data = cursor.fetchall()
            tables = []
            
            for (table_name,) in tables_data:
                table_schema = self._extract_table_schema(cursor, table_name)
                tables.append(table_schema)
            
            cursor.close()
            conn.close()
            
            return DatabaseSchema(tables=tables)
        
        except Exception as e:
            logger.error(f"Error extracting schema: {e}")
            raise
    
    def _extract_table_schema(self, cursor, table_name: str) -> TableInfo:
        """Extract schema for a single table"""
        # Get column information
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        cursor.execute(query, (table_name,))
        columns_data = cursor.fetchall()
        
        columns = []
        for col_name, col_type, is_nullable, col_default in columns_data:
            # Check if column is primary key
            is_pk = self._is_primary_key(cursor, table_name, col_name)
            
            columns.append(ColumnSchema(
                name=col_name,
                type=col_type,
                nullable=is_nullable == 'YES',
                is_primary_key=is_pk
            ))
        
        # Get row count
        row_count_query = f"SELECT COUNT(*) FROM {sql.Identifier(table_name).as_string(cursor)}"
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        return TableInfo(
            name=table_name,
            columns=columns,
            row_count=row_count
        )
    
    def _is_primary_key(self, cursor, table_name: str, column_name: str) -> bool:
        """Check if column is a primary key"""
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = %s
                AND kcu.column_name = %s
                AND tc.constraint_type = 'PRIMARY KEY'
            )
        """
        cursor.execute(query, (table_name, column_name))
        return cursor.fetchone()[0]
    
    def get_schema_dict(self, exposed_tables: Optional[List[str]] = None) -> Dict:
        """Get schema as a dictionary suitable for LLM context"""
        schema = self.extract_schema(exposed_tables)
        
        schema_dict = {}
        for table in schema.tables:
            schema_dict[table.name] = {
                'columns': {
                    col.name: {
                        'type': col.type,
                        'nullable': col.nullable,
                        'primary_key': col.is_primary_key
                    }
                    for col in table.columns
                },
                'row_count': table.row_count
            }
        
        return schema_dict
    
    def get_relationships(self) -> Dict[str, List[Dict]]:
        """Extract foreign key relationships"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                ORDER BY tc.table_name, kcu.column_name
            """
            
            cursor.execute(query)
            relationships_data = cursor.fetchall()
            
            relationships = {}
            for table, column, foreign_table, foreign_column in relationships_data:
                if table not in relationships:
                    relationships[table] = []
                
                relationships[table].append({
                    'column': column,
                    'references': foreign_table,
                    'foreign_key': foreign_column
                })
            
            cursor.close()
            conn.close()
            
            return relationships
        
        except Exception as e:
            logger.error(f"Error extracting relationships: {e}")
            return {}
