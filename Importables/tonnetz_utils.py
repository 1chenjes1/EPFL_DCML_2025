import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21
import ms3
from functools import lru_cache

# Check if 1) tonic is same and 2) third shifted up/down a semitone
def is_parallel(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is parallel

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if parallel transformation, False otherwise
    """
    
    common_pitches = set([l1.name, l3.name, l5.name]) & set([c1.name, c3.name, c5.name])
    if len(common_pitches) != 2:
        return False
        
    truth = (
        (l1 == c1) and 
        (l5 == c5) and 
        ((m21.interval.Interval(pitchStart=c3, pitchEnd=l3).semitones % 12 == 1) or (m21.interval.Interval(pitchStart=l3, pitchEnd=c3).semitones % 12 == 1))
    )
    return truth

# Check if 1) the tonic shifted down/up 3 st and 2) that the chord is minor/major
def is_relative(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is relative

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if relative transformation, False otherwise
    """
    
    common_pitches = set([l1.name, l3.name, l5.name]) & set([c1.name, c3.name, c5.name])
    if len(common_pitches) != 2:
        return False
        
    truth = (
        (
            (m21.interval.Interval(pitchStart=c1, pitchEnd=l1).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        ) or 
        (
            (m21.interval.Interval(pitchStart=l1, pitchEnd=c1).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)     
        )
    )
    return truth

# Check if 1) tonic shifted up/down 4 semitones and 2) chord is minor/major
def is_leading(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is leading

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if leading transformation, False otherwise
    """
    common_pitches = set([l1.name, l3.name, l5.name]) & set([c1.name, c3.name, c5.name])
    if len(common_pitches) != 2:
        return False
        
    truth = (
        (
            (m21.interval.Interval(pitchStart=l1, pitchEnd=c1).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        ) or 
        (
            (m21.interval.Interval(pitchStart=c1, pitchEnd=l1).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        )
    )
    return truth

# Check if 1) tonic shifted up/down 1 semitone and 2) chord is minor/major
def is_slide(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is slide

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if slide transformation, False otherwise
    """
    common_pitches = set([l1.name, l3.name, l5.name]) & set([c1.name, c3.name, c5.name])
    if len(common_pitches) != 1:
        return False
        
    truth = (
        (
            (m21.interval.Interval(pitchStart=l1, pitchEnd=c1).semitones % 12 == 1) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 3) and
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        ) or 
        (
            (m21.interval.Interval(pitchStart=c1, pitchEnd=l1).semitones % 12 == 1) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        )   
    )
    return truth

# Check if 1) tonic shifted down/up 7 semitones and 2) is minor/major
def is_nebenverwandt(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is nebenverwandt

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if nebenverwandt transformation, False otherwise
    """
    common_pitches = set([l1.name, l3.name, l5.name]) & set([c1.name, c3.name, c5.name])
    if len(common_pitches) != 1:
        return False
        
    truth = (
        (
            (m21.interval.Interval(pitchStart=c1, pitchEnd=l1).semitones % 12 == 7) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        ) or 
        (
            (m21.interval.Interval(pitchStart=l1, pitchEnd=c1).semitones % 12 == 7) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        )
    )
    return truth

# Check if 1) tonic shifted down/up by 4 semitones and 2) is minor/major
def is_hexpole(l1,l3,l5,c1,c3,c5):
    """
    Checks if transition between 2 chords is hexpole

    Args:
        l1: chord1 root, m21.pitch.Pitch
        l3: chord1 third, m21.pitch.Pitch
        l5: chord1 fifth, m21.pitch.Pitch
        c1: chord2 root, m21.pitch.Pitch
        c3: chord2 third, m21.pitch.Pitch
        c5: chord2 fifth, m21.pitch.Pitch

    Return:
        True if hexpole transformation, False otherwise
    """
    
    truth = (
        (
            (m21.interval.Interval(pitchStart=c1, pitchEnd=l1).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 3) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        ) or 
        (
            (m21.interval.Interval(pitchStart=l1, pitchEnd=c1).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c3).semitones % 12 == 4) and 
            (m21.interval.Interval(pitchStart=c1, pitchEnd=c5).semitones % 12 == 7)
        )
    )
    return truth


def transformation(labels):
    """
    Returns dataframe with single transformation information

    Args:
        labels: pd.DataFrame, generated from g.load_labels

    Return:
        df: pd.DataFrame with columns ['chord_1', 'chord_2', 'transformation', 'artist', 'fname', 'recording_year']
        exceptions: list of chord labels that threw exceptions (possibly not readable by music21)
    """
    
    rows_list = []
    exceptions = []

    unique_combos = labels[['artist', 'fnames']].drop_duplicates()
    
    for _, combo in unique_combos.iterrows():
        artist = combo['artist']
        fname = combo['fnames']

        subset = labels[
            (labels['artist'] == artist) &
            (labels['fnames'] == fname) 
        ]

        if subset.empty:
            print(f"{artist},{fname}")
            continue
        
        last_label_name = subset.iloc[0]['label']
        for index, row in subset.iterrows():
            try:
                recording_year = row['recording_year']
            except: 
                continue
                
            current_label_name = row['label']
            
            # look for different label
            if (current_label_name != last_label_name):
                result = None
                l1 = l3 = l5 = c1 = c3 = c5 = None 
    
                try:
                    result = None
                    last_label = m21.harmony.ChordSymbol(last_label_name)
                    l1 = last_label.root()
                    l3 = last_label.third
                    l5 = last_label.fifth
                except:
                    transformation = 'N/A'
                    if current_label_name not in exceptions:
                        exceptions.append(last_label_name)
    
                try:
                    current_label = m21.harmony.ChordSymbol(current_label_name)
                    c1 = current_label.root()
                    c3 = current_label.third
                    c5 = current_label.fifth
                except:
                    transformation = 'N/A'
                    if current_label_name not in exceptions:
                        exceptions.append(current_label_name)
        
                if None in (l1, l3, l5, c1, c3, c5):
                    transformation = 'N/A'
                elif current_label.isDiminishedTriad() or current_label.isAugmentedTriad():
                    transformation = 'N/A'
                    if current_label_name not in exceptions:
                        exceptions.append(current_label_name)
    
                elif last_label.isDiminishedTriad() or last_label.isAugmentedTriad():
                    transformation = 'N/A'
                    
                    if last_label_name not in exceptions:
                        exceptions.append(last_label_name)
                    
                # Parallel Case   
                elif is_parallel(l1,l3,l5,c1,c3,c5):
                    transformation = 'P'
    
                # Relative Case 
                elif is_relative(l1,l3,l5,c1,c3,c5):
                    transformation = 'R'
                    
                # Leading-Tone Exchange Case 
                elif is_leading(l1,l3,l5,c1,c3,c5):
                    transformation = 'L'
            
                # Slide Case 
                elif is_slide(l1,l3,l5,c1,c3,c5):
                    transformation = 'S'
                    
                # Nebenverwandt Case
                elif is_nebenverwandt(l1,l3,l5,c1,c3,c5):
                    transformation = 'N'
    
                # Hexpole case
                elif is_hexpole(l1,l3,l5,c1,c3,c5):
                    transformation = 'H'

                else:
                    # Check two-step sequence
                    seq = find_two_step_sequence(last_label_name, current_label_name)
                    if seq is not None:
                        transformation = seq
                    else:
                        transformation = 'N/A'
    
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': transformation,
                          'artist': artist,
                          'fname': fname,
                          'recording_year': recording_year
                         }
    
                    
                rows_list.append(result)        
                last_label_name = current_label_name
            
    df = pd.DataFrame(rows_list) 

    return df, exceptions

def P(chord):
    """
    Returns new chord after performing parallel transformation

    Args:
        chord: m21.chord.Chord object

    Return:
        Returns chord after performing transformation 
    """
    third = chord.third
    
    if chord.quality == 'major':
        new_third = third.transpose(-1)  
        new_chord = m21.chord.Chord([chord.root(), new_third, chord.fifth]) 
    elif chord.quality == 'minor':
        new_third = third.transpose(1)  
        new_chord = m21.chord.Chord([chord.root(), new_third, chord.fifth]) 
    else:
        return None  

    return new_chord

def R(chord):
    """
    Returns new chord after performing relative transformation

    Args:
        chord: m21.chord.Chord object

    Return:
        Returns chord after performing transformation 
    """
    root = chord.root()

    if chord.quality == 'major':
        i = m21.interval.Interval('-m3')
        new_root = root.transpose(i)  
        third = new_root.transpose('m3')
        fifth = new_root.transpose('P5')
        return m21.chord.Chord([new_root, third, fifth])
    elif chord.quality == 'minor':
        i = m21.interval.Interval('m3')
        new_root = root.transpose(i)  
        third = new_root.transpose('M3')
        fifth = new_root.transpose('P5')
        return m21.chord.Chord([new_root, third, fifth])
        
    return None


def L(chord):
    """
    Returns new chord after performing leading transformation

    Args:
        chord: m21.chord.Chord object

    Return:
        Returns chord after performing transformation 
    """
    root = chord.root()

    if chord.quality == 'major':
        i = m21.interval.Interval('M3')
        new_root = root.transpose(i)  
        third = new_root.transpose('m3')
        fifth = new_root.transpose('P5')
        return m21.chord.Chord([new_root, third, fifth])
    elif chord.quality == 'minor':
        i = m21.interval.Interval('-M3')
        new_root = root.transpose(i)  
        third = new_root.transpose('M3')
        fifth = new_root.transpose('P5')
        return m21.chord.Chord([new_root, third, fifth])

    return None

def chord_symbol_to_chord(chord_symbol_name):
    cs = m21.harmony.ChordSymbol(chord_symbol_name)
    pitches = cs.pitches 
    chord = m21.chord.Chord(pitches)
    return chord

def find_two_step_sequence(chord1_name, chord2_name):
    """
    Returns transformation pair between two chords

    Args:
        chord1_name: label1 string
        chord2_name: label2 string

    Return:
        Returns string of double transformation, None otherwise
    """
    chord1 = m21.harmony.ChordSymbol(chord1_name)
    chord2 = m21.harmony.ChordSymbol(chord2_name)
    transformations = {'P': P, 'R': R, 'L': L}

    for t1_name, t1_func in transformations.items():
        mid_chord = t1_func(chord1)

        if mid_chord is None:
            continue
        for t2_name, t2_func in transformations.items():
            mid_chord_copy = m21.chord.Chord([p for p in mid_chord.pitches])
            final_chord = t2_func(mid_chord_copy)
            if final_chord is None:
                continue
            try:
                if (final_chord.root().name == chord2.root().name and
                    final_chord.third.name == chord2.third.name and
                    final_chord.fifth.name == chord2.fifth.name):
                    return t1_name + t2_name
            except AttributeError:
                continue  # skip chords with missing components

    return None

def double_transformations(transformations):
    """
    Returns df with double transformation information

    Args:
        transformation: pd.DataFrame, generated by transformations()

    Return:
        Returns df with double transformations between chords added in 'transformation' column
    """
    rows_list = []
    exceptions = []
    for index, row in transformations.iterrows():
        chord1 = row['chord_1']
        chord2 = row['chord_2']
        artist = row['artist']
        fname = row['fname']
        recording_year = row['recording_year']
        try:
            dt = find_two_step_sequence(chord1, chord2)

            if dt is not None:
                result = {'chord_1': chord1, 
                          'chord_2': chord2,
                          'transformation': dt,
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }
            else:
                result = {'chord_1': chord1, 
                          'chord_2': chord2,
                          'transformation': 'N/A',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                     }
            
        except:
            result = {'chord_1': chord1, 
                      'chord_2': chord2,
                      'transformation': 'N/A',
                      'fname': fname,
                      'artist': artist,
                      'recording_year': recording_year
                     }

        rows_list.append(result)   

    df = pd.DataFrame(rows_list) 

    return df

def plot_transformation(df, transformation):
    """
    Returns plot of specified transformation frequencies (%) across year bins 

    Args:
        df:pd.DataFrame of transformation info, generated from transformations()
        transformation: string or list of string of transformations 

    Return:
        fig, ax
        P_results = pd.Dataframe with transformation frequency information
    """
    year_bins = sorted(
            df["year_bin"].unique(),
            key=lambda x: int(str(x).split("-")[0])
        )
    
    P_results = []

    for year in year_bins:
        subset_year = df[df['year_bin'] == year]
        tot_count = subset_year.shape[0]

        if isinstance(transformation, str):
            P_count = subset_year[subset_year['transformation'] == transformation].shape[0]
        elif isinstance(transformation, list):
            P_count = subset_year[subset_year['transformation'].isin(transformation)].shape[0]

        value = 100 * P_count / tot_count

        P_results.append({
            'year_bin': year,
            'value': value
        })

    P_results = pd.DataFrame(P_results)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(P_results['year_bin'], P_results['value'], color='skyblue')

    ax.set_xlabel('Year')

    ax.set_ylabel(f'% of {transformation} Transformations')

    ax.set_title(f'{transformation} Transformation Percents by Year', fontsize=19)
    ax.set_xticklabels(P_results['year_bin'], rotation=45)

    return fig, ax, P_results

def bar_plot_transformation(df_plot):
    """
    Returns plot of transformation frequencies (%) across year bins as stacked bar

    Args:
        df:pd.DataFrame of transformation info, generated from transformations()

    Return:
        fig, ax
    """
    year_bins = sorted(
            df_plot["year_bin"].unique(),
            key=lambda x: int(str(x).split("-")[0])
        )
    num_bins = len(year_bins)
    
    fig, ax = plt.subplots()
    current_itn = np.zeros(num_bins)
    counts = df_plot.value_counts(subset=['year_bin']).reset_index(name='count')
    counts = counts.sort_values('year_bin')
    tot_counts = counts['count']
    
    cmap = plt.cm.get_cmap('tab20')
    colors = [cmap(i) for i in range(len(df_plot['transformation'].unique()))]
    
    for i, transformation in enumerate(df_plot['transformation'].unique()):
        transformation_subset = df_plot[df_plot['transformation']== transformation]
        transformations_subset_grouped = (
            transformation_subset.groupby('year_bin')
            .size()
            .reindex(year_bins, fill_value=0)
            .reset_index(name='count')
        )
        
        y = transformations_subset_grouped['count'] 
        y = np.array(y) * 100/tot_counts
    
        ax.bar(year_bins, y, bottom = current_itn, label=transformation, color=colors[i])
    
        current_itn = current_itn + y
    
        ax.set_xticks(np.arange(num_bins))
        ax.set_xlabel('Year')
        ax.set_ylabel('%')
        ax.set_xticklabels(year_bins,rotation=45)
    
    plt.suptitle('Jazz Transformations Frequencies', fontsize=19)
    plt.legend(bbox_to_anchor=(1.01,0.5), loc='center left')

    return fig, ax
