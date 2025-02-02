"""Utilities for handling prompts and file references."""
import re
from pathlib import Path
from .fs import load_file_content, WorkspaceError, join_workspace_path
from ..config import CoreConfig

def process_file_references(text: str) -> str:
    """Replace {{filename}} references with file contents.
    
    Args:
        text: Text containing {{filename}} references to files in the workspace.
              The filename can contain optional whitespace, which will be stripped.
              Example: "{{file.py}}", "{{  file.py  }}", "{{ file.py}}"
              If a directory is referenced, all files within it (recursively) will be included.
              Only files with extensions in CoreConfig.SUPPORTED_FILE_EXTENSIONS will be processed.
        
    Returns:
        Text with file references replaced by their contents, wrapped in markers.
        If a file cannot be loaded, includes an error message instead of the content.
        For directories, includes the content of all supported files within, each wrapped in markers.
        Files with unsupported extensions will be skipped with an error message.
    """
    def replace_match(match):
        filepath = match.group(1).strip()
        try:
            full_path = join_workspace_path(filepath)
            if full_path.is_dir():
                contents = []
                workspace_root = join_workspace_path()
                for child_path in full_path.rglob('*'):
                    if child_path.is_file() and child_path.suffix in CoreConfig.SUPPORTED_FILE_EXTENSIONS:
                        child_rel_path = child_path.relative_to(workspace_root)
                        content = load_file_content(str(child_rel_path))
                        contents.append(f"\n=== Content of {child_rel_path} ===\n{content}\n=== End of {child_rel_path} ===\n")
                return ''.join(contents)
            else:
                # Check if the file has a supported extension
                # if full_path.suffix not in CoreConfig.SUPPORTED_FILE_EXTENSIONS:
                    # raise WorkspaceError(f"\nError loading {filepath} in process_file_references: File extension {full_path.suffix} is not supported. Supported extensions: {CoreConfig.SUPPORTED_FILE_EXTENSIONS}\n")
                content = load_file_content(filepath)
                return f"\n=== Content of {filepath} ===\n{content}\n=== End of {filepath} ===\n"
        except WorkspaceError as e:
            raise WorkspaceError(f"\nError loading {filepath} in process_file_references: {str(e)}")
        except Exception as e:
            raise Exception(f"\nError processing {filepath} in process_file_references: {str(e)}")
    
    return re.sub(r'\{\{(.+?)\}\}', replace_match, text)

def load_prompt(path: str) -> str:
    with open(path, "r") as file:
        return file.read()