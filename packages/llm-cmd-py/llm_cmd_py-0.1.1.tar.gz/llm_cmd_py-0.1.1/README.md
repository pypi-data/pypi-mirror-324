# LLM-CMD Python Version

## Introduction
This is the Python version of LLM-CMD, a command-line tool that generates and executes system commands using natural language.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- pip or poetry

### Installation
1. Clone the repository
```bash
git clone https://github.com/whyparkc/llm-cmd-py    
cd llm-cmd-py
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file and set the following variables:
```plaintext
LLM_ENDPOINT="https://api.openai.com/v1"
LLM_API_KEY="your-api-key-here"
LLM_MODEL="gpt-4o-mini"
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=100
```

5. Install in development mode
```bash
pip install -e .
```

## Usage Example
```bash
llm-cmd find all python files in current directory
```

## License
MIT License 