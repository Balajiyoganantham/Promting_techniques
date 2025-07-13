"""
Main Flask application for the Advanced Research Article Summarizer.
Serves as the entry point and orchestrates the modular components.
"""

from flask import Flask, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

from routes.api_routes import api_bp

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register API routes blueprint
app.register_blueprint(api_bp)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)