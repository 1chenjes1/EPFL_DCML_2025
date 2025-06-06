import sys
sys.path.append('/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/')

from Importables import pitchanalysis_utils as pa
from Importables import intervalanalysis_utils as ia

def test_dissonance_2():
    result = 0.76
    harmony = [11,3,6,9,1]
    assert result == ia.dissonance(harmony)