import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21
import ms3

pitch_class_names = [
    'B#', 'C',
    'C#', 'Db',
    'D',
    'D#', 'Eb',
    'E', 'Fb',
    'F', 'E#',
    'F#', 'Gb',
    'G',
    'G#', 'Ab',
    'A',
    'A#', 'Bb',
    'B', 'Cb'
]


def load_df():


    md_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/metadata.tsv"
    metadata = pd.read_csv(md_path, sep='\t')
    metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]

    dfs = []
    for _, row in metadata.iterrows():
        rel_paths = row['rel_paths']
        fnames = row['fnames']
        
        base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
        notes_path = base_path + "/notes/" + fnames + ".tsv"
        labels_path = base_path + "/labels/" + fnames + ".labels.tsv"
        
        try: 
            df_notes = pd.read_csv(notes_path, sep='\t')
            df_notes['mc'] = df_notes['mc'].astype(int)

            df_notes['pc'] = df_notes['midi'] % 12
            df_notes['pc'] = df_notes['pc'].apply(int)

            df_notes['note'] = df_notes['tpc'].apply(ms3.tpc2name)
        
            df_notes['mc_onset'] = df_notes['mc_onset'].astype(str).apply(lambda x: float(Fraction(x)))
            df_notes['time'] = df_notes['mc'] + df_notes['mc_onset']

            df_notes['artist'] = row['artists']
            df_notes['workTitle'] = row['workTitle']
            df_notes['fnames'] = row['fnames']
            df_notes['rel_paths'] = row['rel_paths']
            df_notes['recording_year'] = row['recording_year']

            df_labels = pd.read_csv(labels_path, sep='\t')
            df_labels['mc'] = df_labels['mc'].astype(int)
            df_labels['mc_onset'] = df_labels['mc_onset'].astype(str).apply(lambda x: float(Fraction(x)))
            df_labels['time'] = df_labels['mc'] + df_labels['mc_onset']

            df_labels = df_labels.sort_values(by='time')
            df_notes = df_notes.sort_values(by='time')
            
            df = pd.merge_asof(df_notes, df_labels[['time', 'label']], on='time', direction='backward')

            dfs.append(df)

    
        except Exception as e:
            #print(f'{e}')
            continue
    
    dfs = pd.concat(dfs, ignore_index=True)
    
    return dfs

from music21 import harmony

def label_to_pcs(label):
    cs = harmony.ChordSymbol(label)
    pcs = sorted([p.pitchClass for p in cs.pitches])
    return pcs

# FIX !!!!!
def generate_pcs(df):
    pitchclass = df.copy()
    pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc', 'midi']].agg(list).reset_index()
    pitchclass['pcs'] = pitchclass['pc'].apply(lambda x: list(set(x)))
    return pitchclass
    
def groupby_standard(df, length=3):
    # Step 1: Get unique (fnames, workTitle) pairs
    ref = df[['fnames', 'workTitle']].drop_duplicates()

    # Step 2: Group by workTitle → count how many files (fnames) per title
    ref_count = ref.groupby('workTitle').size().reset_index(name='count')

    # Step 3: Keep only titles with ≥ length files
    ref_filtered = ref_count[ref_count['count'] >= length]

    # Step 4: Filter big df to only those titles
    title_grouped = df[df['workTitle'].isin(ref_filtered['workTitle'])]

    return title_grouped, ref_filtered

