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
    rows_list = []
    exceptions = []
    last_label_name = labels.iloc[0]['label']
    for index, row in labels.iterrows():
        artist = row['artist']
        fname = row['fnames']
        recording_year = row['recording_year']
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
                result = {'chord_1': last_label_name, 
                              'chord_2': current_label_name,
                              'transformation': 'N/A',
                              'fname': fname,
                              'artist': artist,
                              'recording_year': recording_year
                             }
                if current_label_name not in exceptions:
                    exceptions.append(last_label_name)

            try:
                current_label = m21.harmony.ChordSymbol(current_label_name)
                c1 = current_label.root()
                c3 = current_label.third
                c5 = current_label.fifth
            except:
                result = {'chord_1': last_label_name, 
                              'chord_2': current_label_name,
                              'transformation': 'N/A',
                              'fname': fname,
                              'artist': artist,
                              'recording_year': recording_year
                             }
                if current_label_name not in exceptions:
                    exceptions.append(current_label_name)
    
            if None in (l1, l3, l5, c1, c3, c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'N/A',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }
                
            # Parallel Case   
            elif is_parallel(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'P',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }

            # Relative Case 
            elif is_relative(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'R',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }
                
            # Leading-Tone Exchange Case 
            elif is_leading(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'L',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }

        
            # Slide Case 
            elif is_slide(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'S',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }
                
            # Nebenverwandt Case
            elif is_nebenverwandt(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'N',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }

            # Hexpole case
            elif is_hexpole(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'H',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }
            
            # No transformation Case
            else:
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'N/A',
                          'fname': fname,
                          'artist': artist,
                          'recording_year': recording_year
                         }

                
            rows_list.append(result)        
            last_label_name = current_label_name
            
    df = pd.DataFrame(rows_list) 

    return df,exceptions 