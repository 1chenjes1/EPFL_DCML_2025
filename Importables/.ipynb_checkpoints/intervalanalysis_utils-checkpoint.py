import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

# Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
def generate_pcs(df_raw):
    pitchclass = df_raw.copy()
    pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc']].agg(list).reset_index()
    pitchclass['pcs'] = pitchclass['pc'].apply(lambda x: list(set(x)))
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
    
# Takes list of notes and returns list of interval classes between all note pairs
def interval_class(notes):
    interval_classes = []
    
    # Generate all unique pairs:
    pairs = itertools.combinations(notes, 2)
    
    for n1_str, n2_str in pairs:
        # Convert to music21 Notes:
        n1 = m21.note.Note(n1_str)
        n2 = m21.note.Note(n2_str)
        
        # Compute interval:
        i = m21.interval.Interval(noteStart=n1, noteEnd=n2)
        
        # Append the interval class:
        interval_classes.append(i.intervalClass)
    
    return interval_classes

# Takes list of pc and returns int (normalized dissonance index of pitch class set)
def dissonance(harmony):
    ic = interval_class(harmony)
    num_notes = len(harmony)
    dissonance = (sum([dissonance_table[i] for i in ic])) / num_notes
    return dissonance 

dissonance_table = {
    0: 0.0,    # Unison
    1: 1.0,    # m2/M7
    2: 0.6,    # M2/m7
    3: 0.4,    # m3/M6
    4: 0.2,    # M3/m6 
    5: 0.0,    # P4/P5
    6: 0.8,    # Tritone
}