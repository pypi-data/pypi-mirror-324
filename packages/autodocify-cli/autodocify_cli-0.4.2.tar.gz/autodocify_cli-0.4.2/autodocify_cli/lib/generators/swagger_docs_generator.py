from pathlib import Path
import os
from autodocify_cli.lib.generators.helper import process_generation
from rich.console import Console
from rich.progress import Progress
from rich.spinner import Spinner
from typing import List
from autodocify_cli.lib.project_content_merger import merge_files
from autodocify_cli.lib.utils import swagger_prompt
from autodocify_cli.lib.services.ai_integration import AI

console = Console()



def generate_swagger_docs(base_path: str, output_file: str, format: str, llm: str, project_files: List[str]):
    process_generation(
        base_path=base_path,
        project_files=project_files,
        output_file=output_file,
        llm=llm,
        generate_prompt=lambda content: swagger_prompt(content, format),
        success_message="Swagger documentation generated successfully at",
        spinner_message="🛠️ Generating Swagger documentation...",
        spinner_style="moon"
    )


# def generate_swagger_docs(base_path: str, output_file: str, format: str, llm: str, project_files: List[str]):
    """
    Generates a Swagger documentation file for the project by merging content from the specified base directory.

    Args:
        base_path (str): The base directory for the project.
        output_file (str): Path to the output Swagger documentation file.
        format (str): The format of the Swagger docs (json or yaml).
        llm (str): The AI language model to use (e.g., gemini, openai, bard).
        project_files (List[str]): A list of valid project files to include in the Swagger docs.

    Returns:
        None: Writes the Swagger documentation to the specified output file.
    """
    try:
        if not project_files:
            console.print("❌ [red]No files provided to generate Swagger documentation.[/red]")
            return

        console.print("[bold cyan]📂 Validating files...[/bold cyan]")
        base_path = Path(base_path)
        output_file = Path(output_file)

        # Filter valid files
        valid_project_files = [file for file in project_files if (base_path / file).exists()]
        if not valid_project_files:
            console.print("⚠️ [yellow]No valid project files found. Exiting...[/yellow]")
            return

        # Merge file contents
        console.print("[bold cyan]🛠️ Merging files for Swagger documentation...[/bold cyan]")
        with console.status("[bold cyan]🛠️ Merging files...[/bold cyan]", spinner="moon"):
            content = merge_files(base_path, valid_project_files)
        if not content.strip():
            console.print("❌ [red]Error: Merged file content is empty.[/red]")
            return

        # Generate AI prompt for Swagger documentation
        console.print("[bold cyan]🤖 Generating Swagger documentation with AI...[/bold cyan]")
        with console.status("[bold cyan]🤖 Generating Swagger content...[/bold cyan]", spinner="earth"):
            prompt = swagger_prompt(content, format)
            result = AI(prompt, llm)

        if not result or not result.strip():
            console.print("❌ [red]Error: AI returned empty or invalid content for Swagger documentation.[/red]")
            return

        # Write the result to the output file
        output_file.write_text(result, encoding="utf-8")
        console.print(f"✅ [green]Swagger documentation generated successfully at '{output_file.resolve()}'. 🎉[/green]")

    except Exception as e:
        console.print(f"❌ [red]Unexpected error: {e}[/red]")
    finally:
            os.remove(f"{base_path}/merge.txt")
            console.print("🧹 [yellow]Temporary merge.txt file deleted.[/yellow]")