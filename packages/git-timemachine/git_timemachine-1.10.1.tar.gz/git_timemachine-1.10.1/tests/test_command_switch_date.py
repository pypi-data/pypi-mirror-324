import json
import tempfile
from datetime import datetime
from pathlib import Path

from click.testing import CliRunner
from git_timemachine.__main__ import cli


def test_cli_switch_date_command(cli_runner: CliRunner):
    cache_dir = tempfile.mkdtemp()

    state_file = Path(cache_dir, 'commit-time')

    state_file.write_text('{"type": "datetime", "value": "2030-01-01T00:00:00+08:00"}', encoding='utf-8')

    result = cli_runner.invoke(cli, ['--states-dir', cache_dir, 'switch-date'])
    assert not result.exception

    states = json.loads(state_file.read_text(encoding='utf-8'))
    assert datetime.fromisoformat(states['value']) == datetime.fromisoformat('2030-01-02T10:00:00+08:00')
    state_file.unlink()
