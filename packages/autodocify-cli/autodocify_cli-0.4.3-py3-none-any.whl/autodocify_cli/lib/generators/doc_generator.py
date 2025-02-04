from pathlib import Path
from autodocify_cli.lib.generators.helper import process_generation
from rich.console import Console
from rich.progress import Progress
from typing import List
from autodocify_cli.lib.project_content_merger import merge_files
from autodocify_cli.lib.utils import technical_docs_prompt
from autodocify_cli.lib.services.ai_integration import AI
import os

console = Console()




def generate_technical_docs(base_path: str, output_file: str, llm: str, project_files: List[str]):
    process_generation(
        base_path=base_path,
        project_files=project_files,
        output_file=output_file,
        llm=llm,
        generate_prompt=technical_docs_prompt,
        success_message="Technical documentation generated successfully at",
        spinner_message="🛠️ Generating technical documentation...",
        spinner_style="arrow3"
    )

