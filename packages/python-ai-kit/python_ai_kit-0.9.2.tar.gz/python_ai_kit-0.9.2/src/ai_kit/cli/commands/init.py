from pathlib import Path
import sys
import logging
from rich.console import Console
from rich.prompt import Confirm
from ai_kit.utils.fs import package_root, find_workspace_root, remove_tree
from ai_kit.config import CoreConfig
from ai_kit.cli.templating import copy_dir, handle_cursorrules

console_instance = Console()
error_console_instance = Console(stderr=True)


def init_command(force: bool, log_level: str):
    """Implementation of the init command logic."""
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    print("Set logging level to", log_level)

    ROOT_DIR = Path(CoreConfig.ROOT_DIR)  # path to the dir we're gonna create

    # ! Check if directory exists and handle force
    if ROOT_DIR.exists():
        if force:
            # Check for existing index data
            files_dir = ROOT_DIR / CoreConfig.INDEX_DIR
            has_index = (files_dir.exists() and any(files_dir.iterdir()))
            
            if has_index:
                reset_index = Confirm.ask(
                    "[bold yellow]Files in the index directory exist. Do you want to overwrite them?[/bold yellow]",
                    default=False
                )
                if reset_index:
                    # User wants to reset everything
                    try:
                        remove_tree(ROOT_DIR)
                        console_instance.print(
                            f"[yellow]Reset all files (including index) in {ROOT_DIR}[/yellow]"
                        )
                    except Exception as e:
                        error_console_instance.print(
                            f"[red]Error removing directory: {e}[/red]"
                        )
                        sys.exit(1)
                else:
                    # Keep index data, remove everything else
                    console_instance.print("[yellow]Keeping existing index files[/yellow]")
                    try:
                        for item in ROOT_DIR.iterdir():
                            if item != files_dir:
                                if item.is_dir():
                                    remove_tree(item)
                                else:
                                    item.unlink()
                    except Exception as e:
                        error_console_instance.print(
                            f"[red]Error updating directory structure: {e}[/red]"
                        )
                        sys.exit(1)
            else:
                # No index data, just remove everything
                try:
                    remove_tree(ROOT_DIR)
                    console_instance.print(
                        f"[yellow]Removed existing {ROOT_DIR} directory[/yellow]"
                    )
                except Exception as e:
                    error_console_instance.print(
                        f"[red]Error removing directory: {e}[/red]"
                    )
                    sys.exit(1)
        else:
            error_console_instance.print(
                f"[bold yellow]{ROOT_DIR} directory already exists.[/bold yellow]\n"
                "[yellow]Use --force to overwrite existing files. If index files exist, you'll be asked whether to reset them.[/yellow]"
            )
            sys.exit(1)

    pkg_root = package_root()

    # ! Copy over the template files
    try:
        # If we're keeping index directories, ignore them during copy
        ignore_dirs = None
        if force and ROOT_DIR.exists():
            files_dir = ROOT_DIR / CoreConfig.INDEX_DIR
            if files_dir.exists():
                ignore_dirs = {CoreConfig.INDEX_DIR}
        
        # copy files over to root dir
        copy_dir(
            pkg_root / ".template", 
            ROOT_DIR,
            ignore_dirs=ignore_dirs
        )
        console_instance.print(
            "[green]✓ Initialized directory structure in .ai-kit[/green]"
        )
    except Exception as e:
        error_console_instance.print(f"[red]Error copying template files: {e}[/red]")
        sys.exit(1)

    # Handle .gitignore update with interactive prompt
    gitignore_path = Path(".gitignore")
    ai_kit_ignore_line = f"{CoreConfig.ROOT_DIR}/"
    
    # Check if .gitignore exists and if ROOT_DIR is already ignored
    already_ignored = False
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r") as f:
                content = f.read()
                if ai_kit_ignore_line in content:
                    already_ignored = True
                    console_instance.print(
                        f"[green]✓ {CoreConfig.ROOT_DIR} is already ignored in .gitignore[/green]"
                    )
        except Exception as e:
            # If we can't read the file, we'll assume it's not ignored and show the prompt
            error_console_instance.print(f"[yellow]Warning: Could not read .gitignore: {e}[/yellow]")
    
    if not already_ignored:
        update_gitignore = Confirm.ask("[bold yellow]Would you like to update .gitignore to ignore the .ai-kit directory?[/bold yellow]", default=True)
        
        if update_gitignore:
            comment_line = "# Added by ai-kit - ignoring AI Kit directory"
            
            try:
                # Create or update .gitignore
                if gitignore_path.exists():
                    with open(gitignore_path, "a") as f:
                        f.write(f"\n{comment_line}\n{ai_kit_ignore_line}\n")
                else:
                    with open(gitignore_path, "w") as f:
                        f.write(f"{comment_line}\n{ai_kit_ignore_line}\n")
                
                console_instance.print(
                    "[green]✓ Updated .gitignore[/green]"
                )
            except Exception as e:
                error_console_instance.print(f"[yellow]Warning: Could not update .gitignore: {e}[/yellow]")

    # Handle cursorrules.md update with interactive prompt
    cursorrules_path = find_workspace_root() / ".cursorrules"
    cursorrules_source = Path(package_root()) / "system_prompts" / "cursorrules.md"
    
    # Check if cursorrules exists and has content
    already_has_rules = False
    if not already_has_rules and cursorrules_source.exists():
        update_cursorrules = Confirm.ask(
            "[bold yellow]Would you like to create/update cursorrules.md with default rules?[/bold yellow]",
            default=True
        )
        
        if update_cursorrules:
            try:
                handle_cursorrules(cursorrules_source, cursorrules_path)
            except Exception as e:
                error_console_instance.print(f"[yellow]Warning: Could not update cursorrules.md: {e}[/yellow]")

    console_instance.print(
        "\n[bold green]✨ AI Kit initialization complete![/bold green]"
    )
