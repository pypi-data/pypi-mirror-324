import click
import logging
from pathlib import Path
from ai_kit.utils.env import load_environment
from ai_kit.config import CoreConfig
import warnings
from ai_kit.cli.commands.status import status_command
import sys
from rich.table import Table
import asyncio
from ai_kit.cli.registry import registry_instance
from ai_kit.cli.commands.init import init_command
from ai_kit import __version__  # Import version
from ai_kit.shared_console import shared_console, shared_error_console

# Configure basic logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Load environment variables
load_environment(CoreConfig.ROOT_DIR)
logger = logging.getLogger(__name__)

# Filter out warnings from internal dependencies
warnings.filterwarnings("ignore", module="pydantic.*")
warnings.filterwarnings("ignore", module="openai.*")


# ! MAIN COMMAND ===============================================
# This is the entry point for the CLI
@click.group(invoke_without_command=True)
@click.version_option(__version__, "--version", "-v", help="Show the version and exit.")
@click.pass_context
def main(ctx):
    """AI development toolkit for managing prompts and scripts."""
    # Handle no subcommand
    if ctx.invoked_subcommand is None:
        ctx.invoke(help)


# ! INIT COMMAND ===============================================
# This is the command for initializing the [ROOT_DIR] directory structure
# It copies over the template files and makes the index dir
@main.command()
@click.option(
    "--force", "-f", is_flag=True, help="Overwrite existing configuration and files"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    default="WARNING",
    help="Set logging level",
)
@registry_instance.add(
    name="init",
    description="Initialize a new .ai-kit directory structure with templates and search index.",
    usage="ai-kit init [--force] [--log-level LEVEL]",
)
def init(force: bool, log_level: str):
    """Initialize a new .ai-kit directory structure.

    Steps:
    1. Sets up logging based on --log-level
    2. Creates .ai-kit directory (or removes existing if --force)
    3. Copies template files for project structure
    4. Creates and initializes the search index
    5. Updates .gitignore to handle .ai-kit files (if confirmed)

    Options:
    --force, -f: Overwrite existing .ai-kit directory if it exists
    --log-level: Set logging level (DEBUG, INFO, WARNING, ERROR)
    """
    init_command(force=force, log_level=log_level)


# ! WEB COMMAND ===============================================
# These are the rest of the commands
# web, think (deepseek, return <think> only), find, reason, list/help or something
@click.argument("query")
@click.option(
    "--max-results",
    "-n",
    type=int,
    default=10,
    help="Maximum number of results to return",
)
@main.command()
@registry_instance.add(
    name="web",
    description="Search the web for information.",
    usage="ai-kit web <query> [--max-results <n>]",
)
def web(query: str, max_results: int):
    """Search the web for information."""
    from ai_kit.cli.commands.web import search_web

    try:
        results = search_web(query, max_results)
    except Exception as e:
        shared_error_console.print(f"[red]Error searching web: {e}[/red]")
        sys.exit(1)

    # Create and configure the table
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Title", style="cyan", no_wrap=False)
    table.add_column("Link", style="blue")
    table.add_column("Snippet", style="green", no_wrap=False)

    # Add rows to the table
    for result in results:
        table.add_row(
            result.get("title", "N/A"),
            result.get("link", "N/A"),
            result.get("snippet", "N/A"),
        )

    # Print the table
    shared_console.print(table)


# ! SEARCH COMMAND ===============================================
@click.argument("query")
@click.option(
    "--max-results",
    "-n",
    type=int,
    default=10,
    help="Maximum number of results to return",
)
@main.command()
@registry_instance.add(
    name="search",
    description="Search through indexed files in your workspace.",
    usage="ai-kit search <query> [--max-results <n>]",
)
def search(query: str, max_results: int):
    """Search through indexed files."""
    from ai_kit.cli.commands.search import search_command

    try:
        asyncio.run(search_command(query, max_results))
    except Exception as e:
        shared_error_console.print(f"[red]Error searching index: {e}[/red]")
        sys.exit(1)


# ! REASON COMMAND ===============================================
@click.argument("prompt")
@click.option(
    "--model", "-m", type=str, default="o1", help="Model to use for reasoning"
)
@main.command()
@registry_instance.add(
    name="reason",
    description="Consult with a smart AI designed to perform reasoning. You can pass {{ filepath }} in the prompt to reference files in the codebase.",
    usage="ai-kit reason [--model <model>] <prompt> ",
)
async def reason(prompt: str, model: str):
    """Reason about the prompt."""
    from ai_kit.cli.commands.reason import reason_command

    try:
        asyncio.run(reason_command(prompt, model))
    except Exception as e:
        shared_error_console.print(f"[red]Error reasoning: {e}[/red]")
        sys.exit(1)


# ! THINK COMMAND ===============================================
@click.argument("prompt")
@click.option(
    "--model",
    "-m",
    type=str,
    default="o3-mini",
    help="Model to use for thinking",
)
@main.command()
@registry_instance.add(
    name="think",
    description="Access your brain. If the request is complex enough, this will call on a smar AI to generate a thought stream. Otherwise it will return back to you. You can pass {{ filepath }} in the prompt to reference files and directories in the codebase.",
    usage="ai-kit think <prompt> [--model <model>]",
)
def think(prompt: str, model: str):
    """Think about the prompt."""
    from ai_kit.cli.commands.think import think_command

    if not Path(CoreConfig.ROOT_DIR).exists():
        shared_console.print(
            "[red]AI Kit is not initialized. Run `ai-kit init` first.[/red]"
        )
        return

    try:
        asyncio.run(think_command(prompt, model))
    except Exception as e:
        shared_error_console.print(f"[red]Error thinking: {e}[/red]")
        sys.exit(1)


# ! HELP COMMAND ===============================================
@main.command()
@registry_instance.add(
    name="help",
    description="Show help information.",
    usage="ai-kit help",
)
def help():
    """Show help information."""
    shared_console.print(
        "\n[bold cyan]AI Kit - The first CLI designed for AI agents[/bold cyan]\n"
    )

    # Show version
    shared_console.print(f"[bold]Version:[/bold] {__version__}\n")

    # Show available commands
    shared_console.print("[bold]Available Commands:[/bold]")
    registry_instance.display_commands()

    # Show initialization hint
    shared_console.print("\n[bold yellow]Getting Started:[/bold yellow]")
    shared_console.print("1. Initialize AI Kit in your project:")
    shared_console.print("   ai-kit init")
    shared_console.print("\n2. Try the think command:")
    shared_console.print('   ai-kit think "What files are in this project?"')

    # Show more info
    shared_console.print("\n[bold]For more information:[/bold]")
    shared_console.print("- Use --help with any command for detailed usage")

    shared_console.print("- Visit https://www.ai-kit.dev/docs/ for docs")


# ! STATUS COMMAND ===============================================
@main.command()
@registry_instance.add(
    name="status",
    description="Show status information.",
    usage="ai-kit status",
)
def status():
    """Show status information."""
    status_command()


# ! LIST COMMAND ===============================================
# This is the command for listing all commands so every command is registered
@main.command()
@registry_instance.add(
    name="list",
    description="List all commands.",
    usage="ai-kit list.",
)
def list():
    """List all commands."""
    registry_instance.display_commands()
