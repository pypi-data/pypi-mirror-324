import typer
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress
from autodocify_cli.core.exceptions import (
    AIGenerationError,
    AutoDocifyError,
    GitError,
    InvalidDirectoryError,
)
from autodocify_cli.lib.utils import get_base_path, get_project_files
from autodocify_cli.lib.generators.readme_generator import generate_read_me
from autodocify_cli.lib.generators.test_generator import generate_test_files
from autodocify_cli.lib.generators.doc_generator import generate_technical_docs
from autodocify_cli.lib.generators.swagger_docs_generator import generate_swagger_docs
from autodocify_cli.lib.utils import check_llm

# Initialize the Typer app and console
app = typer.Typer()
console = Console()

# ASCII Art for the CLI header
ASCII_ART = """
 █████╗ ██████╗ ████████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██╗███████╗██╗   ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝ ██╔══██╗██║██╔════╝╚██╗ ██╔╝
███████║██████╔╝   ██║   ██║   ██║██████╔╝██║  ███╗██████╔╝██║█████╗   ╚████╔╝ 
██╔══██║██╔═══╝    ██║   ██║   ██║██╔═══╝ ██║   ██║██╔═══╝ ██║██╔══╝    ╚██╔╝  
██║  ██║██║        ██║   ╚██████╔╝██║     ╚██████╔╝██║     ██║███████╗   ██║   
╚═╝  ╚═╝╚═╝        ╚═╝    ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚═╝╚══════╝   ╚═╝   
"""


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidDirectoryError as e:
            console.print(f"❌ [bold red]Error:[/bold red] {e}")
        except GitError as e:
            console.print(f"❌ [bold red]Git Error:[/bold red] {e}")
        except AIGenerationError as e:
            console.print(f"❌ [bold red]AI Error:[/bold red] {e}")
        except AutoDocifyError as e:
            console.print(f"❌ [bold red]Unexpected AutoDocify Error:[/bold red] {e}")
        except Exception as e:
            console.print(f"❌ [bold red]Unexpected Error:[/bold red] {e}")

    return wrapper


def get_valid_project_files(base_dir: str) -> tuple:
    base_path = get_base_path(base_dir)
    project_files = get_project_files(base_path)
    if not project_files:
        console.print("❌ [red]No valid files found for the specified operation.[/red]")
        raise InvalidDirectoryError(
            "No valid files found for the specified operation.[/red]"
        )
    return base_path, project_files


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    AutoDocify CLI: Automate your README generation, Technical Document Generation, and testing workflows.
    """
    if ctx.invoked_subcommand is None:
        console.print(Text(ASCII_ART, style="bold yellow"))
        console.print(
            Panel(
                """
AutoDocify: Automate your README generation, testing workflows, and technical documentation.

[bold purple]Usage:[/bold purple]
  autodocify [bold yellow]<command>[/bold yellow] [options]

[bold purple]Commands:[/bold purple]
  greet              Greets the user.
  generate-readme    Generate a README.md using AI.
  generate-tests     Generate test files for your project.
  generate-docs      Generate technical documentation for your project.
  generate-swagger   Generate Swagger documentation for your project.
""",
                border_style="green",
            )
        )
        typer.echo(ctx.get_help())


@handle_exceptions
@app.command()
def greet(name: str = typer.Argument("COMRADE", help="Name of the user to greet")):
    """
    Greets the user with a friendly message.
    """
    console.print(f"[bold green]Hello, {name}! Welcome to AutoDocify.[/bold green]")


@handle_exceptions
@app.command()
def generate_readme(
    base_dir: str = typer.Argument(
        None,
        help="Path to the project directory. Defaults to the current working directory.",
    ),
    output_file: str = typer.Option("README.md", help="Name of the output README file"),
    llm: str = typer.Option(
        "gemini",
        help="Name of the language model to use. Supports openai|gemini|bard",
        callback=check_llm,
    ),
):
    """
    Generates a README.md file for the specified project.
    """
    base_path, project_files = get_valid_project_files(base_dir)
    generate_read_me(base_path, output_file, llm, project_files)


@handle_exceptions
@app.command()
def generate_tests(
    base_dir: str = typer.Argument(
        None,
        help="Path to the project directory. Defaults to the current working directory.",
    ),
    output_file: str = typer.Option("tests/test_main.py"),
    llm: str = typer.Option(
        "gemini",
        help="Name of the language model to use. Supports openai|gemini|bard",
        callback=check_llm,
    ),
):
    """
    Generates test files for the specified project.
    """
    base_path, project_files = get_valid_project_files(base_dir)
    with console.status(
        "[bold cyan]🤖 Generating test files...[/bold cyan]", spinner="dots2"
    ):
        generate_test_files(base_path, output_file, llm, project_files)


@handle_exceptions
@app.command()
def generate_docs(
    base_dir: str = typer.Argument(
        None,
        help="Path to the project directory. Defaults to the current working directory.",
    ),
    output_file: str = typer.Option(
        "DOCS.md", help="Name of the output technical documentation file"
    ),
    llm: str = typer.Option(
        "gemini",
        help="Name of the language model to use. Supports openai|gemini|bard",
        callback=check_llm,
    ),
):
    """
    Generates technical documentation for the specified project.
    """
    base_path, project_files = get_valid_project_files(base_dir)
    with console.status(
        "[bold cyan]🤖 Generating technical documentation...[/bold cyan]",
        spinner="line",
    ):
        generate_technical_docs(base_path, output_file, llm, project_files)


@handle_exceptions
@app.command()
def generate_swagger(
    base_dir: str = typer.Argument(
        None,
        help="Path to the project directory. Defaults to the current working directory.",
    ),
    output_file: str = typer.Option(
        "swagger.json", help="Name of the output Swagger documentation file"
    ),
    format: str = typer.Option(
        "json", help="The format of the Swagger docs. json|yaml"
    ),
    llm: str = typer.Option(
        "gemini",
        help="Name of the language model to use. Supports openai|gemini|bard",
        callback=check_llm,
    ),
):
    """
    Generates Swagger documentation for the specified project.
    """
    base_path, project_files = get_valid_project_files(base_dir)
    with console.status(
        "[bold cyan]🤖 Generating Swagger documentation...[/bold cyan]",
        spinner="bouncingBar",
    ):
        generate_swagger_docs(base_path, output_file, format, llm, project_files)


if __name__ == "__main__":
    app()
