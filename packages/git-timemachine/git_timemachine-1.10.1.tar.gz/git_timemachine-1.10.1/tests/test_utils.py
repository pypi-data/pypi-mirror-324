import json
import random
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from chance import chance

from git_timemachine.utils import StateManager, get_offset_seconds


def test_statemanager():
    root_dir = Path(tempfile.mkdtemp())
    key_file = root_dir.joinpath('key')

    states = StateManager(root_dir)

    value = random.randint(1, 1000)
    states.set('key', value)
    assert states.get('key') == value
    assert key_file.read_text(encoding='utf-8') == str(value)

    value = chance.pickone([True, False])
    states.set('key', value)
    assert states.get('key') == value
    assert key_file.read_text(encoding='utf-8') == str(value).lower()

    value = random.uniform(1.0, 1000.0)
    states.set('key', value)
    assert states.get('key') == value
    assert key_file.read_text(encoding='utf-8') == str(value)

    value = chance.sentence()
    states.set('key', value)
    assert states.get('key') == value
    assert key_file.read_text(encoding='utf-8') == f'"{value}"'

    value = datetime.now()
    states.set('key', value)
    assert states.get('key') == value
    assert key_file.read_text(encoding='utf-8') == json.dumps({'type': 'datetime', 'value': value.isoformat()})

    value = {'test-key': 'test-value'}
    states.set('key', value)
    assert states.get('key') == value

    value = [chance.word(), random.randint(0, 1000), random.uniform(1.0, 1000.0), True, False, {'test-key': 'test-value'}, datetime.now()]
    states.set('key', value)
    assert states.get('key') == value

    with pytest.raises(TypeError):
        states.set('key', states)

    key_file.write_text('{"type": "known", "value": null}', encoding='utf-8')
    with pytest.raises(TypeError):
        states.get('key')

    assert states.get('unknown-key', 'default-value') == 'default-value'

    shutil.rmtree(root_dir)


def test_get_offset_seconds():
    assert get_offset_seconds(None) == 0
    assert get_offset_seconds('1234') == 1234
    assert get_offset_seconds('1234h') == 1234 * 3600
    assert get_offset_seconds('1234d') == 1234 * 86400
    assert get_offset_seconds('1234m') == 1234 * 86400 * 30
    assert get_offset_seconds('1234y') == 1234 * 86400 * 365

    assert get_offset_seconds('-1234') == -1234
    assert get_offset_seconds('-1234h') == -1234 * 3600
    assert get_offset_seconds('-1234d') == -1234 * 86400
    assert get_offset_seconds('-1234m') == -1234 * 86400 * 30
    assert get_offset_seconds('-1234y') == -1234 * 86400 * 365
