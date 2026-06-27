from flask import Flask, render_template
from flask_cors import CORS
import logging
import os

from app.config import Config
from app.core.logging_service import setup_logging
from app.routes import api_bp, init_services


def create_app(config: Config = None):
    """Create and configure the Flask application"""
    
    if config is None:
        config = Config()
    
    # Setup logging
    setup_logging(log_level=config.LOG_LEVEL, log_file=config.LOG_FILE)
    logger = logging.getLogger(__name__)
    
    # Create app
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    # Configure app
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize services
    try:
        init_services(config)
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/results')
    def results():
        return render_template('results.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return {'error': 'Internal server error'}, 500
    
    return app


if __name__ == '__main__':
    config = Config()
    app = create_app(config)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG
    )
