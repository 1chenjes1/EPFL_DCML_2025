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
    truth = (
        (l1 == c1) and 
        (l5 == c5) and 
        ((m21.interval.Interval(pitchStart=c3, pitchEnd=l3).semitones % 12 == 1) or (m21.interval.Interval(pitchStart=l3, pitchEnd=c3).semitones % 12 == 1))
    )
    return truth

# Check if 1) the tonic shifted down/up 3 st and 2) that the chord is minor/major
def is_relative(l1,l3,l5,c1,c3,c5):
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
    last_label_name = labels.iloc[0]['label']
    for index, row in labels.iterrows():
        current_label_name = row['label']
        # look for different label
        if (current_label_name != last_label_name):
            result = None
            last_label = m21.harmony.ChordSymbol(last_label_name)
            l1 = last_label.root()
            l3 = last_label.third
            l5 = last_label.fifth
            current_label = m21.harmony.ChordSymbol(current_label_name)
            c1 = current_label.root()
            c3 = current_label.third
            c5 = current_label.fifth

            # Parallel Case
            if is_parallel(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'P'
                         }

            # Relative Case 
            elif is_relative(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'R'
                         }
                
            # Leading-Tone Exchange Case 
            elif is_leading(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'L'
                         }

        
            # Slide Case 
            elif is_slide(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'S'
                         }
                
            # Nebenverwandt Case
            elif is_nebenverwandt(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'N'
                         }

            # Hexpole case
            elif is_hexpole(l1,l3,l5,c1,c3,c5):
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'H'
                         }
            
            # No transformation Case
            else:
                result = {'chord_1': last_label_name, 
                          'chord_2': current_label_name,
                          'transformation': 'N/A'
                         }
                
            last_label_name = current_label_name

            rows_list.append(result)

    df = pd.DataFrame(rows_list) 

    return df 