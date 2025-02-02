import json
from typing import List

import yaml
from click.testing import CliRunner
from pygit2 import Repository, Commit  # pylint: disable=no-name-in-module

from git_timemachine.__main__ import cli


def assert_commit_logs(commits: List[Commit], logs: List[dict]):
    for i, log in enumerate(logs):
        assert log['id'] == str(commits[i].id)
        assert log['author']['name'] == commits[i].author.name
        assert log['author']['email'] == commits[i].author.email
        assert log['author']['time'] == commits[i].author.time
        assert log['author']['offset'] == commits[i].author.offset
        assert log['committer']['name'] == commits[i].committer.name
        assert log['committer']['email'] == commits[i].committer.email
        assert log['committer']['time'] == commits[i].committer.time
        assert log['committer']['offset'] == commits[i].committer.offset
        assert log['tree_id'] == str(commits[i].tree_id)
        assert log['gpg'] is None
        assert log['message'] == commits[i].message


def test_command_log(cli_runner: CliRunner, nonempty_repo: Repository):
    commits = list(nonempty_repo.walk(nonempty_repo.head.target))

    result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'log'])
    assert not result.exception

    assert_commit_logs(commits, json.loads(result.output))

    result = cli_runner.invoke(cli, ['-C', nonempty_repo.workdir, 'log', '--format', 'yaml'])

    assert not result.exception
    assert_commit_logs(commits, yaml.full_load(result.output))
