"""
BASE_DIR.

Defines the base directory of the project.

Makes available the BASE_DIR and BASE_PATH variables.

BASE_DIR is a string containing the absolute path to the project's root directory.
BASE_PATH is a Path object containing the absolute path to the project's root directory.
"""

from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent.parent.parent

BASE_DIR = str(BASE_PATH)
