from pathlib import Path
from typing import Callable, List
import os
from rich.console import Console
from autodocify_cli.lib.project_content_merger import merge_files
from autodocify_cli.lib.services.ai_integration import AI

console = Console()

def process_generation(
    base_path: str,
    project_files: List[str],
    output_file: str,
    llm: str,
    generate_prompt: Callable[[str], str],
    success_message: str,
    spinner_message: str,
    spinner_style: str = "dots"
):
    """
    Generalized function to handle file generation workflows for README, technical docs, tests, etc.

    Args:
        base_path (str): The base directory for the project.
        project_files (List[str]): A list of project files to process.
        output_file (str): Path to the output file.
        llm (str): The language model to use (e.g., gemini, openai, bard).
        generate_prompt (Callable[[str], str]): A function to generate the AI prompt.
        success_message (str): Message to display upon successful generation.
        spinner_message (str): Message to display in the spinner.
        spinner_style (str): Style of the spinner for the progress indicator.

    Returns:
        None
    """
    try:
        base_path = Path(base_path)
        output_file = Path(output_file)
        merge_path = base_path / "merge.txt"

        # Validate project files
        if not project_files:
            console.print("❌ [red]No files provided for generation.[/red]")
            return

        valid_files = [file for file in project_files if (base_path / file).exists()]
        if not valid_files:
            console.print("⚠️ [yellow]No valid project files found. Exiting...[/yellow]")
            return

        # Merge files
        console.print("[bold cyan]🛠️ Merging files...[/bold cyan]")
        with console.status(f"[bold cyan]{spinner_message}[/bold cyan]", spinner=spinner_style):
            content = merge_files(base_path, valid_files)

        if not content.strip():
            console.print("❌ [red]Error: Merged file content is empty.[/red]")
            return

        # Generate AI prompt and process
        console.print("[bold cyan]🤖 Generating content with AI...[/bold cyan]")
        with console.status("[bold cyan]Processing with AI...[/bold cyan]", spinner=spinner_style):
            prompt = generate_prompt(content)
            result = AI(prompt, llm)

        if not result or not result.strip():
            console.print("❌ [red]Error: AI returned empty or invalid content.[/red]")
            return

        # Write the result to the output file
        output_file.write_text(result, encoding="utf-8")
        console.print(f"✅ [green]{success_message} '{output_file.resolve()}'. 🎉[/green]")

    except Exception as e:
        console.print(f"❌ [red]Unexpected error: {e}[/red]")
    finally:
        # Cleanup temporary merge file
        
            os.remove(f"{base_path}/merge.txt")
            console.print("🧹 [yellow]Temporary merge.txt file deleted.[/yellow]")
