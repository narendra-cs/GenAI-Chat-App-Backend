# GenAI Chat App - Backend

A high-performance backend service for the GenAI Chat Application, built with FastAPI. This service provides the API endpoints for the chat interface, handles conversation management, and integrates with various AI models.

## 🚀 Features

- 💬 Real-time chat with AI models
- 🔐 User authentication and authorization
- 📝 Conversation history management
- ⚡ Fast and scalable API endpoints
- 📊 Built-in API documentation
- 🧪 Comprehensive test coverage
- 🔄 Asynchronous request handling

## 🛠 Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/narendra-cs/GenAI-Chat-App-Backend.git
   cd GenAI-Chat-App-Backend
   ```

2. **Set up the environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Unix/macOS
   source venv/bin/activate
   # On Windows
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API documentation**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 🏗 Project Structure

```
GenAI-Chat-App-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ChatApp/
│       ├── __init__.py
│       └── request_models.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── setup.sh
├── .pre-commit-config.yaml
├── .gitignore
└── README.md
```

## 📚 API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

## 🧹 Code Quality

### Pre-commit Hooks
Pre-commit hooks will automatically run on each commit. They include:
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (static type checking)

### Manual Code Formatting

```bash
# Format code with Black
black .

# Sort imports
isort .

# Run linter
flake8

# Run type checking
mypy .
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Documentation powered by [Swagger UI](https://swagger.io/tools/swagger-ui/) and [ReDoc](https://github.com/Redocly/redoc)
