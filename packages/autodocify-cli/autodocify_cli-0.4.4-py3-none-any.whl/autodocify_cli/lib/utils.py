import subprocess
from pathlib import Path
from typing import List, Optional
from autodocify_cli.core.exceptions import GitError
from autodocify_cli.lib.get_general_project_files import get_general_project_files
import typer
from autodocify_cli.lib.prompt_templates.readme_prompt_template import (
    readme_prompt_template,
)
from autodocify_cli.lib.prompt_templates.technical_doc_prompt_template import (
    technical_doc_prompt_template,
)
from autodocify_cli.lib.prompt_templates.test_prompt_template import (
    test_doc_prompt_template,
)
from autodocify_cli.lib.prompt_templates.swagger_prompt_template import (
    swagger_doc_prompt_template,
)
from autodocify_cli.core.settings.config import LLMEnum

# Centralized exclusions
DEFAULT_EXCLUDED_PATHS = {".github/workflows", "tests", "CHANGELOG.md"}
DEFAULT_EXCLUDED_EXTENSIONS = {
    ".log",
    ".tmp",
    ".yml",
    ".yaml",
    ".gitignore",
    ".json",
    ".lock",
    ".toml",
    ".md",
}


def greet_user(name: str = "Comrade") -> str:
    """
    Returns a greeting message.
    """
    return f"Hello, {name}! Welcome to AutoDocify."


def get_base_path(base_dir: Optional[str] = None) -> Path:
    """
    Returns the base path for the project directory or raises an error if invalid.
    """
    base_path = Path(base_dir or Path.cwd())
    if not base_path.exists():
        typer.echo(f"Error: The directory {base_path} does not exist.")
        raise typer.Exit(code=1)
    return base_path


def is_git_initialized(base_path: Path) -> bool:
    """
    Check if the directory is a Git repository.
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=base_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        # raise GitError(f"The directory '{base_path}' is not a Git repository.")
        return False


def warn_untracked_files(base_path: Path):
    """
    Warn the user if there are untracked files in the Git repository.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=base_path,
            text=True,
            capture_output=True,
            check=True,
        )
        untracked_files = [
            line[3:]
            for line in result.stdout.strip().split("\n")
            if line.startswith("??")
        ]
        if untracked_files:
            typer.echo(
                f"Warning: There {'are' if len(untracked_files) > 1 else 'is'} {len(untracked_files)} untracked {'files' if len(untracked_files) > 1 else 'file'}. Consider running 'git add'."
            )
    except subprocess.CalledProcessError:
        typer.echo("Error: Unable to check for untracked files.")


def get_git_tracked_files(base_path: Path) -> List[str]:
    """
    Retrieve a list of all files tracked by Git in the given directory,
    excluding deleted files, excluded paths, and excluded extensions.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=base_path,
            text=True,
            capture_output=True,
            check=True,
        )
        tracked_files = result.stdout.strip().split("\n")

        deleted_result = subprocess.run(
            ["git", "ls-files", "--deleted"],
            cwd=base_path,
            text=True,
            capture_output=True,
            check=True,
        )
        deleted_files = deleted_result.stdout.strip().split("\n")

        valid_files = [
            file
            for file in tracked_files
            if file not in deleted_files
            and not any(file.startswith(f"{path}/") for path in DEFAULT_EXCLUDED_PATHS)
            and not any(file.endswith(ext) for ext in DEFAULT_EXCLUDED_EXTENSIONS)
        ]
        return valid_files
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error retrieving tracked files: {e}")
        return []


def get_project_files(base_path: Path) -> List[str]:
    """
    Retrieve project files either from a Git repository or general directory structure.
    """
    if is_git_initialized(base_path):
        warn_untracked_files(base_path)
        tracked_files = get_git_tracked_files(base_path)
        if not tracked_files:
            typer.echo("No tracked files found in the repository.")
        return tracked_files
    else:
        typer.echo(
            "Warning: The provided directory is not a Git repository. Falling back to general file scanning."
        )
        return get_general_project_files(base_path)


def readme_prompt(content: str) -> str:
    """
    Generates a README prompt based on the provided content.
    """
    return f"{readme_prompt_template}\n\nHere is the project content:\n{content}"


def technical_docs_prompt(content: str) -> str:
    """
    Generates a technical documentation prompt based on the provided content.
    """
    return f"{technical_doc_prompt_template}\n\nHere is the project content:\n{content}"


def create_test_prompt(content: str) -> str:
    """
    Generates a test prompt based on the provided content.
    """
    return f"{test_doc_prompt_template}\n\nHere is the project content:\n{content}"


def swagger_prompt(content: str, format: str = "json") -> str:
    """
    Generates a swagger prompt based on the provided content.
    """
    return f"{swagger_doc_prompt_template}\n\nHere is the project content:\n{content}\n\nAnd the format it should be in:\n{format}"


def check_llm(llm: str):
    llms = [option.value for option in LLMEnum]
    if llm not in llms:
        raise typer.BadParameter(
            f"Invalid LLM Specified. Valid option(s) are {LLMEnum.get_values()}"
        )
    else:
        return llm
