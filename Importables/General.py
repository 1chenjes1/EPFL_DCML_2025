import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21
import ms3
from functools import lru_cache

import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import intervalanalysis_utils as ia

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

def load_metadata():
    metadata = pd.read_csv("/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions/metadata.tsv", sep='\t')
    metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]
    metadata['recording_year'] = pd.to_numeric(metadata['recording_year'], errors='coerce')
    return metadata
    
def load_harmonies(metadata):
    metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]
    dfs = []
    for _, row in metadata.iterrows():
        try: 
            rel_paths = row['rel_paths']
            fnames = row['fnames']
            
            base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
            score_path = f"{base_path}/{rel_paths}/{fnames}.xml"
    
    
            score = m21.converter.parse(score_path)
            
            for h in score.recurse().getElementsByClass('Harmony'):
                score.remove(h, recurse=True)
                
            chords = score.chordify()
                
            # Build list of dictionaries to collect data
            rows = []
            
            for thisChord in chords.recurse().getElementsByClass(m21.chord.Chord):
                h = [p for p in thisChord.pitches]
                
                if len(h) <= 1:
                    continue
                    
                intervals, semitones = ia.get_intervals_semitones(h)
                intervals_from_root, semitones_from_root = ia.get_intervals_semitones_from_root(h)
            
                rows.append({
                    'artist': row['artists'],
                    'workTitle': row['workTitle'],
                    'fnames': fnames,
                    'rel_paths': rel_paths,
                    'recording_year': row['recording_year'],
                    'time': thisChord.offset,
                    'duration_qb': thisChord.quarterLength,
                    'harmony': h,
                    'interval': intervals,
                    'semitones': semitones,
                    'interval from root': intervals_from_root,
                    'semitones from root': semitones_from_root
                })
                
            # Convert to DataFrame
            dfs.append(pd.DataFrame(rows))
        except Exception as e:
            #print(f'error:{e}')
            continue
    
    dfs = pd.concat(dfs, ignore_index=True)
    
    return dfs
    
def load_labels(metadata):
    metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]
    dfs = []
    for _, row in metadata.iterrows():
        rel_paths = row['rel_paths']
        fnames = row['fnames']
        
        base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
        labels_path = base_path + "/labels/" + fnames + ".labels.tsv"
        
        try: 
            df_labels = pd.read_csv(labels_path, sep='\t')
            df_labels['artist'] = row['artists']
            df_labels['workTitle'] = row['workTitle']
            df_labels['fnames'] = row['fnames']
            df_labels['rel_paths'] = row['rel_paths']
            df_labels['recording_year'] = row['recording_year']
            df_labels['year_bin'] = row['year_bin']
            
            df_labels['mc'] = df_labels['mc'].astype(int)
            df_labels['mc_onset'] = df_labels['mc_onset'].astype(str).apply(lambda x: float(Fraction(x)))
            df_labels['time'] = df_labels['mc'] + df_labels['mc_onset']

            df_labels['label'] = df_labels['label'].apply(clean_chord_label)
            df_labels['ILS'] = df_labels['label'].apply(get_ilset)

            df_labels = df_labels.sort_values(by='time')

            dfs.append(df_labels)

    
        except Exception as e:
            #print(f'{e}')
            continue
    
    dfs = pd.concat(dfs, ignore_index=True)
    
    return dfs


def load_keys(metadata):

    metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]

    metadata['key'] = None

    for i, row in metadata.iterrows():
        rel_paths = row['rel_paths']
        fnames = row['fnames']
        
        base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
        score_path = f"{base_path}/{rel_paths}/{fnames}.xml"
        
        try: 
            score = m21.converter.parse(score_path)
            key = score.analyze('key')
            metadata.loc[i, 'key'] = str(key)

    
        except Exception as e:
            #print(f'{e}')
            continue

    
    return metadata


def load_notes(metadata, keys=False):
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

            df_notes['pc'] = df_notes['midi'] % 24
            df_notes['pc'] = df_notes['pc'].apply(int)

            df_notes['note'] = df_notes['tpc'].apply(ms3.tpc2name)
            df_notes['note'] = df_notes['note'].apply(fix_flats)
        
            df_notes['mc_onset'] = df_notes['mc_onset'].astype(str).apply(lambda x: float(Fraction(x)))
            df_notes['duration'] = df_notes['duration'].astype(str).apply(lambda x: float(Fraction(x)))
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
            
            df_labels['label'] = df_labels['label'].apply(clean_chord_label)
            df_labels['ILS'] = df_labels['label'].apply(get_ilset)

            df_labels = df_labels.sort_values(by='time')
            df_notes = df_notes.sort_values(by='time')

            if keys:
                try:
                    score_path = f"{base_path}/{rel_paths}/{fnames}.xml"
                    score = m21.converter.parse(score_path)
                    key = score.analyze('key')
                    df_notes['key'] = str(key)
                except Exception:
                    df_notes['key'] = np.nan
            
            df = pd.merge_asof(df_notes, df_labels[['time', 'label', 'ILS']], on='time', direction='backward')

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


import re
def fix_flats(label):
    label = re.sub(r'([A-Ga-g])bbb', r'\1---', label)
    label = re.sub(r'([A-Ga-g])bb', r'\1--', label)
    label = re.sub(r'([A-Ga-g])b', r'\1-', label)
    return label

def clean_chord_label(label):
    if not isinstance(label, str):
        return label
        
    label = re.sub(r'\((.*?)\)', r'\1', label)
    label = fix_flats(label)
    
    label = label.replace('Maj', 'M')
    label = label.replace('maj', 'M')
    
    label = label.replace('min', 'm')

    label = label.replace('M6', '6')
    label = label.strip()

    
    return label

@lru_cache(maxsize=None)
def parse_chord(label):
    return m21.harmony.ChordSymbol(label)

def get_ilset(label):
    try:
        chord = parse_chord(label)
        chord_pitches = chord.pitches
        chord_tones = [p.name for p in chord_pitches]
        return chord_tones
    except Exception as e:
        return np.nan


