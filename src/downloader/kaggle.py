import logging
from pathlib import Path

import kagglehub


class KaggleDownloader:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def download(
        self, dataset_id: str, destination: Path, dataset_file: str = ""
    ) -> Path:
        if not dataset_id.strip():
            raise ValueError("dataset_id must not be empty")
        self.logger.info("Downloading %s to %s", dataset_id, destination)
        destination.mkdir(parents=True, exist_ok=True)
        kwargs: dict[str, str | bool] = {"output_dir": str(destination)}
        if dataset_file:
            kwargs["path"] = dataset_file
        path = Path(kagglehub.dataset_download(dataset_id, **kwargs))
        self.logger.info("Downloaded to %s", path)
        return path
