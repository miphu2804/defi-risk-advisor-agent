from pathlib import Path


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


def get_project_path(*parts: str) -> Path:
    """Join path parts under the project root."""
    return get_project_root().joinpath(*parts)


def get_data_path(*parts: str) -> Path:
    """Get a path inside the project's data directory."""
    return get_project_path("data", *parts)


def get_file_path(filename: str) -> Path:
    """Convert a filename into a Path object."""
    return Path(filename)
