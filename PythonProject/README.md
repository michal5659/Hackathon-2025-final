# AI Multi-Agent Orchestration System

A Python-based AI multi-agent system designed for processing and executing tasks through IDIT API integration. This system uses AI agents to classify messages, create tasks, and execute operations with intelligent data processing.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agents](#agents)
- [API Integration](#api-integration)
- [Contributing](#contributing)

## 🎯 Overview

This multi-agent orchestration system processes user messages, classifies them, and executes appropriate tasks via the IDIT API. The system leverages AI to understand natural language requests and perform operations like updating contact information, managing policies, and handling customer service tasks.

## ✨ Features

- **AI-Powered Classification**: Automatically classifies incoming messages to determine the appropriate action
- **Task Execution**: Executes tasks through IDIT API integration
- **Asynchronous Processing**: Handles multiple concurrent tasks efficiently
- **Flexible Architecture**: Modular agent-based design for easy extension
- **Natural Language Understanding**: Processes requests in multiple languages including English and Hebrew
- **API Integration**: Seamless integration with IDIT web services

## 🏗️ Architecture

The system follows a multi-agent architecture with the following components:

```
<img width="912" height="864" alt="image" src="https://github.com/user-attachments/assets/dc5075c4-60e2-453d-895c-7b6f2e7779e7" />

```

### Key Components:

1. **Orchestrator**: Central coordinator managing message flow and agent interactions
2. **Classification Agent**: Analyzes and categorizes incoming messages
3. **Task Execution Agent**: Executes API calls and processes responses
4. **Simple AI Agent**: Provides AI-powered response generation and data processing

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Access to IDIT API (required credentials)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PythonProject
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   # API Configuration
   IDIT_API_BASE_URL=https://core-trunk-ci-qa.idit.sapiens.com:443
   IDIT_API_KEY=your_api_key_here
   
   # AI Configuration
   OPENAI_API_KEY=your_openai_key_here
   
   # Application Settings
   MAX_CONCURRENT_TASKS=5
   LOG_LEVEL=INFO
   ```

## ⚙️ Configuration

Configuration is managed through the `config/settings.py` file. Key settings include:

- **API Endpoints**: Configure IDIT API base URLs
- **Concurrency**: Set maximum concurrent task processing
- **Logging**: Configure log levels and output
- **Agent Parameters**: Customize AI agent behavior

## 🚀 Usage

### Running the Application

```bash
python main.py
```

### Basic Example

```python
import asyncio
from orchestarator import get_orchestrator

async def process_request():
    orchestrator = get_orchestrator()
    
    message = {
        "message_id": "123",
        "title": "Update Address",
        "content": "I want to update my address to 3 Broyer st. Bnei Brak",
        "sender": "user@example.com",
        "channel": "email"
    }
    
    result = await orchestrator.process_message(message)
    print(f"Result: {result}")

asyncio.run(process_request())
```

### Processing Messages

The system can process messages from various channels:
- Email
- Teams
- Web forms
- Manual input

## 📁 Project Structure

```
PythonProject/
│
├── main.py                  # Application entry point
├── orchestarator.py         # Main orchestrator logic
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
│
├── agents/                 # AI Agents
│   ├── __init__.py
│   ├── classification_agent.py     # Message classification
│   ├── simple_ai_agent.py          # AI response generation
│   └── task_execution_agent.py     # Task execution
│
├── config/                 # Configuration
│   ├── __init__.py
│   └── settings.py         # Application settings
│
├── services/              # External services
│   ├── __init__.py
│   └── api_utils.py       # API utilities
│
└── __pycache__/           # Python cache (auto-generated)
```

## 🤖 Agents

### Classification Agent
Analyzes incoming messages and determines:
- Message intent
- Required action type (GET, POST, PUT, DELETE)
- Entity type (contact, policy, claim, etc.)
- Priority level

### Task Execution Agent
Responsible for:
- Extracting task parameters
- Calling IDIT API endpoints
- Processing API responses
- Generating user-friendly responses

### Simple AI Agent
Provides:
- Natural language understanding
- Response generation
- Data transformation and formatting
- Multi-language support

## 🔌 API Integration

### IDIT API

The system integrates with IDIT web services for:
- Contact management
- Policy operations
- Claim processing
- Account management

### API Utilities

Located in `services/api_utils.py`, provides:
- HTTP request handling
- Authentication management
- Error handling and retry logic
- Response parsing

## 📝 Example Use Cases

1. **Update Contact Information**
   ```
   Input: "Update my address to 8 HaTanya Street, Bnei Brak"
   → Classifies as contact update
   → Extracts address components
   → Updates contact via API
   → Confirms to user
   ```

2. **Query Policy Details**
   ```
   Input: "What's my current policy status?"
   → Classifies as policy query
   → Retrieves policy information
   → Formats response
   → Returns to user
   ```

3. **Process Claims**
   ```
   Input: "I want to file a claim for my car accident"
   → Classifies as claim creation
   → Collects necessary information
   → Initiates claim process
   → Provides confirmation
   ```

## 🛠️ Development

### Adding a New Agent

1. Create a new file in `agents/` directory
2. Implement the agent class
3. Add singleton getter function
4. Register in `agents/__init__.py`
5. Update orchestrator to use the new agent

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_agents.py

# Run with coverage
python -m pytest --cov=agents
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all `__init__.py` files exist in package directories
   - Use relative imports within packages (e.g., `from .module import func`)
   - Clear `__pycache__` directories if encountering stale imports

2. **API Connection Issues**
   - Verify API credentials in `.env` file
   - Check network connectivity
   - Ensure API endpoints are correct

3. **AttributeError on Agent Methods**
   - Ensure class and method names match between import and definition
   - Check that agents return expected data structures

## 📄 License

[Specify your license here]

## 👥 Contributors

- Development Team - Sapiens Hackathon 2025

## 📞 Support

For issues and questions:
- Open an issue in the repository
- Contact the development team
- Check documentation in `/docs` (if available)

## 🔄 Version History

- **v1.0.0** (Current) - Initial release with core functionality
  - Message classification
  - Task execution
  - IDIT API integration
  - Multi-agent orchestration

---

**Last Updated**: November 2025  
**Project**: Hackathon 2025

