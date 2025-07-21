import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

canonical_intervals = [
    'd1', 'P1', 'm2', 'A1',  # Unison to Augmented Unison
    'M2', 'd3', 'A2',
    'm3', 'M3', 'd4', 'A3',
    'P4', 'A4', 'd5',
    'P5', 'A5', 'd6',
    'm6', 'M6', 'A6',
    'd7', 'm7', 'M7', 'A7',
    'P8', 'd9', 'm9', 'M9', 'A9',
    'd10', 'm10', 'M10', 'A10',
    'P11', 'A11', 'd12',
    'P12', 'A12', 'd13',
    'm13', 'M13', 'A13',
    'd14', 'm14', 'M14', 'A14',
    'P15', 'A15'
]

interval_order = {
    'd1': -1,
    'P1': 0,
    'm2': 1,
    'A1': 1,
    'M2': 2,
    'd3': 2,
    'A2': 3,
    'm3': 3,
    'M3': 4,
    'd4': 4,
    'A3': 5,
    'P4': 5,
    'A4': 6,
    'd5': 6,
    'P5': 7,
    'A5': 8,
    'd6': 7,
    'm6': 8,
    'M6': 9,
    'A6': 10,
    'd7': 9,
    'm7': 10,
    'M7': 11,
    'A7': 12,
    'P8': 12,
    'd9': 13,
    'm9': 13,
    'M9': 14,
    'A9': 15,
    'd10': 14,
    'm10': 15,
    'M10': 16,
    'A10': 17,
    'P11': 17,
    'A11': 18,
    'd12': 18,
    'P12': 19,
    'A12': 20,
    'd13': 20,
    'm13': 20,
    'M13': 21,
    'A13': 22,
    'd14': 21,
    'm14': 22,
    'M14': 23,
    'A14': 24,
    'P15': 24,
    'A15': 25
}


# Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
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
        
        if isinstance(pc1, m21.pitch.Pitch):
            p1 = pc1
        else:
            p1 = m21.pitch.Pitch(pc1)

        if isinstance(pc2, m21.pitch.Pitch):
            p2 = pc2
        else:
            p2 = m21.pitch.Pitch(pc2) 

        aInterval_raw = m21.interval.Interval(pitchStart=p1, pitchEnd=p2)
        aInterval_semitone = aInterval_raw.semitones % 24
        aInterval = m21.interval.Interval(aInterval_semitone)
        intervals.append(aInterval.name)
        semitones.append(aInterval_semitone)
    
    return intervals, semitones

def get_intervals_semitones_from_root(pcs):
    intervals = []
    semitones = []

    root = pcs[0]
    root_pitch = root if isinstance(root, m21.pitch.Pitch) else m21.pitch.Pitch(root)

    for pc in pcs[1:]:
        
        current_pitch = pc if isinstance(pc, m21.pitch.Pitch) else m21.pitch.Pitch(pc)
        interval_raw = m21.interval.Interval(pitchStart=root_pitch, pitchEnd=current_pitch)
        interval_semitones = interval_raw.semitones % 24
        interval = m21.interval.Interval(interval_semitones)
        intervals.append(interval.name)
        semitones.append(interval_semitones)
    
    return intervals, semitones


def label_to_intervals_semitones(label):
    root, chord_type = split_harmony_label(label)    
    try:
        if chord_type == 'm69':
            intervals_raw = ['m3', 'P5', 'M6', 'M9', 'M3', 'A4', 'M9', 'M2', 'P5', 'P4']
            
            intervals = [m21.interval.Interval(i).simpleName for i in intervals_raw]

            semitones = [m21.interval.Interval(i).semitones for i in intervals]

            return intervals, semitones

        elif chord_type == '13sus4' :
            chord = parse_chord(root + '13')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            root_pitch = chord.root().pitchClass
            
            # Remove the third
            pcs = [pc for pc in pcs if pc != third_pitch]
            
            # Add the P4 (5 semitones above root)
            P4_pitch = (root_pitch + 5) % 12
            pcs.insert(1, P4_pitch)
            

        elif chord_type == '9sus4':
            chord = parse_chord(root + '9')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            root_pitch = chord.root().pitchClass
            
            # Remove the third
            pcs = [pc for pc in pcs if pc != third_pitch]
            
            # Add the P4 (5 semitones above root)
            P4_pitch = (root_pitch + 5) % 12
            pcs.insert(1, P4_pitch)
            
            
        elif chord_type == '13no3':
            chord = parse_chord(root + '13')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            pcs = [pc for pc in pcs if pc != third_pitch]
            

        elif chord_type == '7no5': 
            chord = parse_chord(root + '7')
            pcs = [p.pitchClass for p in chord.pitches]
            
            fifth_pitch = chord.fifth.pitchClass
            pcs = [pc for pc in pcs if pc != fifth_pitch]
            

        elif chord_type == 'M7no5':
            chord = parse_chord(root + 'M7')
            pcs = [p.pitchClass for p in chord.pitches]
            
            fifth_pitch = chord.fifth.pitchClass
            pcs = [pc for pc in pcs if pc != fifth_pitch]

        else:
            chord = parse_chord(label)
            pcs = [p.pitchClass for p in chord.pitches]
    
        
        intervals, semitones = get_intervals_semitones(pcs)
            
        
        return intervals, semitones

    except Exception as e:
        #print(f'{chord_type}, {label},{e}')
        return np.nan, np.nan


