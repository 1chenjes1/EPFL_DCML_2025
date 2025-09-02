import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

from Importables import General as g

canonical_intervals = [
    'd1', 'P1', 'm2', 'A1',  
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


# # Takes df and returns df with columns 'note' and 'pc' with all notes occurring at the same time as list
# def generate_pcs(df_raw):
#     pitchclass = df_raw.copy()
#     pitchclass = pitchclass.groupby(by=['order'])[['note', 'pc']].agg(list).reset_index()
#     pitchclass['pcs'] = pitchclass['pc'].apply(lambda x: list(set(x)))
#     return pitchclass
    
from functools import lru_cache

@lru_cache(maxsize=None)
def parse_chord(label):
    return m21.harmony.ChordSymbol(label)

from itertools import combinations
def get_intervals_semitones(pcs):
    """
    Returns intervals and semitones (mod 2 octaves) of every pairwise combo of given pitches

    Args:
        pcs: list of pitch strings or m21.pitch.Pitch objects

    Return:
        intervals: list of interval string
        semitones: list of semitone integers
    """
    
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
    """
    Returns intervals and semitones (mod 2 octaves) starting from root note given pitches

    Args:
        pcs: list of pitch strings or m21.pitch.Pitch objects

    Return:
        intervals: list of interval string
        semitones: list of semitone integers
    """
    
    
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
    """
    Returns intervals and semitones (mod 2 octaves) of every pairwise combo of given pitches in label

    Args:
        label: String of label

    Return:
        intervals: list of interval string
        semitones: list of semitone integers
    """
    
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
    """
    Returns intervals and semitones (mod 2 octaves) from root of given pitches in label

    Args:
        label: String of label

    Return:
        intervals: list of interval strings
        semitones: list of semitone integers
    """
    
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

def label_to_dissonance(label):
    """
    Returns dissonance index of intervals in given label

    Args:
        label: String of label

    Return:
        float of dissonance index 
    """
    try:

        intervals, semitones = label_to_intervals_semitones(label)

        return semitones_to_dissonance(semitones)
    
    except Exception as e:
        #print(f"{label} : {e}")
        return np.nan

def semitones_to_dissonance(semitones):
    """
    Returns dissonance index of semitones

    Args:
        semitones: list of integers

    Return:
        float of dissonance index 
    """
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

import re

def split_harmony_label(label):
    """
    Returns harmony label split into root and chord type

    Args:
        label: string of label

    Return:
        root: string of root of chord
        chord type: string of chord type
    """
    
    match = re.match(r'^([A-G][b#-]*)(.*)', label)
    if match:
        root = match.group(1)
        chord_type = match.group(2)
        return root, chord_type
    else:
        # If it doesn't match, return None for both
        return None, None 
        
# def incompatible_label(df):
#     results_list = []

#     for _, row in df.iterrows():

#         label = row['label']

#         intervals, semitones = label_to_intervals_semitones(label)
            
#         if isinstance(intervals, float) and np.isnan(intervals):

#             root, chord_type = split_harmony_label(label)

#             results_list.append(chord_type)

#     results = pd.Series(results_list).value_counts()

#     return results

def plot_interval_distribution(data_df, title, method):
    """
    Returns figure of interval distrbution from given dataframe

    Args:
        data_df: pd.DataFrame, usually general.load_harmonies or general.load_labels generated df
        title: String, plot title
        method: 'pairwise' or 'from root'

    Return:
        fig, ax
    """
    
    if method == 'pairwise':
        col_name = 'interval'
    elif method == 'from root':
        col_name = 'interval from root'
    else:
        raise ValueError(f"Unknown method: {method}, method must be 'pairwise' or 'from root'")

    
    baseline_df = pd.DataFrame({
        col_name: canonical_intervals,
        'percentage': 0.0
    })

    fig, ax = plt.subplots(figsize=(15, 6))  # One figure and one axis

    colors = plt.colormaps['viridis']
    
    year_bins = sorted(
                data_df["year_bin"].unique(),
                key=lambda x: int(str(x).split("-")[0])
            )
    
    for i, year in enumerate(year_bins):
        subset = data_df[data_df['year_bin'] == year]            
        interval = subset[[col_name, 'duration_qb']]
        interval = interval.explode(col_name)
    
        interval_counts = (
            interval.groupby([col_name])['duration_qb']
            .sum()
            .reset_index(name='weighted_count')
        )
    
        #interval_counts['semitone'] = interval_counts['interval'].apply(lambda x: m21.interval.Interval(x).semitones)
        interval_counts['semitone'] = interval_counts[col_name].map(interval_order)
        count = interval_counts.sort_values('semitone', ascending=True)
        total = count['weighted_count'].sum()
        
        #Normalize
        count['percentage'] = (count['weighted_count'] / total)*100
    
        merged_df = pd.merge(
            baseline_df[[col_name]],
            count[[col_name, 'percentage']],
            on=col_name,
            how='left'
        )
    
        # Fill NaNs with 0 where artist didn't have that interval
        merged_df['percentage'] = merged_df['percentage'].fillna(0)
        
        merged_df = merged_df[[col_name, 'percentage']]
        
        # Plot bar chart
        ax.plot(merged_df[col_name], merged_df['percentage'], color=colors(i / (len(year_bins) - 1)), alpha=0.5)
        ax.scatter(merged_df[col_name], merged_df['percentage'], label=year, color=colors(i / (len(year_bins) - 1)))
    
    ax.tick_params(axis='x', labelsize=14, rotation=45)
    ax.tick_params(axis='y', labelsize=14)
    ax.set_xlabel('Interval', fontsize=16)
    ax.set_ylabel('Percentage %', fontsize=16)
    ax.set_title(title, fontsize=19)
    ax.legend(title='Recording Year', fontsize=14)
    ax.set_ylim(0, 25)

    return fig, ax

def notes_to_dissonance(notes):
    """
    Returns dissonance index of intervals from given notes

    Args:
        notes: list of notes string

    Return:
        float of dissonance index 
    """
    
    pcs = []
    for n in notes:
        n = g.fix_flats(n)
        n_m21 = m21.note.Note(n)
        pcs.append(n_m21.pitch.pitchClass) 

    intervals, semitones = get_intervals_semitones(pcs)
    return semitones_to_dissonance(semitones)

def plot_dissonance(ILC_major, ILC_minor, title):
    """
    Returns figure of plotted dissonance indices for individual scores + mean over time (years)

    Args:
        ILC_major: pd.Dataframe of major key scores' dissonance 
        ILC_minor: pd.Dataframe of minor key scores' dissonance 
        title: String, title of plots

    Return:
        fig, axes
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # Plot major
    axes[0].scatter(ILC_major['recording_year'], ILC_major['dissonance'], s=50)
        
    axes[0].plot(ILC_major.groupby(by='year_bin', as_index=False).mean()['recording_year'], 
                 ILC_major.groupby(by='year_bin', as_index=False).mean()['dissonance'], color="red")
    axes[0].set_title(f'{title} (Major)', fontsize=19)
    axes[0].set_xlabel('Recording Year', fontsize=16)
    axes[0].set_ylabel('Dissonance Index', fontsize=16)
    axes[0].grid(True, linestyle='--', alpha=0.3)
    axes[0].tick_params(axis='both', which='major', labelsize=14)
    
    
    # Plot minor
    axes[1].scatter(ILC_minor['recording_year'], ILC_minor['dissonance'], s=50)
        
    axes[1].plot(ILC_minor.groupby(by='year_bin', as_index=False).mean()['recording_year'], 
                 ILC_minor.groupby(by='year_bin', as_index=False).mean()['dissonance'], color="red")
    axes[1].set_title(f'{title} (Minor)', fontsize=19)
    axes[1].set_xlabel('Recording Year', fontsize=16)
    axes[1].grid(True, linestyle='--', alpha=0.3)
    axes[1].tick_params(axis='both', which='major', labelsize=14)

    return fig, axes
    
    
