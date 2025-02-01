"""Main entry point for the code quality analyzer.

Example usage:
    python-code-quality-analyzer analyze                # Analyze current directory
    python-code-quality-analyzer analyze src/           # Analyze src directory
    python-code-quality-analyzer analyze -f json        # Output in JSON format
    python-code-quality-analyzer analyze -e "*.test.py" # Exclude test files
"""

import click
from rich.console import Console

console = Console()

@click.group()
def main():
    """Python Code Quality Analyzer - A tool for analyzing Python code quality."""
    pass

@main.command()
@click.argument('path', type=click.Path(exists=True))
def analyze(path):
    """Analyze Python code quality in the specified path."""
    console.print(f"[bold green]Analyzing code in:[/] {path}")
    # TODO: Implement code analysis logic

if __name__ == '__main__':
    main() 