def label_to_intervals_semitones_from_root(label):
    root, chord_type = split_harmony_label(label)    
    try:
        if chord_type == 'm69':
            intervals_raw = ['m3', 'P5', 'M6', 'M9']
            
            intervals = [m21.interval.Interval(i).simpleName for i in intervals_raw]

            semitones = [m21.interval.Interval(i).semitones for i in intervals]

            return intervals, semitones

        elif chord_type == '13sus4' :
            chord = parse_chord(root + '13')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            root_pitch = chord.root().pitchClass
            
            # Remove the third
            pcs = [pc for pc in pcs if pc != third_pitch]
            
            # Add the P4 (5 semitones above root)
            P4_pitch = (root_pitch + 5) % 12
            pcs.insert(1, P4_pitch)
            

        elif chord_type == '9sus4':
            chord = parse_chord(root + '9')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            root_pitch = chord.root().pitchClass
            
            # Remove the third
            pcs = [pc for pc in pcs if pc != third_pitch]
            
            # Add the P4 (5 semitones above root)
            P4_pitch = (root_pitch + 5) % 12
            pcs.insert(1, P4_pitch)
            
            
        elif chord_type == '13no3':
            chord = parse_chord(root + '13')
            pcs = [p.pitchClass for p in chord.pitches]
            
            third_pitch = chord.third.pitchClass
            pcs = [pc for pc in pcs if pc != third_pitch]
            

        elif chord_type == '7no5': 
            chord = parse_chord(root + '7')
            pcs = [p.pitchClass for p in chord.pitches]
            
            fifth_pitch = chord.fifth.pitchClass
            pcs = [pc for pc in pcs if pc != fifth_pitch]
            

        elif chord_type == 'M7no5':
            chord = parse_chord(root + 'M7')
            pcs = [p.pitchClass for p in chord.pitches]
            
            fifth_pitch = chord.fifth.pitchClass
            pcs = [pc for pc in pcs if pc != fifth_pitch]

        else:
            chord = parse_chord(label)
            pcs = [p.pitchClass for p in chord.pitches]
    
        
        intervals, semitones = get_intervals_semitones_from_root(pcs)
            
        
        return intervals, semitones

    except Exception as e:
        #print(f'{chord_type}, {label},{e}')
        return np.nan, np.nan

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

import math

# Takes list of pc and returns int (normalized dissonance index of pitch class set)
def label_to_dissonance(label):
    try:

        intervals, semitones = label_to_intervals_semitones(label)

        return semitones_to_dissonance(semitones)
    
    except Exception as e:
        #print(f"{label} : {e}")
        return np.nan

def semitones_to_dissonance(semitones):

    try: 
        semitones = [item % 12 for item in semitones]
    
        p = len(semitones)
        num_notes = (1+math.sqrt(1+8*p))/2
        dissonance = (sum([dissonance_table[i] for i in semitones])) / num_notes
        
        return dissonance
        
    except Exception as e:
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
            
        data[key] = subset_row.iloc[0][['interval', 'interval from root', 'duration_qb']]
        
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

import re

def split_harmony_label(label):
    
    match = re.match(r'^([A-G][b#-]*)(.*)', label)
    if match:
        root = match.group(1)
        chord_type = match.group(2)
        return root, chord_type
    else:
        # If it doesn't match, return None for both
        return None, None 
        
def incompatible_label(df):
    results_list = []

    for _, row in df.iterrows():

        label = row['label']

        intervals, semitones = label_to_intervals_semitones(label)
            
        if isinstance(intervals, float) and np.isnan(intervals):

            root, chord_type = split_harmony_label(label)

            results_list.append(chord_type)

    results = pd.Series(results_list).value_counts()

    return results


    
    
