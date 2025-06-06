import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import General as g
import pandas as pd

def test_load_df_1():
    label = pd.read_csv("/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/labels/12 Keys Blues - Bob Mintzer.labels.tsv", sep='\t')
    
    result = label[(label['mc'] == "4") & (label['mc_onset'] == "0")]['label'].tolist()
    
    df = g.load_df()
    df = df[df['fnames'] == "12 Keys Blues - Bob Mintzer"]
    
    df_result = df[(df['mc'] == "4") & (df['mc_onset'] == "0")]['label'].tolist()
    
    assert result == df_result


def test_load_df_2():
    label = pd.read_csv("/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/labels/12 Keys Blues - Bob Mintzer.labels.tsv", sep='\t')
    
    result = label[(label['mc'] == "4") & (label['mc_onset'] == "1/2")]['label'].tolist()
    
    df = g.load_df()
    df = df[df['fnames'] == "12 Keys Blues - Bob Mintzer"]
    
    df_result = df[(df['mc'] == "4") & (df['mc_onset'] == "1/2")]['label'].tolist()
    
    assert result == df_result

