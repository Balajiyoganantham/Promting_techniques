# Advanced Research Article Summarizer

A sophisticated Flask application that leverages advanced prompting techniques with Groq's `llama-3.1-8b-instant` model to generate comprehensive research article summaries. This tool demonstrates various AI prompting methodologies and provides a practical interface for research article analysis.

## 🚀 Features

- **9 Advanced Prompting Methods**: Chain-of-Thoughts, Tree-of-Thoughts, Role-based, ReAct, Directional Stimulus, Step-Back, Zero-shot, One-shot, and Few-shot
- **Smart Validation**: Real-time word counting and content validation (500-1000 words)
- **Modern UI**: Responsive design with real-time feedback and progress indicators
- **Fast Processing**: Uses Groq's lightning-fast `llama-3.1-8b-instant` model
- **RESTful API**: Complete API endpoints for integration with other applications
- **Health Monitoring**: Built-in health check endpoint for system monitoring
- **Modular Architecture**: Clean separation of concerns with dedicated modules for prompts, summarization, and API routes

## 🏗️ Architecture

The application follows a modular architecture pattern for better maintainability and scalability:

- **`app.py`**: Main Flask application entry point and configuration
- **`prompts.py`**: All prompt templates and generation logic
- **`summarizer.py`**: Core summarization logic using GROQ API
- **`routes/api_routes.py`**: API route handlers and endpoints
- **`templates/index.html`**: Frontend interface

## 📋 Prerequisites

