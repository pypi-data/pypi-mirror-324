import os
import platform
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def clean_commands(text: str) -> List[str]:
    """Clean the commands by removing markdown code blocks and empty lines."""
    lines = text.strip().split('\n')
    commands = []
    for line in lines:
        # Remove markdown code block indicators
        line = line.strip().replace('```bash', '').replace('```', '')
        if line and not line.startswith('```'):
            commands.append(line)
    return commands

def generate_command(prompt: str) -> List[str]:
    """Generate shell commands from natural language prompt using LLM."""
    try:
        # Collect system information
        system_info = {
            'platform': platform.system(),
            'release': platform.release(),
            'type': os.name,
            'arch': platform.machine(),
            'cwd': os.getcwd()
        }
        
        client = OpenAI(
            api_key=os.getenv('LLM_API_KEY'),
            base_url=os.getenv('LLM_ENDPOINT')
        )
        
        # Construct prompt
        content = f"""System Information:
        - OS: {system_info['platform']} ({system_info['release']})
        - System Type: {system_info['type']}
        - Architecture: {system_info['arch']}
        - Current Working Directory: {system_info['cwd']}
        
        Please generate a command to perform the following task: {prompt}
        
        Requirements:
        1. Return only valid shell commands
        2. Each command should be on a new line
        3. Do not include any explanations, markdown formatting, or code blocks
        4. Return only the raw commands
        
        Example format:
        which node
        node --version"""
        
        response = client.chat.completions.create(
            model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
            messages=[{"role": "user", "content": content}],
            temperature=float(os.getenv('LLM_TEMPERATURE', 0.7)),
            max_tokens=int(os.getenv('LLM_MAX_TOKENS', 100))
        )
        
        # Extract and clean commands from response
        commands = clean_commands(response.choices[0].message.content)
        return [cmd for cmd in commands if cmd]
        
    except Exception as e:
        raise Exception(f"Failed to generate command: {str(e)}") 