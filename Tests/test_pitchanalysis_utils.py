import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import General as g
from Importables import pitchanalysis_utils as pa


def test_tpc():
    note_str = 'C'
    result = 0
    assert result == pa.get_tpc(note_str)

def test_tpc_2():
    note_str = 'F'
    result = -1
    assert result == pa.get_tpc(note_str)


def test_tpc_3():
    note_str = 'G#'
    result = 8
    assert result == pa.get_tpc(note_str)

def test_tpc_4():
    note_str = 'F-'
    result = -8
    assert result == pa.get_tpc(note_str)

def test_note():
    result = 'C'
    note_str = 0
    assert result == pa.get_note(note_str)

def test_note_2():
    result = 'F'
    note_str = -1
    assert result == pa.get_note(note_str)


def test_note_3():
    result = 'G#'
    note_str = 8
    assert result == pa.get_note(note_str)

def test_note_4():
    result = 'F-'
    note_str = -8
    assert result == pa.get_note(note_str)