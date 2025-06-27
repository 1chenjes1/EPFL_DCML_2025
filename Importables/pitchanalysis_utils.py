import itertools
import pandas as pd
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import music21 as m21

def create_data(subset, identifier):
    data = {}

    for row in range(subset.shape[0]):
        subset_row = subset.iloc[[row]]

        if isinstance(identifier, (list, tuple)):
            key = tuple(subset_row.iloc[0][col] for col in identifier)
        else:
            key = subset_row.iloc[0][identifier]

        data[key] = subset_row.iloc[0][['note', 'tpc', 'duration']]
        
    return data

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
        ax.(count['note'], count['percentage'], color='skyblue', edgecolor='black')
        ax.set_xlabel('Pitch')
        ax.set_ylabel('Percentage')

    # Global figure title:
    fig.suptitle(f'Pitch Profiles by {identifier}', fontsize=16)
    
    if fig_name:
        plt.savefig(f"../Jessica-ERIP2025/Results/{fig_name}")

    plt.show()