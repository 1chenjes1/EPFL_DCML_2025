import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

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

# Takes df and returns df with column 'dissonance' which calculates normalized dissonance index of each harmony
def dissonance(pc):
    harmonies = pc[pc['pc'].apply(lambda x: len(x) > 1)].copy()
    harmonies['interval'] = harmonies['pc'].apply(interval_class)
    harmonies['num notes'] = harmonies['pc'].apply(lambda x: len(x))
    harmonies['dissonance'] = (
        harmonies['interval'].apply(lambda x: sum(dissonance_table[i] for i in x))
    ) / harmonies['num notes']
    return harmonies

dissonance_table = {
    0: 0.0,    # Unison
    1: 1.0,    # m2/M7
    2: 0.6,    # M2/m7
    3: 0.4,    # m3/M6
    4: 0.2,    # M3/m6 
    5: 0.0,    # P4/P5
    6: 0.8,    # Tritone
}