import random
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List
from unittest.mock import patch

from chance import chance
from click.testing import CliRunner
# pylint: disable=no-name-in-module
from pygit2 import Repository, Index, Signature

from git_timemachine.__main__ import cli
from git_timemachine.utils import StateManager

from .helper import GIT_USER_NAME, GIT_USER_EMAIL, repo_add_new_file, generate_gitconfig, restore_gitconfig, run_command
from .res import extract_empty_repo, extract_nonempty_repo

CACHE_DIR = tempfile.mkdtemp()
CONFIG_FILE = Path(CACHE_DIR, 'config.ini')
STATES = StateManager(CACHE_DIR)


def setup_module():
    runner = CliRunner()
    runner.invoke(cli, ['--states-dir', CACHE_DIR, '--config-file', CONFIG_FILE, 'init'])

    generate_gitconfig()


def teardown_module():
    shutil.rmtree(CACHE_DIR)

    restore_gitconfig()


def run_commit_command(repo_dir: str, options: List[str]):
    return run_command(['-C', repo_dir, '--states-dir', CACHE_DIR, '--config-file', CONFIG_FILE], 'commit', options)


def assert_signature(signature: Signature, commit_time: datetime, random_range: List[int]):
    assert signature.name == GIT_USER_NAME
    assert signature.email == GIT_USER_EMAIL
    assert int(signature.time - commit_time.timestamp()) in range(random_range[0] - 1, random_range[1] + 1)


def assert_new_commit(repo: Repository, options: List[str]):
    if '--commit-time' in options:
        commit_time = datetime.fromisoformat(options[options.index('--commit-time') + 1])
    else:
        commit_time = STATES.get('commit-time')

    random_range = [int(x.strip()) for x in options[options.index('--random-range') + 1].split(',')]
    message = options[options.index('--message') + 1]
    external = '--external' in options

    if repo.head_is_unborn:
        commit_count = 0
        parent_id = None
    else:
        commits = list(repo.walk(repo.head.target))
        commit_count = len(commits)
        parent_id = str(commits[0].id)

    new_file = repo_add_new_file(repo)

    result = run_commit_command(repo.workdir, options)

    if result.exception:
        print(result.output)

    assert not result.exception

    commits = list(repo.walk(repo.head.target))

    assert len(commits) == commit_count + 1

    if commit_count == 0:
        assert len(commits[0].parents) == 0
    else:
        assert str(commits[0].parents[0].id) == parent_id

    assert_signature(commits[0].author, commit_time, random_range)
    assert_signature(commits[0].committer, commit_time, random_range)

    if not external:
        assert 'commit:' in result.output
        assert f'author: {GIT_USER_NAME} <{GIT_USER_EMAIL}>' in result.output
        assert f'committer: {GIT_USER_NAME} <{GIT_USER_EMAIL}>' in result.output
        assert 'datetime: ' in result.output
        assert f'message: {message}' in result.output
        assert re.search(f'A +{new_file.name} +10064', result.output)


def _test_commit_with_specified_time():
    commit_time = chance.date(2023, 1, 1).astimezone()
    random_range = [random.randint(100, 200), random.randint(200, 300)]

    options = ['--commit-time', commit_time.isoformat(), '--random-range', f'{random_range[0]},{random_range[1]}', '--message', chance.sentence()]

    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        assert_new_commit(repo, options)
        shutil.rmtree(repo.workdir)


def test_commit_with_states():
    commit_time = chance.date(2023, 1, 1).astimezone()

    STATES.set('commit-time', commit_time)

    random_range = [random.randint(100, 200), random.randint(200, 300)]

    options = ['--random-range', f'{random_range[0]},{random_range[1]}', '--message', chance.sentence()]

    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        assert_new_commit(repo, options)
        shutil.rmtree(repo.workdir)


def test_commit_with_external():
    commit_time = chance.date(2023, 1, 1).astimezone()
    random_range = [random.randint(100, 200), random.randint(200, 300)]
    message = chance.sentence()

    options = ['--commit-time', commit_time.isoformat(), '--random-range', f'{random_range[0]},{random_range[1]}', '--message', message, '--external']

    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        assert_new_commit(repo, options)
        shutil.rmtree(repo.workdir)


def test_exception_nothing_to_commit():
    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        result = run_commit_command(repo.workdir, ['--message', chance.sentence()])

        assert result.exception
        assert 'Nothing to commit or pending changes.' in result.output
        shutil.rmtree(repo.workdir)


def test_exception_failed_write_tree():
    with patch.object(Index, 'write_tree', return_value=None):
        for repo in [extract_empty_repo(), extract_nonempty_repo()]:
            repo_add_new_file(repo)

            result = run_commit_command(repo.workdir, ['--message', chance.sentence()])

            assert result.exception
            assert 'Failed to write index tree.' in result.output
            shutil.rmtree(repo.workdir)


def test_exception_failed_create_commit():
    with patch.object(Repository, 'create_commit', return_value=None):
        for repo in [extract_empty_repo(), extract_nonempty_repo()]:
            repo_add_new_file(repo)

            result = run_commit_command(repo.workdir, ['--message', chance.sentence()])

            assert result.exception
            assert 'Failed to create commit.' in result.output
            shutil.rmtree(repo.workdir)


def test_exception_commit_earlier():
    repo = extract_nonempty_repo()

    repo_add_new_file(repo)

    result = run_commit_command(repo.workdir, ['--commit-time', '2000-01-01T00:00:00+0800', '--message', chance.sentence()])

    assert result.exception
    assert 'Commit time is earlier than HEAD.' in result.output
    shutil.rmtree(repo.workdir)


def test_exception_random_range_length():
    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        repo_add_new_file(repo)

        result = run_commit_command(repo.workdir, ['--message', chance.sentence(), '--random-range', '1,2,3'])

        assert result.exception
        assert 'Length of list' in result.output
        shutil.rmtree(repo.workdir)


def test_exception_daily_commit_limit():
    for repo in [extract_empty_repo(), extract_nonempty_repo()]:
        repo_add_new_file(repo)

        result = run_commit_command(repo.workdir, ['--message', chance.sentence()])
        assert not result.exception

        repo_add_new_file(repo)
        result = run_commit_command(repo.workdir, ['--message', chance.sentence(), '--max-daily-commits', '1'])
        assert result.exception
        assert 'Exceeded the daily commit limit: 1' in result.output

        shutil.rmtree(repo.workdir)
