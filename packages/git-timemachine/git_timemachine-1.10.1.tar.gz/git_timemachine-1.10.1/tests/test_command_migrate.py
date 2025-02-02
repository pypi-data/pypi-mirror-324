import shutil
import tempfile
from unittest.mock import patch

from click.testing import CliRunner
from pygit2 import discover_repository, Repository, Index  # pylint: disable=no-name-in-module

from git_timemachine.__main__ import cli


def test_cli_migrate_command(cli_runner: CliRunner, nonempty_repo: Repository):
    dest_dir = tempfile.mktemp()

    result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'migrate', dest_dir])
    if result.exception:
        print(result.output)

    assert not result.exception

    dest_repo = Repository(discover_repository(dest_dir))

    src_commits = list(nonempty_repo.walk(nonempty_repo.head.target))
    dest_commits = list(dest_repo.walk(dest_repo.head.target))

    assert len(src_commits) == len(dest_commits)

    for i, src_commit in enumerate(src_commits):
        assert dest_commits[i].author.name == src_commit.author.name
        assert dest_commits[i].author.email == src_commit.author.email
        assert dest_commits[i].author.time == src_commit.author.time

        assert dest_commits[i].committer.name == src_commit.committer.name
        assert dest_commits[i].committer.email == src_commit.committer.email
        assert dest_commits[i].committer.time == src_commit.committer.time

    shutil.rmtree(dest_dir)

    dest_dir = tempfile.mkdtemp()
    result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'migrate', dest_dir])
    assert result.exception
    assert 'already exists' in result.output
    shutil.rmtree(dest_dir)

    dest_dir = tempfile.mktemp()
    with patch.object(Index, 'write_tree', return_value=None):
        result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'migrate', dest_dir])
        assert result.exception
        assert 'Failed to write index tree.' in result.output
    shutil.rmtree(dest_dir)
