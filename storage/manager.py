import os
import hashlib
from typing import Dict, List
from .models import FileSystemItem

class FileStorageManager:
    def __init__(self, base_path: str):
        self.base_path = os.path.abspath(base_path)

    def _generate_id(self, path: str) -> str:
        """Generate a unique ID for a file/folder based on its path"""
        return hashlib.md5(path.encode()).hexdigest()[:12]

    def scan_directory(self) -> Dict[str, FileSystemItem]:
        items: Dict[str, FileSystemItem] = {}
        
        for root, dirs, files in os.walk(self.base_path):
            # Process current directory
            if root != self.base_path:  # Skip base directory itself
                dir_id = self._generate_id(root)
                # Only set parent_id if not directly under base path
                parent_dir = os.path.dirname(root)
                parent_id = self._generate_id(parent_dir) if parent_dir != self.base_path else None
                items[dir_id] = FileSystemItem.from_path(
                    self.base_path, root, dir_id, parent_id
                )

            # Process files in current directory
            for file in files:
                full_path = os.path.join(root, file)
                file_id = self._generate_id(full_path)
                parent_id = None if root == self.base_path else self._generate_id(root)
                items[file_id] = FileSystemItem.from_path(
                    self.base_path, full_path, file_id, parent_id
                )

        return items

    def get_structure(self) -> Dict:
        """Returns a JSON-serializable structure of the file system"""
        items = self.scan_directory()
        return {
            'items': list(items.values()),
            'total': len(items)
        }
