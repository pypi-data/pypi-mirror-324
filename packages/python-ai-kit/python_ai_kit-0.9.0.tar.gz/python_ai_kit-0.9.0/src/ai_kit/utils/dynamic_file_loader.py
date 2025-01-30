import os
import mimetypes
from pypdf import PdfReader
from typing import Optional, Callable, Dict

try:
    import magic
except ImportError:
    magic = None


class DynamicFileLoader:
    def __init__(self):
        self.loader_registry: Dict[str, Callable] = {}
        self.extension_registry: Dict[str, Callable] = {}
        self.default_loader: Optional[Callable] = None

        # Register default loaders
        self.register_loader(
            extensions=[".pdf"], mime_types=["application/pdf"], loader=self._load_pdf
        )
        self.register_loader(mime_types=["text/plain"], loader=self._load_text)

    def register_loader(
        self,
        extensions: Optional[list] = None,
        mime_types: Optional[list] = None,
        loader: Optional[Callable] = None,
    ):
        if extensions:
            for ext in extensions:
                self.extension_registry[ext.lower()] = loader
        if mime_types:
            for mime in mime_types:
                self.loader_registry[mime.lower()] = loader

    def load_file_content(self, file_path: str) -> str:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Try extension-based loading first
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.extension_registry:
            return self.extension_registry[ext](file_path)

        # Fall back to MIME-type-based loading
        mime_type = self._get_mime_type(file_path)
        if mime_type in self.loader_registry:
            return self.loader_registry[mime_type](file_path)

        # Try default loader if set
        if self.default_loader:
            return self.default_loader(file_path)

        raise ValueError(
            f"No loader available for {file_path} (MIME: {mime_type}, Extension: {ext})"
        )

    def _get_mime_type(self, file_path: str) -> str:
        # First try mimetypes based on extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type.lower()

        # Fall back to magic for content-based detection
        if not magic:
            raise ImportError(
                "The 'python-magic' package is required for MIME type detection. "
                "Install with 'pip install python-magic'."
            )

        mime = magic.Magic(mime=True)
        with open(file_path, "rb") as f:
            file_content = f.read(2048)
            return mime.from_buffer(file_content).lower()

    def set_default_loader(self, loader: Callable):
        self.default_loader = loader

    @staticmethod
    def _load_pdf(file_path: str) -> str:
        text = []
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text())
        return "\n".join(text)

    @staticmethod
    def _load_text(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()