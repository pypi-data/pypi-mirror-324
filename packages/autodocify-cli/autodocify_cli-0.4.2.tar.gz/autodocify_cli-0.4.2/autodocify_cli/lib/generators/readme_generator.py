import os
from pathlib import Path
from typing import List
from autodocify_cli.lib.generators.helper import process_generation
import typer
# from yaspin import yaspin
from autodocify_cli.lib.project_content_merger import merge_files
from autodocify_cli.lib.utils import get_git_tracked_files, readme_prompt
from autodocify_cli.lib.services.ai_integration import AI
# from rich.console import Console
# from rich.spinner import Spinner
# from rich.progress import Progress

# console = Console()

def generate_read_me(base_path: str, output_file: str, llm: str, project_files: List[str]):
    process_generation(
        base_path=base_path,
        project_files=project_files,
        output_file=output_file,
        llm=llm,
        generate_prompt=readme_prompt,
        success_message="README generated successfully at",
        spinner_message="🛠️ Generating README content...",
        spinner_style="dots"
    )





# def generate_read_me(base_path: str, output_file: str, llm: str, project_files: List[str]):
#     try:
#         if not project_files:
#             console.print("❌ [red]No files provided to generate the README.[/red]")
#             return

#         console.print("[bold cyan]📂 Validating files...[/bold cyan]")
#         base_path = Path(base_path)
#         output_file = Path(output_file)

#         # Check base path
#         if not base_path.exists() or not base_path.is_dir():
#             console.print(f"❌ [red]Error: The directory '{base_path}' does not exist.[/red]")
#             return

#         # Filter valid files
#         valid_project_files = [file for file in project_files if (base_path / file).exists()]
#         if not valid_project_files:
#             console.print("⚠️ [yellow]No valid project files found. Exiting...[/yellow]")
#             return

#         # Merge file contents
#         console.print("[bold cyan]🛠️ Merging files...[/bold cyan]")
#         with console.status("[bold cyan]🛠️ Merging files...[/bold cyan]", spinner="dots"):
#             content = merge_files(base_path, valid_project_files)
#         if not content.strip():
#             console.print("❌ [red]Error: Merged file content is empty.[/red]")
#             return

#         # Generate AI prompt
#         console.print("[bold cyan]🤖 Generating README content with AI...[/bold cyan]")
#         with console.status("[bold cyan]🤖 Generating README content with AI...[/bold cyan]", spinner="bouncingBall"):
#             prompt = readme_prompt(content)
#             result = AI(prompt, llm)

#         if not result or not result.strip():
#             console.print("❌ [red]Error: AI returned empty or invalid content.[/red]")
#             return

#         # Write result to output file
#         output_file.write_text(result, encoding="utf-8")
#         console.print(f"✅ [green]README generated successfully at '{output_file.resolve()}'. 🎉[/green]")

#     except Exception as e:
#         console.print(f"❌ [red]Unexpected error: {e}[/red]")
#     finally:
#             os.remove(f"{base_path}/merge.txt")
#             console.print("🧹 [yellow]Temporary merge.txt file deleted.[/yellow]")
