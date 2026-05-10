import argparse
import logging

from src.app_config import app_config
from src.downloader.kaggle import KaggleDownloader
from src.utils import get_data_path

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s"
    )

    parser = argparse.ArgumentParser(description="Download dataset from Kaggle")
    parser.add_argument(
        "--dataset", default=None, help="Kaggle dataset identifier (owner/name)"
    )
    parser.add_argument(
        "--dest", default="raw", help="Destination directory under data/"
    )
    args = parser.parse_args()

    dataset = args.dataset or app_config.DATASET_NAME

    downloader = KaggleDownloader()
    dest = get_data_path(args.dest)
    result = downloader.download(dataset, dest, app_config.DATASET_FILE)
    logger.info("Done: %s", result)


if __name__ == "__main__":
    main()
