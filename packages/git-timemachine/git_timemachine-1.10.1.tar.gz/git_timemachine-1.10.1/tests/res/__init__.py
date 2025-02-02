import os.path
import tarfile
import tempfile

from pygit2 import discover_repository, Repository  # pylint: disable=no-name-in-module


def _extract_repo(archive_file: str) -> Repository:
    target_dir = tempfile.mkdtemp()

    with tarfile.open(archive_file) as file:
        file.extractall(target_dir)

    return Repository(discover_repository(target_dir))


def extract_empty_repo() -> Repository:
    return _extract_repo(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'empty-repo.tar.gz'))


def extract_nonempty_repo() -> Repository:
    return _extract_repo(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nonempty-repo.tar.gz'))
