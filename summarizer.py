"""
Core summarization logic using GROQ API.
Handles API calls and response processing for research article summarization.
"""

import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional

from prompts import PromptGenerator


class ResearchSummarizer:
    """Main class for research article summarization using GROQ API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the summarizer with API configuration."""
        self.api_key = api_key or os.getenv('GROQ_API_KEY', '')
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.default_model = "llama-3.1-8b-instant"
        
    def call_groq_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to Groq using single model"""
        if not self.api_key:
            raise ValueError("Groq API key not configured")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.default_model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 250,
            'temperature': 0.3,
            'top_p': 0.9
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def summarize_article(self, article: str, prompting_method: str = 'zero_shot') -> Dict[str, Any]:
        """Main method to summarize research article using selected prompting method"""
        # Validate article
        is_valid, message = PromptGenerator.validate_article(article)
        if not is_valid:
            raise ValueError(message)
        
        # Create prompt based on method
        prompt = PromptGenerator.create_prompt_by_method(article, prompting_method)
        
        # Call API
        response = self.call_groq_api(prompt)
        
        # Extract summary
        if 'choices' in response and len(response['choices']) > 0:
            summary = response['choices'][0]['message']['content'].strip()
            
            # Validate summary length
            summary_word_count = PromptGenerator.count_words(summary)
            
            return {
                'summary': summary,
                'word_count': summary_word_count,
                'prompting_method': prompting_method,
                'model_used': self.default_model,
                'article_word_count': PromptGenerator.count_words(article),
                'timestamp': datetime.now().isoformat()
            }
        else:
            raise Exception("No summary generated from API response")
    
    def validate_article(self, article: str) -> tuple[bool, str]:
        """Validate article length and content"""
        return PromptGenerator.validate_article(article)
    
    def count_words(self, text: str) -> int:
        """Count words in text"""
        return PromptGenerator.count_words(text) 