"""Utility script to remove generated dependency directories.

Run this script from the project root to delete:
 - the top-level `venv` virtual environment directory
 - the `backend/__pycache__` directory
 - the `frontend/node_modules` directory
"""

from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def remove_directory(path: Path) -> None:
    """Delete the given directory tree if it exists."""

    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
            print(f"Removed: {path}")
        else:
            raise ValueError(f"Expected a directory at {path}, found non-directory.")
    else:
        print(f"Skipped (not found): {path}")


def main() -> None:
    targets = [
        PROJECT_ROOT / "venv",
        PROJECT_ROOT / "backend" / "__pycache__",
        PROJECT_ROOT / "frontend" / "node_modules",
    ]

    for target in targets:
        remove_directory(target)


if __name__ == "__main__":
    main()

