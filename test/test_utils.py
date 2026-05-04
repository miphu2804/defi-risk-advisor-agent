from pathlib import Path

from src.utils import get_data_path, get_file_path, get_project_path, get_project_root


class TestUtils:
    """Test utility path helpers using pytest."""

    def test_get_project_root(self):
        expected_root = Path(__file__).resolve().parent.parent
        assert get_project_root() == expected_root

    def test_get_project_path(self):
        expected_path = (
            Path(__file__).resolve().parent.parent / "data" / "raw" / "sample.csv"
        )
        assert get_project_path("data", "raw", "sample.csv") == expected_path

    def test_get_data_path(self):
        expected_path = (
            Path(__file__).resolve().parent.parent / "data" / "raw" / "sample.csv"
        )
        assert get_data_path("raw", "sample.csv") == expected_path

    def test_get_file_path(self):
        assert get_file_path("sample.csv") == Path("sample.csv")
