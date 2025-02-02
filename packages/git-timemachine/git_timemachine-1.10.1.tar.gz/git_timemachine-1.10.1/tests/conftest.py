import shutil
import tarfile
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from pygit2 import discover_repository, Repository  # pylint: disable=no-name-in-module


@pytest.fixture(scope='module')
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope='function')
def empty_repo() -> Repository:
    path = tempfile.mkdtemp()
    with tarfile.open(Path(__file__).parent.joinpath('res', 'empty-repo.tar.gz')) as file:
        file.extractall(path)

    yield Repository(discover_repository(path))

    shutil.rmtree(path)


@pytest.fixture(scope='function')
def nonempty_repo() -> Repository:
    path = tempfile.mkdtemp()
    with tarfile.open(Path(__file__).parent.joinpath('res', 'nonempty-repo.tar.gz')) as file:
        file.extractall(path)

    yield Repository(discover_repository(path))

    shutil.rmtree(path)
