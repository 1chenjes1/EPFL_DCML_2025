import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

def get_tpc(n):
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

def create_data(subset, identifier):
    data = {}

    for row in range(subset.shape[0]):
        subset_row = subset.iloc[[row]]

        if isinstance(identifier, (list, tuple)):
            key = tuple(subset_row.iloc[0][col] for col in identifier)
        else:
            key = subset_row.iloc[0][identifier]

        data[key] = subset_row.iloc[0][['note', 'tpc', 'duration', 'transposed note', 'transposed tpc']]
        
    return data

def transpose_to_C(notes_df):
    transposed_pcs = []
    transposed_notes = []
    transposed_tpc = []
    
    for _, row in notes_df.iterrows():
        
        try: 
            note_raw = row['note']
            note = m21.note.Note(note_raw)
            key_raw = row['key']
            key = m21.key.Key(key_raw[0])
            i = m21.interval.Interval(key.tonic, m21.key.Key('C').tonic)
    
            note_new = note.transpose(i)

            transposed_pcs.append(note_new.pitch.pitchClass)
            transposed_notes.append(note_new.name)
            transposed_tpc.append(get_tpc(note_new.name))
            
        except Exception as e:
            #print(f'{e}')
            transposed_pcs.append(np.nan)
            transposed_notes.append(np.nan)
            transposed_tpc.append(np.nan)

    notes_df['transposed pc'] = transposed_pcs
    notes_df['transposed note'] = transposed_notes
    notes_df['transposed tpc'] = transposed_tpc
    
    return notes_df

def plot_pitch_distribution(data, identifier, fig_name = False):
    keys = list(data.keys())
    num_items = len(keys)
    
    fig = plt.figure(figsize=(12, 4.5 * num_items))
    subfigs = fig.subfigures(nrows=num_items, ncols=1)

    if num_items == 1:
        subfigs = [subfigs]  # make iterable

    for i, key in enumerate(keys):
        subfig = subfigs[i]

        # Format title from key (tuple or string)
        if isinstance(key, tuple):
            label = " – ".join(str(k) for k in key)
        else:
            label = str(key)

        subfig.suptitle(f'{label}', fontsize=14)

        ax = subfig.subplots(nrows=1, ncols=1)

        # Get the pitch profile data:
        pitch_data = data[key]
        tpc = pd.DataFrame({
            'note': pitch_data['note'],
            'tpc': pitch_data['tpc'],
            'duration': pitch_data['duration']
        })

        pitch_counts = tpc.groupby(['note', 'tpc'])['duration'].sum().reset_index(name='weighted_count')
        count = pitch_counts.sort_values('tpc')
        total = count['weighted_count'].sum()
        count['percentage'] = count['weighted_count'] / total

        # Plot histogram:
        ax.bar(count['note'], count['percentage'], color='skyblue', edgecolor='black')
        ax.set_xlabel('Pitch')
        ax.set_ylabel('Percentage')

    # Global figure title:
    fig.suptitle(f'Pitch Profiles by {identifier}', fontsize=16)
    
    if fig_name:
        plt.savefig(f"../Jessica-ERIP2025/Results/{fig_name}")

    plt.show()

# def get_pitch_profiles(metadata):
#     metadata = metadata[metadata['fnames'] != "Give Thanks - Yohan Kim"]
#     pitch_profiles = []
    
#     for _, row in metadata.iterrows():
#         pitch_profile = []
#         rel_paths = row['rel_paths']
#         fnames = row['fnames']
        
#         base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions" 
#         notes_path = base_path + "/notes/" + fnames + ".tsv"

#         try: 
#             df_notes = pd.read_csv(notes_path, sep='\t')
#             df_notes['mc'] = df_notes['mc'].astype(int)

#             df_notes['pc'] = df_notes['midi'] % 24
#             df_notes['pc'] = df_notes['pc'].apply(int)

#             df_notes['note'] = df_notes['tpc'].apply(ms3.tpc2name)
#             df_notes['note'] = df_notes['note'].apply(fix_flats)
        
#             df_notes['mc_onset'] = df_notes['mc_onset'].astype(str).apply(lambda x: float(Fraction(x)))
#             df_notes['duration'] = df_notes['duration'].astype(str).apply(lambda x: float(Fraction(x)))
#             df_notes['time'] = df_notes['mc'] + df_notes['mc_onset']

#             df_notes = df_notes.sort_values(by='time')

#             pitch_profile['artist'] = row['artists']
#             pitch_profile['workTitle'] = row['workTitle']
#             pitch_profile['fnames'] = row['fnames']
#             pitch_profile['rel_paths'] = row['rel_paths']
#             pitch_profile['recording_year'] = row['recording_year']