from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ColumnInfo(BaseModel):
    """Schema information for a database column"""
    name: str
    type: str
    nullable: bool
    is_primary_key: bool = False
    
    
class TableInfo(BaseModel):
    """Schema information for a database table"""
    name: str
    columns: List[ColumnInfo]
    row_count: Optional[int] = None


class DatabaseSchema(BaseModel):
    """Complete database schema"""
    tables: List[TableInfo]
    timestamp: datetime = Field(default_factory=datetime.now)


class QueryRequest(BaseModel):
    """Request to generate and/or execute a SQL query"""
    question: str = Field(..., description="Natural language question")
    explain_query: bool = False
    page: int = Field(1, ge=1, description="Page number for pagination")
    page_size: int = Field(20, ge=1, le=1000, description="Rows per page")


class QueryResponse(BaseModel):
    """Response containing generated SQL and results"""
    question: str
    generated_sql: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    results: Optional[List[Dict[str, Any]]] = None
    total_rows: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None


class QueryGenerationRequest(BaseModel):
    """Request to only generate SQL without execution"""
    question: str
    explain: bool = False


class QueryGenerationResponse(BaseModel):
    """Response with generated SQL only"""
    query: str
    confidence: float
    explanation: Optional[str] = None


class AuditLogEntry(BaseModel):
    """Audit log entry for query execution"""
    user_email: Optional[str] = None
    question: str
    generated_sql: str
    execution_status: str  # 'success', 'error', 'validation_failed'
    error_message: Optional[str] = None
    rows_returned: Optional[int] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)


class ExecutionResult(BaseModel):
    """Result of SQL query execution"""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    total_rows: Optional[int] = None
    execution_time_ms: int
    error: Optional[str] = None
    query: Optional[str] = None
