import os
from pathlib import Path
from typing import List

from chance import chance
from click.testing import CliRunner, Result
from pygit2 import Repository

from git_timemachine.__main__ import cli

GIT_USER_NAME = 'git-timemachine'
GIT_USER_EMAIL = 'git-timemachine@email.com'


def repo_add_new_file(repo: Repository) -> Path:
    path = Path(repo.workdir, chance.word())
    path.write_text(chance.sentence(), encoding='utf-8')

    repo.index.add_all()
    repo.index.write()

    return path


def generate_gitconfig():
    gitconfig = Path(os.environ['HOME'], '.gitconfig')
    gitconfig_backup = Path(str(gitconfig) + '~')

    if gitconfig.exists():
        gitconfig.rename(gitconfig_backup)

    gitconfig.write_text(f'''
[user]
        name = {GIT_USER_NAME}
        email = {GIT_USER_EMAIL}
[init]
        defaultBranch = main
''', encoding='utf-8')


def restore_gitconfig():
    gitconfig = Path(os.environ['HOME'], '.gitconfig')
    gitconfig_backup = Path(str(gitconfig) + '~')

    gitconfig.unlink()

    if gitconfig_backup.exists():
        gitconfig_backup.rename(gitconfig)


def run_command(global_options: List[str], command: str, options: List[str]) -> Result:
    cli_runner = CliRunner()
    return cli_runner.invoke(cli, global_options + [command] + options)
