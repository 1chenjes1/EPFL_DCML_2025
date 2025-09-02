import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

def get_fifthsteps(n):
    """
    Returns fifth step from note (C=0, G=1, etc.)

    Args:
        n: string or music21.note.Note object

    Return:
        integer 
    """
    base_tpc = {
        'F': -1,
        'C': 0,
        'G': 1,
        'D': 2,
        'A': 3,
        'E': 4,
        'B': 5
    }
    try:
        if not isinstance(n, m21.note.Note):
            n = m21.note.Note(n)
        
        pitch = n.pitch
        letter = pitch.step 

        # sharp = +1, flat = -1, etc.
        acc = pitch.accidental
        acc_offset = acc.alter if acc is not None else 0

        tpc = base_tpc[letter]

        tpc += int(acc_offset * 7)

        return tpc
        
    except Exception as e:
        return None

def get_note(fifth):
    """
    Returns note name given the fifth step (0=C, 1=G, etc.)

    Args:
        fifth: fifth step, integer 

    Return:
        note String 
    """
    
    base_note = {
        -1: 'F',
        0: 'C',
        1: 'G',
        2: 'D',
        3: 'A',
        4: 'E',
        5: 'B'
    }
    try:
        base_tpc = ((fifth + 1) % 7) - 1
        note_base = base_note[base_tpc]

        accidental = (tpc - base_tpc) // 7

        if accidental > 0:
            note = note_base + "#" * accidental
        elif accidental < 0:
            note = note_base + "-" * (-accidental)
        else:
            note = note_base

        return note
    except Exception as e:
        return None    


def transpose_note(note, key):
    """
    Returns note transposed to C

    Args:
        note: Note, string or music21.note.Note object
        key: Key of piece, string or music21.key.Key object

    Return:
        music21.note.Note object
    """
    try: 
        if not isinstance(note, m21.note.Note):
            note = m21.note.Note(note)
        if not isinstance(key, m21.key.Key):
            key = m21.key.Key(key)
            
        i = m21.interval.Interval(key.tonic, m21.key.Key('C').tonic)

        note_new = note.transpose(i)
        
    except Exception as e:
        note_new = np.nan

    return note_new
            
def transpose_to_C(df):
    """
    Returns df with all notes transposed to C

    Args:
        df: pd.DataFrame representation of notes (from general.load_notes())

    Return:
        pd.DataFrame
        Transposed notes are found in columns ['pc', 'note', 'tpc']
        Original notes are found in columns ['old pc', ' old note', 'old tpc']
    """
    notes_df = df.copy()
    notes_df['old pc'] = notes_df['pc']
    notes_df['old note'] = notes_df['note']
    notes_df['old tpc'] = notes_df['tpc']
    
    transposed_pcs = []
    transposed_notes = []
    transposed_tpc = []
    
    for _, row in notes_df.iterrows():
     
        note_raw = row['note']
        key_raw = row['key']  
        if isinstance(note_raw, str) and isinstance(key_raw, str):

            note = m21.note.Note(note_raw)  
            key = m21.key.Key(key_raw.split()[0])
            note_new = transpose_note(note, key)
        else:
            note_new = np.nan

        if isinstance(note_new, m21.note.Note):
            transposed_pcs.append(note_new.pitch.pitchClass)
            transposed_notes.append(note_new.name)
            transposed_tpc.append(get_fifthsteps(note_new.name))
        else:
            transposed_pcs.append(note_new)
            transposed_notes.append(note_new)
            transposed_tpc.append(note_new)

        
    notes_df['pc'] = transposed_pcs
    notes_df['note'] = transposed_notes
    notes_df['tpc'] = transposed_tpc
    
    return notes_df

def plot_pitch_distribution(data_df, title):
    """
    Returns plot of pitch profile distribution, coloured by years and normalized and weighed by note duration

    Args:
        data_df: pd.DataFrame representation of notes with columns (from general.load_notes())

    Return:
        matplotlib fig, axis
    """
    
    full_range = pd.DataFrame({
        'tpc': range(
            int(data_df['tpc'].min()),
            int(data_df['tpc'].max()) + 1  # include max
        )
    })
    
    
    fig, ax = plt.subplots(figsize=(15, 6)) 
    
    year_bins = sorted(
            data_df["year_bin"].unique(),
            key=lambda x: int(str(x).split("-")[0])
        )

    colors = plt.cm.get_cmap('viridis', len(year_bins))  # Distinct colors
    
    for i, key in enumerate(year_bins):
    
        pitch_data = data_df[data_df['year_bin'] == key]
        tpc = pitch_data[['note', 'tpc', 'duration']]
    
        pitch_counts = tpc.groupby(['note', 'tpc'])['duration'].sum().reset_index(name='weighted_count')
        count = pitch_counts.sort_values('tpc')
        total = count['weighted_count'].sum()
        count['percentage'] = (count['weighted_count'] / total)*100
    
        count = full_range.merge(count, on='tpc', how='left')
        count = count.fillna({'weighted_count': 0, 'percentage': 0})
        count['note'] = count['tpc'].apply(get_note)
    
        ax.plot(count['note'], count['percentage'], color=colors(i), alpha=0.5)
        ax.scatter(count['note'],count['percentage'], label=key, color=colors(i))
    
    ax.set_xlabel('Pitch', fontsize=16)
    ax.set_ylabel('Percentage %', fontsize=16)
    ax.set_title(title, fontsize=19)
    ax.legend(title='Recording Year', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14,rotation=45)

    return fig, ax

