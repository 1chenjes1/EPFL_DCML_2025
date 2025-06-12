import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import General as g
import pandas as pd
from fractions import Fraction


def test_load_df_1():
    label = pd.read_csv("/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/labels/12 Keys Blues - Bob Mintzer.labels.tsv", sep='\t')
    
    result = label[(label['mc'] == 1) & (label['mc_onset'] == "0")]['label'].tolist()
    
    df = g.load_df()
    df = df[df['fnames'] == "12 Keys Blues - Bob Mintzer"]
    
    df_result = df[(df['mc'] == 1) & (df['mc_onset'] == Fraction("7/8"))]['label'].tolist()
    
    assert result == df_result

def test_load_df_2():
    
    df = g.load_df()
    df = df[df['fnames'] == "Vulfpeck-Fugue_State"]
    
    df_result = df[(df['mc'] == 1) & (df['mc_onset'] == Fraction("0"))]
    df_result = df_result.iloc[0]['label']
    
    assert pd.isna(df_result) == True

def test_fix_flats():
    labels = ['Bbmaj7', 'Eb/C', 'Ab7/G', 'Dbmaj7', 'Gbm7', 'D7b9', 'Cmb5']
    expected = ['B-maj7', 'E-/C', 'A-7/G', 'D-maj7', 'G-m7', 'D7b9', 'Cmb5']

    for input_label, expected_label in zip(labels, expected):
        assert fix_flats(input_label) == expected_label
