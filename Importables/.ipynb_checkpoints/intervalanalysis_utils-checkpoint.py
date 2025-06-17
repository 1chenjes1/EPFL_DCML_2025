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

        intervals, semitones = get_intervals(pcs)
        
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

# takes df and returns data dict with songs and artists
def create_data(df):
    data = {}
    songs = []
    artists = []
    
    for row in range(df.shape[0]):
        df_row = df.iloc[[row]]
        worktitle = df_row.iloc[0]['workTitle']
        
        if worktitle not in songs:
            songs.append(worktitle)
        
        
        artist = (df_row.iloc[0]['artist'])
    
        if artist not in artists:
            artists.append(artist)
    
        key = (worktitle, artist)
        data[key] = df_row.iloc[0][['interval', 'duration_qb']]
        
    return songs, artists, data
    
# takes list, list, dict
def plot_interval_distribution(songs, artists, data):
    # Create figure with 2 subfigures
    fig = plt.figure(figsize=(12, 9), constrained_layout=True)
    subfigs = fig.subfigures(nrows=2, ncols=1)

    for i, song in enumerate(songs):
        subfig = subfigs[i]
        subfig.suptitle(f'{song}', fontsize=14)
        axs = subfig.subplots(nrows=1, ncols=2)

        for j, artist in enumerate(artists):
            ax = axs[j]
            
            # Extract pitch profile data for (song, artist)
            interval = data[(song, artist)]
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
            ax.set_title(f'Artist: {artist}')
            ax.set_xlabel('Interval')
            ax.set_ylabel('Percentage')

    fig.suptitle('Harmony Label Interval Distribution of 2 Songs by 2 Artists', fontsize=16)
    plt.show()
