"""File and I/O utilities.

Provides safe file operations with encoding handling, atomic writes for data integrity,
checksum verification, and directory tree traversal.
"""

import os
import hashlib
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Union


class FileUtils:
    """Common file operations: read, write, checksums, atomic writes, tree walking."""

    @staticmethod
    def read_file(filepath: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read a text file with specified encoding.

        Args:
            filepath: Path to file.
            encoding: Text encoding (default: utf-8).

        Returns:
            File contents as string.

        Raises:
            FileNotFoundError: If file does not exist.
            UnicodeDecodeError: If encoding is incorrect.
        """
        return Path(filepath).read_text(encoding=encoding)

    @staticmethod
    def write_file(
        filepath: Union[str, Path], content: str, encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a text file, creating parent directories if needed.

        Args:
            filepath: Path to file.
            content: Content to write.
            encoding: Text encoding (default: utf-8).
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)

    @staticmethod
    def atomic_write(
        filepath: Union[str, Path], content: str, encoding: str = "utf-8"
    ) -> None:
        """
        Atomically write content to a file (write to temp, then rename).

        Prevents partial writes and ensures data integrity. Useful for config files,
        database exports, and other data that must not be corrupted on failure.

        Args:
            filepath: Path to file.
            content: Content to write.
            encoding: Text encoding (default: utf-8).
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file in same directory for atomic rename
        # (rename is atomic on POSIX systems when on same filesystem)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            dir=filepath.parent,
            delete=False,
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Atomic rename: all-or-nothing operation
        Path(tmp_path).replace(filepath)

    @staticmethod
    def checksum(filepath: Union[str, Path], algorithm: str = "sha256") -> str:
        """
        Calculate file checksum.

        Args:
            filepath: Path to file.
            algorithm: Hash algorithm ('md5', 'sha256', etc).

        Returns:
            Hex digest of file hash.
        """
        path = Path(filepath)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {filepath}")

        hasher = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    @staticmethod
    def walk_tree(
        root: Union[str, Path], pattern: Optional[str] = None
    ) -> list:
        """
        Walk directory tree and return list of all file paths.

        Args:
            root: Root directory to walk.
            pattern: Optional glob pattern to filter files (e.g., '*.py').

        Returns:
            List of Path objects for all files matching pattern.
        """
        root = Path(root)
        if pattern:
            return list(root.rglob(pattern))
        return [p for p in root.rglob("*") if p.is_file()]

    @staticmethod
    def safe_remove(filepath: Union[str, Path]) -> bool:
        """
        Safely remove a file, returning True if successful, False if not found.

        Args:
            filepath: Path to file.

        Returns:
            True if file was removed, False if not found.
        """
        path = Path(filepath)
        if path.exists():
            path.unlink()
            return True
        return False
