import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

# takes read tsv file of single composition returns df with listing harmonies
pitch_class_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F',
                   'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def preprocess_df(df_raw):
    df = df_raw.copy()
    df['pc'] = df['midi'] % 12
    df = df[df['pc'].notna()]
    df['pc'] = df['pc'].apply(int)
    df['note'] = df['pc'].map(lambda x: pitch_class_names[x])
    
    df['mc_onset_float'] = df['mc_onset'].apply(lambda x: float(Fraction(x)))
    df['order'] = df['mc'] + df['mc_onset_float']

    pc = generate_pc(df)

    return pc

# Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
def generate_pc(df_raw):
    pitchclass = df_raw.copy()
    pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc']].agg(list).reset_index()
    pitchclass['pc'] = pitchclass['pc'].apply(lambda x: list(set(x)))
    return pitchclass

# Takes df and returns true if there exists harmony
def contains_harmony(pc):
    test = pc[pc['pc'].apply(lambda x: len(x) > 1)].copy()
    if test.empty:
        return False
    else:
        return True

# takes metadata and filters by those containing harmony
def harmony_df(metadata, base_path):
    dfs = []
    for row in range(metadata.shape[0]): 
        path_row = base_path + "/" + metadata.iloc[row,1] + ".tsv"
        try: 
            df = pd.read_csv(path_row, sep='\t')
            pc = preprocess_df(df)
    
            if (contains_harmony(pc) == True):
                pc['artists'] = metadata.iloc[row]['artists']
                pc['workTitle'] = metadata.iloc[row]['workTitle']
                pc['fnames'] = metadata.iloc[row]['fnames']
                pc['recording_year'] = metadata.iloc[row]['recording_year']
                dfs.append(pc)
        except Exception as e:
            continue
    
    dfs = pd.concat(dfs, ignore_index=True)
    return dfs

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