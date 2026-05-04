import logging
from pathlib import Path

import kagglehub


class KaggleDownloader:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def download(self, dataset_id: str, dest: Path) -> Path:
        if not dataset_id.strip():
            raise ValueError("dataset_id must not be empty")
        self.logger.info("Downloading %s to %s", dataset_id, dest)
        dest.mkdir(parents=True, exist_ok=True)
        path = Path(kagglehub.dataset_download(dataset_id, output_dir=str(dest)))
        self.logger.info("Downloaded to %s", path)
        return path
