# Excellence Research Internship Program 2025: Digital and Cognitive Musicology Lab

This project explores pitch, interval, and chord distributions across music history.  
It uses `music21`, `scikit-learn` and other Python libraries for an exploratory analysis of the jazz transcriptions corpus, as well as comparisons between the jazz corpus with the classical corpus.

---

## Notebooks Overview

**Note:** In all notebooks, the `sys.path.append(...)` line must be updated to match the path of this repository on your machine.

- **`0_data_preprocessing.ipynb`**  
  Plots the frequency of scores per year and per artist.

- **`1_pitch_distribution.ipynb`**  
  Analyzes pitch-class distributions across year bins. Generates plots of pitch
  frequencies (normalized to percentages).

- **`2_interval_analysis.ipynb`**  
  Examines musical intervals from sounding or in-label pitch classes. Intervals are calculated using two methods: pairwise and root-based. Produces weighted interval distributions over time.

- **`3_dissonance.ipynb`**  
  Calculates dissonance indices from sounding or in-label pitch classes. Also analyzes the ratio of chord tones vs non-chord tones. Produces the average dissonance index of each score, and the average per year bin. 

- **`4_chord_analysis.ipynb`**  
  Extracts the most used chords for each year bin, as well as what pitches are used during the chord.

- **`5_neo-riemannian_transformations.ipynb`**  
  Calculates frequencies of single and double neo-riemannian transformations for each year bin and artist.

- **`6_hierarchcial_clustering.ipynb`**  
  Takes Shapons Vindaloo by Snarky Puppy and performs agglomerative clusters pitch composition of each bar. Produces plots of the average pitch composition of each cluster.

- **`7_classical_analysis.ipynb`**  
  Produces pitch profile analysis and transformation frequencies over time on the classical corpus (dcml_corpora)

- **`8_PCA.ipynb`**  
  Performs dimensionality reduction (PCA and UMAP) visualizations on the per measure pitch profiles of the entire jazz corpus. Also performs hierarchical clustering using HDBSCAN to plot the optimal number of clusters and the resulting average cluster pitch profiles.

- **`/Importables/` folder**  
  Contains helper scripts for the jazz corpus (functions for classical corpora are found in notebook 7):
  - `pitchanalysis_utils.py` – functions for pitch distribution analysis  
  - `intervalanalysis_utils.py` – functions for interval calculations  
  - `General.py` – general helper functions including functions that load in the metadata, harmonies and notes
  - `tonnetz_utils.py` – functions for neo-riemannian transformation calculations
  - `clustering_utils.py` – functions for performing clustering 
