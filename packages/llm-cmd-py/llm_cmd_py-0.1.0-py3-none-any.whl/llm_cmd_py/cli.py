#!/usr/bin/env python3

import click
import inquirer
from dotenv import load_dotenv

from .executor import execute_command
from .llm import generate_command

load_dotenv()

def get_command_by_number(commands, user_input):
    """Select command by number input"""
    try:
        num = int(user_input)
        if 1 <= num <= len(commands):
            return commands[num-1].split('. ', 1)[1]
    except ValueError:
        pass
    return None

@click.command()
@click.argument('prompt', nargs=-1, required=True)
def main(prompt):
    """Generate and execute shell commands using natural language."""
    try:
        prompt_text = ' '.join(prompt)
        commands = generate_command(prompt_text)
        
        if not commands:
            click.echo('No valid commands generated.')
            return
        
        numbered_commands = [f"{idx+1}. {cmd}" for idx, cmd in enumerate(commands)]
        
        # Print command list
        click.echo("Available commands:")
        for cmd in numbered_commands:
            click.echo(cmd)
        click.echo("\nEnter number or use arrow keys to select a command:")
        
        # Handle user input
        questions = [
            inquirer.List('command',
                         message='Select a command:',
                         choices=numbered_commands,
                         carousel=True)
        ]
        
        # First get direct input
        user_input = input().strip()
        selected_command = get_command_by_number(numbered_commands, user_input)
        
        # If not number input, use arrow selection
        if selected_command is None:
            answers = inquirer.prompt(questions)
            if not answers:
                return
            selected_command = answers['command'].split('. ', 1)[1]
        
        # Execute selected command
        execute_command(selected_command)
        
    except Exception as e:
        click.echo(f'An error occurred: {str(e)}', err=True)

if __name__ == '__main__':
    main() 