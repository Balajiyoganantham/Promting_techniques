"""
API routes for the research article summarizer application.
Handles all HTTP endpoints for the summarization service.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import os

from prompts import PROMPTING_METHODS
from summarizer import ResearchSummarizer

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/prompting-methods', methods=['GET'])
def get_prompting_methods():
    """Get available prompting methods"""
    return jsonify(PROMPTING_METHODS)


@api_bp.route('/summarize', methods=['POST'])
def summarize():
    """Summarize research article using selected prompting method"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        article = data.get('article', '').strip()
        prompting_method = data.get('prompting_method', 'zero_shot')
        
        if not article:
            return jsonify({'error': 'Article content is required'}), 400
        
        # Check if API key is configured
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({
                'error': 'Groq API key not configured. Please set GROQ_API_KEY environment variable.'
            }), 400
        
        if prompting_method not in PROMPTING_METHODS:
            return jsonify({
                'error': f'Invalid prompting method. Available methods: {list(PROMPTING_METHODS.keys())}'
            }), 400
        
        # Create summarizer instance with environment API key
        summarizer = ResearchSummarizer(api_key=groq_api_key)
        
        # Generate summary
        result = summarizer.summarize_article(article, prompting_method)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/validate', methods=['POST'])
def validate_article():
    """Validate article length"""
    try:
        data = request.get_json()
        article = data.get('article', '')
        
        summarizer = ResearchSummarizer()
        is_valid, message = summarizer.validate_article(article)
        word_count = summarizer.count_words(article)
        
        return jsonify({
            'valid': is_valid,
            'message': message,
            'word_count': word_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model': 'llama-3.1-8b-instant',
        'available_methods': list(PROMPTING_METHODS.keys())
    }) 