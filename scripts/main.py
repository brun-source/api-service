import os
from flask import Flask, jsonify
from api_service.config import Config
from api_service.extensions import db, migrate
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from api_service.views import main
    app.register_blueprint(main)
    
    # Register error handlers
    from api_service.errors import error
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(500, error.internal_server_error)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))