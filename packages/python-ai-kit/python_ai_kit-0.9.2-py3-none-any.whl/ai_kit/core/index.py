import os
import json
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from time import perf_counter
from rich.table import Table
from rich.progress import track

from ai_kit.config import CoreConfig
from ai_kit.core.upstash_client import UpstashVectorStore
from ai_kit.utils.dynamic_file_loader import DynamicFileLoader
from ai_kit.shared_console import shared_console

logger = logging.getLogger(__name__)

def sliding_window_chunker(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def crawl_dir(dir_path: str, supported_extensions: List[str]) -> List[tuple[str, str]]:
    paths = []
    dir_path = os.path.abspath(dir_path)
    for root, _, files in os.walk(dir_path):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in supported_extensions):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dir_path)
                paths.append((abs_path, rel_path))
    return paths

class Index:
    """Manages file indexing and searching."""

    def __init__(self):
        """Initialize the Index."""
        self.vector_store = UpstashVectorStore()
        self.file_loader = DynamicFileLoader()
        
        # Create root directory if it doesn't exist
        os.makedirs(CoreConfig.ROOT_DIR, exist_ok=True)
        
        # File paths
        self.root_dir = Path(CoreConfig.ROOT_DIR)
        self.text_dir = self.root_dir / CoreConfig.INDEX_DIR
        self.hashes_file = self.root_dir / "file_hashes.json"
        
        self.supported_extensions = CoreConfig.SUPPORTED_FILE_EXTENSIONS
        self.max_paragraph_size = 1000
        
        # Create text directory if it doesn't exist
        os.makedirs(self.text_dir, exist_ok=True)
        
        logger.info("Index initialized")

    def _get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file."""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _load_hashes(self) -> Dict[str, str]:
        """Load stored file hashes."""
        if self.hashes_file.exists():
            with open(self.hashes_file) as f:
                return json.load(f)
        return {}

    def _save_hashes(self, hashes: Dict[str, str]):
        """Save file hashes."""
        with open(self.hashes_file, "w") as f:
            json.dump(hashes, f, indent=2)

    def get_file_content(self, filename: str, file_hash: str) -> Optional[str]:
        """Get file content if it exists and hash matches."""
        file_path = self.text_dir / filename
        if not file_path.exists():
            return None
        
        current_hash = self._get_file_hash(file_path)
        if current_hash != file_hash:
            return None
            
        return self.file_loader.load_file_content(file_path)

    async def reindex_texts(self):
        t0 = perf_counter()

        # Get current files and load stored hashes
        files = crawl_dir(self.text_dir, self.supported_extensions)
        stored_hashes = self._load_hashes()
        current_hashes = {}
        
        # Track what needs updating
        all_chunks = []
        all_metadata = []
        all_ids = []
        updated_files = []

        # Check each file
        for abs_path, rel_path in files:
            current_hash = self._get_file_hash(abs_path)
            current_hashes[rel_path] = current_hash
            
            # Skip if file hasn't changed
            if rel_path in stored_hashes and stored_hashes[rel_path] == current_hash:
                continue
                
            # File is new or modified
            updated_files.append(rel_path)
            try:
                text_data = self.file_loader.load_file_content(abs_path)
                chunks = sliding_window_chunker(text_data, self.max_paragraph_size)
                
                for chunk_index, chunk_text in enumerate(chunks):
                    all_chunks.append(chunk_text)
                    all_metadata.append({
                        "filename": os.path.basename(abs_path),
                        "rel_path": rel_path,
                        "file_hash": current_hash,  # Only store file info in metadata
                    })
                    all_ids.append(f"{current_hash}-{chunk_index}")  # Create unique ID per chunk
            except Exception as e:
                shared_console.print(f"[yellow]Skipping file {rel_path}: {str(e)}[/yellow]")
                continue

        # Clean up old vectors
        hashes_to_delete = set(stored_hashes.values()) - set(current_hashes.values())
        if hashes_to_delete:
            t_delete = perf_counter()
            deleted_count = await self.vector_store.delete_vectors(list(hashes_to_delete))
            delete_elapsed = perf_counter() - t_delete
            shared_console.print(f"[yellow]Cleaned up {deleted_count} old vectors in {delete_elapsed:.2f}s[/yellow]")

        # Update vector store if we have new content
        if all_chunks:
            t_index = perf_counter()
            shared_console.status("[bold cyan]Indexing new/modified files...[/bold cyan]")
            await self.vector_store.add_to_vector_store(all_chunks, all_metadata, all_ids)
            index_elapsed = perf_counter() - t_index
            elapsed = perf_counter() - t0
                
            # Show updated files in a table
            if updated_files:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Updated Files", style="cyan")
                for file in updated_files:
                    table.add_row(file)
                shared_console.print(table)
            
            shared_console.print(f"[green]✓ Indexed {len(updated_files)} new/modified files with {len(all_chunks)} chunks[/green]")
            shared_console.print(f"[green]  • Indexing time: {index_elapsed:.2f}s[/green]")
            shared_console.print(f"[green]  • Total time: {elapsed:.2f}s[/green]")
        else:
            elapsed = perf_counter() - t0
            shared_console.print(f"[green]✓ No changes detected[/green]")
            shared_console.print(f"[green]  • Checked {len(files)} files in {elapsed:.2f}s[/green]")

        # Save new hashes
        self._save_hashes(current_hashes)

    async def search(self, query: str, max_results: int = 5, silent: bool = False, load_full_content: bool = False) -> List[Dict[str, Any]]:
        s = perf_counter()
        
        # Check for new/modified files
        with shared_console.status("[bold cyan]Checking for file changes...[/bold cyan]") as status:
            await self.reindex_texts()

        # Get embeddings and search
        with shared_console.status("[bold cyan]Searching...[/bold cyan]") as status:
            query_emb = await self.vector_store.embedding_client.create_embeddings(query)
            results = self.vector_store.query(query_emb[0], k=max_results)

        # Format results
        formatted_results = []
        for res in results:
            result = {
                "filename": res.metadata.get("filename", "unknown"),
                "chunk_text": res.data,  # Get chunk text from data field
                "score": res.score,
                "rel_path": res.metadata.get("rel_path", "unknown"),
                "file_hash": res.metadata.get("file_hash"),
            }
            
            # Optionally load full file content
            if load_full_content and result["file_hash"]:
                result["full_content"] = self.get_file_content(
                    result["rel_path"],  # Use rel_path instead of filename
                    result["file_hash"]
                )
            
            formatted_results.append(result)

        # Display results
        if not silent:
            duration = perf_counter() - s
            if formatted_results:
                shared_console.print(f"\n[bold cyan]Search results for:[/bold cyan] [yellow]{query}[/yellow]")
                shared_console.print(f"[yellow]Search completed in {duration:.2f}s[/yellow]")
                
                table = Table(show_header=True, header_style="bold magenta", show_lines=True)
                table.add_column("File", style="cyan", no_wrap=True)
                table.add_column("Score", style="green", justify="right", width=10)
                table.add_column("Snippet", style="white")
                
                for r in formatted_results:
                    table.add_row(
                        r["rel_path"],
                        f"{r['score']:.3f}",
                        r["chunk_text"][:200] + "..."
                    )
                shared_console.print(table)
            else:
                shared_console.print("[yellow]No results found[/yellow]")
                shared_console.print(f"[yellow]Search completed in {duration:.2f}s[/yellow]")

        return formatted_results
