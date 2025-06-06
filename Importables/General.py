import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21
import ms3

def load_df():

    md_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/metadata.tsv"
    metadata = pd.read_csv(md_path, sep='\t')

    dfs = []
    for _, row in metadata.iterrows():
        rel_paths = row['rel_paths']
        fnames = row['fnames']
        
        base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
        notes_path = base_path + "/notes/" + fnames + ".tsv"
        labels_path = base_path + "/labels/" + fnames + ".labels.tsv"
        
        try: 
            df_notes = pd.read_csv(notes_path, sep='\t')

            df_notes['pc'] = df_notes['midi'] % 12
            df_notes['pc'] = df_notes['pc'].apply(int)

            df_notes['note'] = df_notes['tpc'].apply(ms3.tpc2name)
        
            df_notes['mc_onset_float'] = df_notes['mc_onset'].apply(lambda x: float(Fraction(x)))
            df_notes['time'] = df_notes['mc'] + df_notes['mc_onset_float']

            df_notes['artist'] = row['artists']
            df_notes['workTitle'] = row['workTitle']
            df_notes['fnames'] = row['fnames']
            df_notes['rel_paths'] = row['rel_paths']
            df_notes['recording_year'] = row['recording_year']

            df_labels = pd.read_csv(labels_path, sep='\t')
            df_labels['mc_onset_float'] = df_labels['mc_onset'].apply(lambda x: float(Fraction(x)))
            df_labels['time'] = df_labels['mc'] + df_labels['mc_onset_float']
            
            df = pd.merge(df_notes, df_labels[['time', 'harmony_layer', 'label']], on='time', how='left')

            dfs.append(df)

    
        except Exception as e:
            #print(f'{e}')
            continue
    
    dfs = pd.concat(dfs, ignore_index=True)
    
    return dfs

