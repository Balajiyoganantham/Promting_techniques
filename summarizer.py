"""
Core summarization logic using GROQ API.
Handles API calls and response processing for research article summarization.
"""
import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from prompts import PromptGenerator
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq  

class ResearchSummarizer:
    """Main class for research article summarization using GROQ API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the summarizer with API configuration."""
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.default_model = "llama-3.1-8b-instant"
        
    def call_groq_api(self, prompt: str, article: str) -> Dict[str, Any]:
        """Make API call to Groq using langchain_groq's ChatGroq"""
        if not self.api_key:
            raise ValueError("Groq API key not configured")
        
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "{prompt}"),
            ("human", "{article}"),
        ])
        llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name=self.default_model,
            temperature=0.3, #Low value for deterministic, factual summaries.
            max_tokens=250, #Max tokens for the summary.
            top_p=0.9, #Controls diversity of the response.
        )
        chain = chat_prompt | llm
        response = chain.invoke({"prompt": prompt, "article": article})
        summary = response.content.strip() if hasattr(response, "content") else str(response)
        return {
            "choices": [
                {
                    "message": {
                        "content": summary
                    }
                }
            ]
        }
    
    def summarize_article(self, article: str, prompting_method: str = 'zero_shot') -> Dict[str, Any]:
        """Main method to summarize research article using selected prompting method"""
        # Validate article
        is_valid, message = PromptGenerator.validate_article(article)
        if not is_valid:
            raise ValueError(message)
        
        # Create prompt based on method
        prompt = PromptGenerator.create_prompt_by_method(article, prompting_method)
        
        # Call API
        response = self.call_groq_api(prompt, article)
        
        # Extract summary
        if 'choices' in response and len(response['choices']) > 0:
            summary = response['choices'][0]['message']['content'].strip()
            
           
            summary_word_count = PromptGenerator.count_words(summary) # Validate summary length
            
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
        #Count words in text
        return PromptGenerator.count_words(text) 