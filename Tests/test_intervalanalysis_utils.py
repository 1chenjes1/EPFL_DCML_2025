import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import General as g
from Importables import pitchanalysis_utils as pa
from Importables import intervalanalysis_utils as ia

def test_dissonance_2():
    result = 0.76
    harmony = [11,3,6,9,1]
    assert result == ia.dissonance(harmony)


## TESTING HARMONY LABELS

HI = g.load_df
base = HI[(HI['fnames'] == 'Snarky_Puppy-Shapons_Vindaloo') & (HI['rel_paths'] == 'by_Alexander_Booker')]
base = base.iloc[4:6]

def test_harmonyint_1():
    result = pd.DataFrame({
        'onset_time': [0, 2, 4, 5, 7],
        'harmony': [0.0, 1.0, 2.5, 3.0, 4.0],
        'end': [3.0, 5.0, 4.0, 6.0, 7.0]
    })