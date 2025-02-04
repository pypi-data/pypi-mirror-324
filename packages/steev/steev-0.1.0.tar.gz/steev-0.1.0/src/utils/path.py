from pathlib import Path
from time import time

from src.settings import LOCAL_DIR


def check_local_dir() -> bool:
    return LOCAL_DIR.exists()


def create_local_dir() -> None:
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)


def get_base_dir(file_path: str) -> str | Path | None:
    """
    Get the base directory of the file.
    """
    return Path(file_path).parent


class TempFile:
    """Temporary file that will be deleted when the object is deleted

    Usage:
    Example 1
    >>> with TempFile() as file:
    >>>     file.write("Hello, world!")

    Example 2
    >>> file = TempFile()
    >>> file.write("Hello, world!")
    >>> file.close()
    """

    def __init__(self, dir: str | Path = "."):
        self.dir = dir if isinstance(dir, Path) else Path(dir)
        self.file_path = self.dir.joinpath(_generate_filename())
        self._file = open(self.file_path, "w")

    def write(self, content: str) -> None:
        self._file.write(content)

    def flush(self) -> None:
        self._file.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        self.file_path.unlink(missing_ok=True)

    def __del__(self):
        self._file.close()
        self.file_path.unlink(missing_ok=True)


def _generate_filename() -> str:
    return f"tmp_{int(time())}.py"
