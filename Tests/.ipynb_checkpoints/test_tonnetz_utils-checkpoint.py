import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import tonnetz_utils as t
import pandas as pd
from fractions import Fraction

def test_parallel_Major_to_minor():
    data_raw = {"label": ['C', 'Cmin']}
    data = pd.DataFrame(data_raw)
    expected = "P"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_parallel_minor_to_Major():
    data_raw = {"label": ['Cmin', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "P"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected


def test_relative_Major_to_minor():
    data_raw = {"label": ['C', 'Amin']}
    data = pd.DataFrame(data_raw)
    expected = "R"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_relative_minor_to_Major():
    data_raw = {"label": ['Amin', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "R"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_leading_Major_to_minor():
    data_raw = {"label": ['C', 'Emin']}
    data = pd.DataFrame(data_raw)
    expected = "L"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_leading_minor_to_Major():
    data_raw = {"label": ['Emin', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "L"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_slide_Major_to_minor():
    data_raw = {"label": ['C', 'C#min']}
    data = pd.DataFrame(data_raw)
    expected = "S"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_slide_minor_to_Major():
    data_raw = {"label": ['C#min', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "S"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_nebenverwandt_Major_to_minor():
    data_raw = {"label": ['C', 'Fmin']}
    data = pd.DataFrame(data_raw)
    expected = "N"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_nebenverwandt_minor_to_Major():
    data_raw = {"label": ['Fmin', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "N"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_hexpole_Major_to_minor():
    data_raw = {"label": ['C', 'A-min']}
    data = pd.DataFrame(data_raw)
    expected = "H"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected
    
def test_hexpole_minor_to_Major():
    data_raw = {"label": ['A-min', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "H"
    
    result = t.transformation(data)

    assert result.iloc[0]['transformation'] == expected

def test_none_1():
    data_raw = {"label": ['A', 'C']}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result = t.transformation(data)

def test_none_2():
    data_raw = {"label": ['Amin', 'Cmin']}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result = t.transformation(data)

def test_none_3():
    data_raw = {"label": ['C', 'Bmin']}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result = t.transformation(data)

def test_none_4():
    data_raw = {"label": ['Amin', 'B']}
    data = pd.DataFrame(data_raw)
    expected = "N/A"
    
    result = t.transformation(data)