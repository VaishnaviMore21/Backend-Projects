import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # PostgreSQL
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'business_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'sqlgen')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'SecurePassword123!')
    
    # Ollama
    OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/sql_generator.log')
    
    # Query execution
    QUERY_TIMEOUT_MS = int(os.getenv('QUERY_TIMEOUT_MS', 30000))
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 1000))
    
    # Rate limiting
    RATE_LIMIT_QUERIES_PER_MINUTE = int(os.getenv('RATE_LIMIT_QPM', 10))


def get_config():
    """Get application configuration"""
    return Config()
