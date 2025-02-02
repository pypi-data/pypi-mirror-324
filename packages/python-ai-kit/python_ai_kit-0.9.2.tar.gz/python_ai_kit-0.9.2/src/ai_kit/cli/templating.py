import importlib.resources
import shutil
from pathlib import Path
from ..config import CoreConfig
from ..utils.fs import package_root, find_workspace_root
from ai_kit.shared_console import shared_console

def copy_dir(source_dir: Path, dest_dir: Path, ignore_dirs: set[str] = None) -> None:
    """Copy directory to the destination directory.
    
    Args:
        source_dir: Source directory path
        dest_dir: Destination directory path
        ignore_dirs: Set of directory names to skip copying
    """
    if not source_dir.is_dir():
        return
    
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)

    # Handle root .gitignore first
    gitignore_template = source_dir / '.gitignore'
    if gitignore_template.exists():
        # Use the parent of dest_dir (the repo root) for .gitignore
        handle_gitignore(gitignore_template, Path('.gitignore'))

    # Copy every file/subdirectory in source_dir to dest_dir
    for item in source_dir.iterdir():
        # Skip directories in ignore_dirs
        if ignore_dirs and item.is_dir() and item.name in ignore_dirs:
            continue
            
        if item.is_file():
            # Skip .gitignore since we handled it separately
            if item.name != '.gitignore':
                shutil.copy2(item, dest_dir / item.name)
        elif item.is_dir():
            # Create directory if it doesn't exist (for when we're keeping index dirs)
            target_dir = dest_dir / item.name
            if not target_dir.exists():
                shutil.copytree(item, target_dir)

    # Ensure the chats directory exists in .ai-kit
    chats_dir = dest_dir / "chats"
    if not chats_dir.exists():
        chats_dir.mkdir(parents=True, exist_ok=True)
        shared_console.print(f"[green]✓ Created chats directory at {chats_dir}[/green]")

    shared_console.print(f"[green]✓ Created directory {CoreConfig.ROOT_DIR}[/green]")

def handle_gitignore(source: Path, dest: Path) -> None:
    """Handle .gitignore file copying with special merge logic."""
    # Read source content
    source_content = source.read_text().splitlines()
    
    # If destination doesn't exist, just copy the source
    if not dest.exists():
        dest.write_text('\n'.join(source_content) + '\n')
        shared_console.print("[green]✓ Created .gitignore file[/green]")
        return
        
    # Read existing content
    dest_content = dest.read_text().splitlines()
    
    # Add our entries if they don't exist
    added = False
    for line in source_content:
        if line and line not in dest_content:
            if not added:
                # Add a blank line and comment if this is our first addition
                if dest_content and dest_content[-1] != '':
                    dest_content.append('')
                dest_content.append('# Added by AI Kit')
                added = True
            dest_content.append(line)
    
    # Write back if we made changes
    if added:
        dest.write_text('\n'.join(dest_content) + '\n')
        shared_console.print("[green]✓ Updated .gitignore file[/green]")

def handle_cursorrules(source: Path, dest: Path) -> None:
    """Handle cursorrules.md file copying with special merge logic."""
    # Read source content
    source_content = source.read_text().splitlines()
    
    # If destination doesn't exist, just copy the source
    if not dest.exists():
        dest.write_text('\n'.join(source_content) + '\n')
        shared_console.print("[green]✓ Created cursorrules.md file[/green]")
        return
        
    # Read existing content
    dest_content = dest.read_text().splitlines()
    
    # Add our entries if they don't exist
    added = False
    for line in source_content:
        if line and line not in dest_content:
            if not added:
                # Add a blank line and comment if this is our first addition
                if dest_content and dest_content[-1] != '':
                    dest_content.append('')
                dest_content.append('# Added by AI Kit')
                added = True
            dest_content.append(line)
    
    # Write back if we made changes
    if added:
        dest.write_text('\n'.join(dest_content) + '\n')
        shared_console.print("[green]✓ Updated cursorrules.md file[/green]")
