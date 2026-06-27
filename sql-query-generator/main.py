#!/usr/bin/env python3
"""
SQL Query Generator - Main Entry Point
Convert natural language questions to SQL queries using LangChain and Ollama
"""

import os
import sys
import logging
from app import create_app
from app.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("SQL Query Generator - Initializing...")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        config = Config()
        logger.info(f"Environment: {config.FLASK_ENV}")
        logger.info(f"PostgreSQL: {config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")
        logger.info(f"Ollama API: {config.OLLAMA_API_URL}")
        logger.info(f"Model: {config.OLLAMA_MODEL}")
        
        # Create Flask app
        app = create_app(config)
        logger.info("Flask app created successfully")
        
        # Run app
        logger.info("Starting server on http://0.0.0.0:5000")
        logger.info("Open browser to http://localhost:5000")
        logger.info("=" * 60)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=config.DEBUG,
            use_reloader=False
        )
    
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
