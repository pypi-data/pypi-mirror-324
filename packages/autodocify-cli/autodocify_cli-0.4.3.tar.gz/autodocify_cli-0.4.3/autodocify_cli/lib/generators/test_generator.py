import os
from pathlib import Path
from autodocify_cli.lib.generators.helper import process_generation
from rich.console import Console
from rich.progress import Progress
from rich.spinner import Spinner
from typing import List
from autodocify_cli.lib.project_content_merger import merge_files
from autodocify_cli.lib.utils import test_prompt
from autodocify_cli.lib.services.ai_integration import AI

console = Console()


def generate_test_files(
    base_path: str, output_file: str, llm: str, project_files: List[str]
):
    process_generation(
        base_path=base_path,
        project_files=project_files,
        output_file=output_file,
        llm=llm,
        generate_prompt=test_prompt,
        success_message="Test files generated successfully at",
        spinner_message="🛠️ Generating test files...",
        spinner_style="line",
    )


# def generate_test_files(base_path: str, llm: str, project_files: List[str]):
#     """
#     Creates a 'tests' folder in the specified directory if it doesn't already exist,
#     and generates test files based on the content of the project.

#     Args:
#         base_path (str): The base directory for the project.
#         llm (str): The language model to use (e.g., gemini, openai, bard).
#         project_files (List[str]): A list of valid project files to generate tests for.

#     Returns:
#         None: Writes the generated test content to files in the 'tests' folder.
#     """
#     try:
#         if not project_files:
#             console.print("❌ [red]No files provided to generate tests.[/red]")
#             return

#         console.print("[bold cyan]📂 Validating files...[/bold cyan]")
#         base_path = Path(base_path)
#         tests_folder = base_path / "tests"

#         # Ensure the 'tests' directory exists
#         tests_folder.mkdir(parents=True, exist_ok=True)

#         # Define the main test file
#         test_file = tests_folder / "test_main.py"

#         # Merge project file contents
#         console.print("[bold cyan]🛠️ Merging files for test generation...[/bold cyan]")
#         with console.status("[bold cyan]🛠️ Merging files...[/bold cyan]", spinner="dots"):
#             content = merge_files(base_path, project_files)
#         if not content.strip():
#             console.print("❌ [red]Error: Merged file content is empty.[/red]")
#             # Write a placeholder test file as fallback
#             test_file.write_text(
#                 "# Placeholder test file\n"
#                 "def test_placeholder():\n"
#                 "    assert True\n",
#                 encoding="utf-8",
#             )
#             return

#         # Generate AI prompt for tests
#         console.print("[bold cyan]🤖 Generating test content with AI...[/bold cyan]")
#         with console.status("[bold cyan]🤖 Generating tests...[/bold cyan]", spinner="line"):
#             prompt = test_prompt(content)
#             result = AI(prompt, llm)

#         # Validate AI response
#         if not result or not result.strip():
#             console.print("❌ [red]Error: AI returned empty or invalid content for tests.[/red]")
#             return

#         # Write the generated test content to the main test file
#         test_file.write_text(result, encoding="utf-8")
#         console.print(f"✅ [green]Test files generated successfully at '{tests_folder.resolve()}'. 🎉[/green]")

#     except Exception as e:
#         console.print(f"❌ [red]Unexpected error: {e}[/red]")
#     finally:
#             os.remove(f"{base_path}/merge.txt")
#             console.print("🧹 [yellow]Temporary merge.txt file deleted.[/yellow]")
