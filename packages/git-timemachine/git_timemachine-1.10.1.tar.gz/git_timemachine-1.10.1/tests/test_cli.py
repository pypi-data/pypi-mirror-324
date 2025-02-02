import importlib.metadata

from click.testing import CliRunner
from git_timemachine.__main__ import cli


def test_cli_version(cli_runner: CliRunner):
    result = cli_runner.invoke(cli, ['--version'])

    assert not result.exception
    assert result.output.strip() == importlib.metadata.version('git_timemachine')
