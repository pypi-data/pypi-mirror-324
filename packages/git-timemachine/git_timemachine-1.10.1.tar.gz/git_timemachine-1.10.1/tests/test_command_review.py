from click.testing import CliRunner
from pygit2 import Repository

from git_timemachine.__main__ import cli


def test_command_log(cli_runner: CliRunner, nonempty_repo: Repository):
    result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'review'])

    assert 'date          commits\n----------  ---------\n2022-07-23          3' in result.output
