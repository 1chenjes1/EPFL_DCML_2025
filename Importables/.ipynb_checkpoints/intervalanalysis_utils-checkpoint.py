import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

# Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
# EDITTTT !!!! So that it generates ILC and OLC
def generate_pcs(df_raw):
    pitchclass = df_raw.copy()
    pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc']].agg(list).reset_index()
    pitchclass['pcs'] = pitchclass['pc'].apply(lambda x: list(set(x)))
    return pitchclass
    
from functools import lru_cache

@lru_cache(maxsize=None)
def parse_chord(label):
    return m21.harmony.ChordSymbol(label)

from itertools import combinations
def get_intervals_semitones(pcs):
    intervals = []
    semitones = []

    for pc1, pc2 in combinations(pcs, 2):
        
        # convert pc1
        if isinstance(pc1, m21.pitch.Pitch):
            p1 = pc1
        else:
            p1 = m21.pitch.Pitch(pc1)
        # convert pc2
        if isinstance(pc2, m21.pitch.Pitch):
            p2 = pc2
        else:
            p2 = m21.pitch.Pitch(pc2) 

        aInterval = m21.interval.Interval(pitchStart=p1, pitchEnd=p2)
        intervals.append(aInterval.simpleName)
        semitones.append(aInterval.semitones)
    
    return intervals, semitones


def label_to_intervals(label):
    try:
        chord = parse_chord(label)
        pcs = [p.pitchClass for p in chord.pitches]

        intervals, semitones = get_intervals_semitones(pcs)
        
        return intervals

    except Exception as e:
        return np.nan

pc_to_interval_name = {
    0: "P1",
    1: "m2",
    2: "M2",
    3: "m3",
    4: "M3",
    5: "P4",
    6: "A4/d5",   
    7: "P5",
    8: "m6",
    9: "M6",
    10: "m7",
    11: "M7"
}

# Takes list of pc and returns int (normalized dissonance index of pitch class set)
def label_to_dissonance(label):
    try:
        chord = parse_chord(label)
        pcs = [p.pitchClass for p in chord.pitches]

        intervals, semitones = get_intervals_semitones(pcs)

        semitones = [item % 12 for item in semitones]
        
        num_notes = len(pcs)
        dissonance = (sum([dissonance_table[i] for i in semitones])) / num_notes
        return dissonance 
    
    except Exception as e:
        # print(f"{e}")
        return np.nan
    

dissonance_table = {
    0: 0.0,    # Unison
    1: 1.0,    # m2/M7
    2: 0.6,    # M2/m7
    3: 0.4,    # m3/M6
    4: 0.2,    # M3/m6 
    5: 0.0,    # P4/P5
    6: 0.8,    # Tritone
    7: 0.0,
    8: 0.2,
    9: 0.4,
    10: 0.6,
    11: 1.0,
}

# takes df and returns data dict with songs and artists
def create_data(subset, identifier):
    data = {}

    for row in range(subset.shape[0]):
        subset_row = subset.iloc[[row]]

        if isinstance(identifier, (list, tuple)):
            key = tuple(subset_row.iloc[0][col] for col in identifier)
            
        else:
            key = subset_row.iloc[0][identifier]
            

        data[key] = subset_row.iloc[0][['interval', 'duration_qb']]
        
    return data
    
# takes list, list, dict
def plot_interval_distribution(data, identifier, fig_name = False):
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
        interval = data[key]
        interval = pd.DataFrame({'interval_name': interval['interval'], 'duration': interval['duration_qb']})
        interval = interval.explode('interval_name')

        interval_counts = (
            interval.groupby(['interval_name'])['duration']
            .sum()
            .reset_index(name='weighted_count')
        )

        interval_counts['semitone'] = interval_counts['interval_name'].apply(lambda x: m21.interval.Interval(x).semitones)
        count = interval_counts.sort_values('semitone')
        total = count['weighted_count'].sum()
        count['percentage'] = count['weighted_count'] / total

        # Plot bar chart
        ax.bar(count['interval_name'], count['percentage'], color='skyblue', edgecolor='black')
        ax.set_xlabel('Interval')
        ax.set_ylabel('Percentage')

    # Global figure title:
    fig.suptitle(f'Harmony Label Interval Distribution by {identifier}', fontsize=16)
    
    if fig_name:
        plt.savefig(f"../Results/{fig_name}")

    plt.show()
    
