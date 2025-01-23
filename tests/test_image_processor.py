import pytest
from app.core.image_processor import get_image_files, process_image

def test_get_image_files():
    test_folder = "tests/test_data"
    files = get_image_files(test_folder)
    assert len(files) > 0
    assert all(f.endswith(('.jpg', '.jpeg', '.png')) for f in files)

def test_process_image(test_image_path):
    result = process_image(test_image_path, "test_key")
    assert isinstance(result, dict)