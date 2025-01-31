import subprocess
from typing import Optional

def execute_command(command: str) -> Optional[str]:
    """Execute the shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e.stderr}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None 