import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import tonnetz_utils as t
import pandas as pd
from fractions import Fraction

def test_parallel_Major_to_minor():
    data_raw = {"label": ['C', 'Cmin'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "P"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_parallel_minor_to_Major():
    data_raw = {"label": ['Cmin', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "P"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected


def test_relative_Major_to_minor():
    data_raw = {"label": ['C', 'Amin'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "R"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_relative_minor_to_Major():
    data_raw = {"label": ['Amin', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected= "R"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_leading_Major_to_minor():
    data_raw = {"label": ['C', 'Emin'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "L"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_leading_minor_to_Major():
    data_raw = {"label": ['Emin', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "L"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_slide_Major_to_minor():
    data_raw = {"label": ['C', 'C#min'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "S"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_slide_minor_to_Major():
    data_raw = {"label": ['C#min', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "S"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_nebenverwandt_Major_to_minor():
    data_raw = {"label": ['C', 'Fmin'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_nebenverwandt_minor_to_Major():
    data_raw = {"label": ['Fmin', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_hexpole_Major_to_minor():
    data_raw = {"label": ['C', 'A-min'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "H"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_hexpole_minor_to_Major():
    data_raw = {"label": ['A-min', 'C'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "H"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_none_1():
    data_raw = {"label": ['A', 'Csus2'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result, _ = t.transformation(data)
    assert result.iloc[0]['transformation'] == expected

def test_none_2():
    data_raw = {"label": ['Amin', 'Csus4'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_none_3():
    data_raw = {"label": ['C', 'Bmin'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result, _ = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_none_4():
    data_raw = {"label": ['Amin', 'B'],
               'fnames': 'p',
               'artist': 'c',
               'recording_year': 2009}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result, _ = t.transformation(data)
    assert result.iloc[0]['transformation'] == expected

def test_RP():
    chord1_name = 'C'
    chord2_name = 'A'
    expected = 'RP'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_LP():
    chord1_name = 'C'
    chord2_name = 'E'
    expected = 'LP'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_PR():
    chord1_name = 'C'
    chord2_name = 'E-'
    expected = 'PR'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_PL():
    chord1_name = 'C'
    chord2_name = 'A-'
    expected = 'PL'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_LP():
    chord1_name = 'A-'
    chord2_name = 'C'
    expected = 'LP'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_RP():
    chord1_name = 'E-'
    chord2_name = 'C'
    expected = 'RP'
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

def test_none():
    chord1_name = 'D'
    chord2_name = 'B-sus2#7add9add13'
    expected = None
    result = t.find_two_step_sequence(chord1_name, chord2_name)

    assert result == expected

    