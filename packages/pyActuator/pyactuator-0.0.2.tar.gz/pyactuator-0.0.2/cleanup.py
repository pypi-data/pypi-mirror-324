import os
import shutil
from pathlib import Path

def cleanup():
    """Clean up build artifacts and temporary files."""
    # Get the root directory (where this script is located)
    root_dir = Path(__file__).parent

    # Directories to remove
    dirs_to_remove = [
        "build",
        "dist",
        "*.egg-info",
        "__pycache__",
        "pyActuator/__pycache__",
        "pyActuator/*.pyd",
        "pyActuator/*.so",
        "pyActuator/*.pyi",
        "pyActuator/*.dll",
        "pyActuator/*.dylib",
    ]

    # Files to remove
    files_to_remove = [
        "pyActuator/*.pyc",
        ".coverage",
        "coverage.xml",
        ".pytest_cache",
    ]

    def remove_matching_items(patterns):
        for pattern in patterns:
            paths = root_dir.glob(pattern)
            for path in paths:
                try:
                    if path.is_file():
                        path.unlink()
                        print(f"Removed file: {path}")
                    elif path.is_dir():
                        shutil.rmtree(path)
                        print(f"Removed directory: {path}")
                except Exception as e:
                    print(f"Error removing {path}: {e}")

    print("Cleaning up build artifacts...")
    remove_matching_items(dirs_to_remove)
    remove_matching_items(files_to_remove)
    print("Cleanup complete!")

if __name__ == "__main__":
    cleanup()