- Python 3.7 or higher
- Groq API key (get it from [console.groq.com/keys](https://console.groq.com/keys))
- Internet connection for API calls

## 🛠️ Installation & Setup

### 1. Clone and Navigate
```bash
cd "path/to/your/project"
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# If not already included, also install langchain-core:
pip install langchain-core
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Groq API Configuration
GROQ_API_KEY=your_actual_groq_api_key_here

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important**: 
- Replace `your_actual_groq_api_key_here` with your real Groq API key from [console.groq.com/keys](https://console.groq.com/keys)
- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` file

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Application
Open your browser and go to: `http://localhost:5000`

## 🎯 How to Use

### Web Interface
1. **Select Prompting Method**: Choose from 9 advanced prompting techniques
2. **Paste Research Article**: Enter a research article (500-1000 words)
3. **Validate Content**: Use the validation feature to check article length
4. **Generate Summary**: Click the button and get your comprehensive summary

### API Usage
The application provides RESTful API endpoints for programmatic access:

#### Summarize Article
```bash
POST /api/summarize
Content-Type: application/json

{
    "article": "Your research article text here...",
    "prompting_method": "chain_of_thoughts"
}
```

#### Get Available Methods
```bash
GET /api/prompting-methods
```

#### Validate Article
```bash
POST /api/validate
Content-Type: application/json

{
    "article": "Your research article text here..."
}
```

#### Health Check
```bash
GET /health
```

## 🔧 Available Prompting Methods

| Method | Description | Best For |
|--------|-------------|----------|
| **Chain-of-Thoughts** | Step-by-step systematic reasoning | Complex research with multiple components |
| **Tree-of-Thoughts** | Multiple reasoning paths simultaneously | Articles with multiple perspectives |
| **Role-based** | AI as senior research analyst | Professional academic summaries |
| **ReAct** | Reasoning + Acting iteratively | Problem-solving focused research |
| **Directional Stimulus** | Specific guidance toward output | Structured, consistent summaries |
| **Step-Back** | Higher-level perspective first | Understanding broader implications |
| **Zero-shot** | Direct instruction without examples | Quick, straightforward summaries |
| **One-shot** | Single example to guide format | Consistent formatting requirements |
| **Few-shot** | Multiple examples for pattern | Complex formatting or style requirements |

## 📁 Project Structure

```
├── app.py                     # Main Flask application entry point
├── prompts.py                 # All prompt templates and generation logic
├── summarizer.py              # Core logic for summarization using GROQ API
├── routes/
│   ├── __init__.py           # Routes package initialization
│   └── api_routes.py         # API route handlers and endpoints
├── templates/
│   └── index.html            # Frontend interface
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore file
├── venv/                    # Virtual environment
└── README.md               # This documentation file
```

## 🔧 Module Documentation

### `app.py`
Main Flask application that serves as the entry point. Handles:
- Flask app initialization and configuration
- CORS setup
- Blueprint registration
- Main route serving the web interface

### `prompts.py`
Contains the `PromptGenerator` class and all prompting methods:
- **`PromptGenerator`**: Static class with methods for each prompting technique
- **`PROMPTING_METHODS`**: Dictionary mapping method keys to display names
- **`count_words()`**: Utility function for word counting
- **`validate_article()`**: Article length and content validation

### `summarizer.py`
Contains the `ResearchSummarizer` class for API interactions:
- **`ResearchSummarizer`**: Main class for handling GROQ API calls
- **`call_groq_api()`**: Uses LangChain's compositional API (`ChatPromptTemplate` and chaining) to interact with the GROQ LLM. The prompt template is dynamically generated based on the selected prompting method, supporting zero-shot, few-shot, and other advanced prompting techniques.
- **`summarize_article()`**: Orchestrates the summarization process, including validation, prompt generation, and summary extraction.
- **Configuration**: API key, model selection, and request parameters

#### How it Works (LangChain Chaining Style)
The summarizer now uses LangChain's compositional API for prompt and LLM chaining. For each summarization request:
1. The appropriate prompt is generated using the selected prompting method (e.g., zero-shot, few-shot, etc.).
2. A `ChatPromptTemplate` is created, with placeholders for the prompt and article.
3. The prompt template and the LLM (`ChatGroq`) are chained using the `|` operator.
4. The chain is invoked with the prompt and article, and the summary is extracted from the response.

**Example (Python):**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

prompt = ChatPromptTemplate.from_messages([
    ("system", "{prompt}"),
    ("human", "{article}"),
])
llm = ChatGroq(
    groq_api_key="YOUR_API_KEY",
    model_name="llama-3-1-8b-instant",
    temperature=0.3,
    max_tokens=250,
    top_p=0.9,
)
chain = prompt | llm
response = chain.invoke({"prompt": "Your generated prompt here", "article": "Your article text here."})
print(response.content)
```

This approach allows flexible support for all advanced prompting methods.

### `routes/api_routes.py`
Contains all API route handlers using Flask Blueprint:
- **`api_bp`**: Blueprint for all API routes
- **`/api/summarize`**: POST endpoint for article summarization
- **`/api/prompting-methods`**: GET endpoint for available methods
- **`/api/validate`**: POST endpoint for article validation
- **`/health`**: GET endpoint for health checks

## 🔌 API Reference

### Endpoints

#### `GET /`
- **Description**: Serves the main web interface
- **Response**: HTML page

#### `GET /api/prompting-methods`
- **Description**: Returns available prompting methods
- **Response**: JSON object with method names and descriptions

#### `POST /api/summarize`
- **Description**: Summarizes a research article using specified prompting method
- **Request Body**:
  ```json
  {
    "article": "Research article text (500-1000 words)",
    "prompting_method": "chain_of_thoughts"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "summary": "Generated summary...",
      "word_count": 120,
      "prompting_method": "chain_of_thoughts",
      "model_used": "llama-3.1-8b-instant",
      "article_word_count": 750,
      "timestamp": "2024-01-01T12:00:00"
    }
  }
  ```

#### `POST /api/validate`
- **Description**: Validates article length and content
- **Request Body**:
  ```json
  {
    "article": "Research article text"
  }
  ```
- **Response**:
  ```json
  {
    "valid": true,
    "message": "Article length valid (750 words)",
    "word_count": 750
  }
  ```

#### `GET /health`
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "model": "llama-3.1-8b-instant",
    "available_methods": ["chain_of_thoughts", "tree_of_thoughts", ...]
  }
  ```

## 🔒 Security & Best Practices

### Environment Variables
- Store sensitive data in `.env` files
- Never hardcode API keys in source code
- Use environment-specific configurations

### API Key Security
- Keep your Groq API key secure and private
- Rotate API keys regularly
- Monitor API usage for unusual activity

### Application Security
- The application uses CORS for cross-origin requests
- Input validation prevents malicious content
- Error handling prevents information leakage

### Code Organization
- Modular architecture promotes maintainability
- Separation of concerns improves testability
- Blueprint pattern enables scalable route management

## 🐛 Troubleshooting

### Common Issues

#### 1. "API key not configured" error
**Solution**:
- Ensure you've created a `.env` file in the project root
- Verify your API key is correctly set: `GROQ_API_KEY=your_key_here`
- Restart the Flask application after adding the `.env` file
- Check that there are no extra spaces or quotes around the API key

#### 2. "Server disconnected" error
**Solution**:
- Ensure the Flask app is running: `python app.py`
- Check that the server is accessible at `http://localhost:5000`
- Verify no firewall is blocking the connection
- Check the console for any error messages

#### 3. Import errors
**Solution**:
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again
- Check Python version compatibility (3.7+)
- Verify all modules are in the correct locations

#### 4. "Article too short/long" error
**Solution**:
- Ensure your article is between 500-1000 words
- Use the validation feature before submitting
- Check for proper text formatting

#### 5. API rate limiting
**Solution**:
- Check your Groq API usage limits
- Implement request throttling if needed
- Monitor API response headers for rate limit information

#### 6. Module import issues
**Solution**:
- Ensure the `routes` directory contains `__init__.py`
- Check that all import statements use correct relative paths
- Verify the project structure matches the documentation

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up proper logging
- Implementing monitoring and health checks
- Using environment-specific configurations
- Setting up SSL/TLS certificates

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📊 Performance

- **Model**: Groq's `llama-3.1-8b-instant` for fast inference
- **Response Time**: Typically 1-3 seconds for article summarization
- **Concurrent Requests**: Flask development server handles multiple requests
- **Memory Usage**: Minimal memory footprint
- **Modular Design**: Improved maintainability and scalability

## 🔄 Development Workflow

### Adding New Prompting Methods
1. Add the method to `prompts.py` in the `PromptGenerator` class
2. Update the `PROMPTING_METHODS` dictionary
3. Add the method to the `create_prompt_by_method` mapping
4. Test the new method through the API

### Extending API Functionality
1. Add new routes to `routes/api_routes.py`
2. Use the existing `api_bp` Blueprint
3. Follow the established error handling patterns
4. Update documentation as needed

### Modifying Summarization Logic
1. Update the `ResearchSummarizer` class in `summarizer.py`
2. Maintain the existing interface for compatibility
3. Test changes through the API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the modular architecture
4. Add tests if applicable
5. Update documentation for any new features
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Groq API key is valid
3. Ensure all dependencies are installed correctly
4. Check the application logs for detailed error messages
5. Verify the project structure matches the documentation

## 🔗 Useful Links

- [Groq API Documentation](https://console.groq.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Flask Blueprint Documentation](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

---

**Happy Summarizing! 🚀**

*Built with ❤️ using Flask, Groq API, and advanced AI prompting techniques with a modular architecture.* 