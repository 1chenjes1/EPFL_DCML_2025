import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

# takes read tsv file of single composition returns df with listing harmonies
pitch_class_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F',
                   'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def preprocess_df(fname):
    base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/notes" 
    path_row = base_path + "/" + fname + ".tsv"

    try: 
        df = pd.read_csv(path_row, sep='\t')
        df['pc'] = df['midi'] % 12
        df = df[df['pc'].notna()]
        df['pc'] = df['pc'].apply(int)
        df['note'] = df['pc'].map(lambda x: pitch_class_names[x])
        
        df['mc_onset_float'] = df['mc_onset'].apply(lambda x: float(Fraction(x)))
        df['order'] = df['mc'] + df['mc_onset_float']

    except Exception as e:
        print(f"{e}")
    
    return df

# Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
def generate_pcs(df_raw):
    pitchclass = df_raw.copy()
    pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc', 'midi']].agg(list).reset_index()
    pitchclass['pcs'] = pitchclass['pc'].apply(lambda x: list(set(x)))
    return pitchclass


# Takes df and groups by workTitle if theres more than length instances
def groupby_standard(dfs, length=3):
    title_grouped = dfs.copy()
    ref = dfs.copy()
    ref = ref.groupby('workTitle', as_index=False).agg(list).reset_index()
    ref = ref[ref['recording_year'].apply(lambda x: len(x) > length)].copy()
    title_grouped = title_grouped[title_grouped['workTitle'].isin(ref['workTitle'])]
    return title_grouped, ref

# Takes df and groups by artist if theres more than length instances
def groupby_artist(dfs, length=5):
    artist_grouped = dfs.copy()
    ref = dfs.copy()
    ref = ref.groupby('artists', as_index=False).agg(list).reset_index()
    ref = ref[ref['workTitle'].apply(lambda x: len(x) > length)].copy()
    artist_grouped = artist_grouped[artist_grouped['artists'].isin(ref['artists'])]
    return artist_grouped