import os
import pytest
from src.utils import get_python_files

def test_get_python_files_with_single_file(tmp_path):
    """
    Tests that the function returns the correct path when given a single file.
    """
    py_file = tmp_path / "test.py"
    py_file.touch()
    
    found_files = get_python_files(str(py_file))
    
    assert len(found_files) == 1
    assert str(py_file) in found_files

def test_get_python_files_in_directory(tmp_path):
    """
    Tests that the function finds all Python files in a directory
    and ignores other file types.
    """
    (tmp_path / "test1.py").touch()
    (tmp_path / "test2.py").touch()
    (tmp_path / "data.txt").touch()
    
    found_files = get_python_files(str(tmp_path))
    
    assert len(found_files) == 2
    assert str(tmp_path / "test1.py") in found_files
    assert str(tmp_path / "test2.py") in found_files

def test_get_python_files_respects_gitignore(tmp_path):
    """
    Tests that the function correctly ignores files and directories
    listed in a .gitignore file.
    """
    (tmp_path / "main.py").touch()
    
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "ignored.py").touch()
    
    (tmp_path / "ignored_by_rule.py").touch()

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("venv/\nignored_by_rule.py")

    found_files = get_python_files(str(tmp_path))
    
    assert len(found_files) == 1
    assert str(tmp_path / "main.py") in found_files
    assert str(venv_dir / "ignored.py") not in found_files
    assert str(tmp_path / "ignored_by_rule.py") not in found_files