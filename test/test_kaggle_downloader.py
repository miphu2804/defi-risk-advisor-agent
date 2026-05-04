from pathlib import Path
from unittest.mock import patch

import pytest

from src.downloader.kaggle import KaggleDownloader


class TestKaggleDownloader:

    def test_empty_dataset_id_raises_error(self):
        downloader = KaggleDownloader()
        with pytest.raises(ValueError, match="dataset_id must not be empty"):
            downloader.download("", Path("/tmp"))

    def test_whitespace_dataset_id_raises_error(self):
        downloader = KaggleDownloader()
        with pytest.raises(ValueError, match="dataset_id must not be empty"):
            downloader.download("   ", Path("/tmp"))

    @patch("src.downloader.kaggle.kagglehub.dataset_download")
    def test_download_returns_path(self, mock_download):
        mock_download.return_value = "/fake/cache/path"
        downloader = KaggleDownloader()
        dest = Path("/tmp/test-dest")
        result = downloader.download("owner/dataset", dest)
        assert result == Path("/fake/cache/path")
        assert dest.exists()
        mock_download.assert_called_once_with("owner/dataset", output_dir=str(dest))
