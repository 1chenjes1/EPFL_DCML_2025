from music21 import converter, metadata, key
import pandas as pd

def beat_to_frac(beat_in_measure, timesig):
    beats_per_measure = timesig.numerator
    beat_fraction = (beat_in_measure - 1)/ beats_per_measure
    return beat_fraction
    
def get_notes(rel_paths, fnames):
    
    base_path = "/Users/Jessica/Documents/ERIP2025/Jessica-ERIP2025/jazz_transcriptions"
    xml_path =  base_path + "/" + rel_paths + "/" + fnames + ".xml"
    # === Load your MusicXML file ===
    score = converter.parse(xml_path)  # <-- replace with your filename
    
    # === Prepare rows ===
    rows = []
    
    # === Iterate over parts ===
    for part in score.parts:
        part_name = part.partName if part.partName else 'Unknown Part'
        
        # Iterate over all notes/chords in this part
        for n in part.recurse().notes:
            measure_num = n.measureNumber  # SAFE and consistent
            beat_in_measure = n.beat
            timesig = n.getContextByClass('TimeSignature')
            beat_frac = beat_to_frac(beat_in_measure, timesig)
            abs_time = measure_num + beat_frac
            duration = n.quarterLength
            
            # Handle Note
            if n.isNote:
                row = {
                    'time': abs_time,
                    'measure': measure_num,
                    'beat': beat_in_measure,
                    'part': part_name,
                    'midi': n.pitch.midi,
                    'spelled_pitch': n.name,
                    'duration': duration
                }
                rows.append(row)
            
            # Handle Chord (multiple pitches)
            elif n.isChord:
                for p in n.pitches:
                    row = {
                        'time': abs_time,
                        'measure': measure_num,
                        'beat': beat_in_measure,
                        'part': part_name,
                        'midi': p.midi,
                        'spelled_pitch': p.name,
                        'duration': duration
                    }
                    rows.append(row)
    
    # === Build DataFrame ===
    df = pd.DataFrame(rows)
    df = df.sort_values(by=['time', 'part', 'midi']).reset_index(drop=True)
    
    # === Extract metadata ===
    md = score.metadata
    artist = md.composer if md and md.composer else 'Unknown'
    title = md.title if md and md.title else 'Unknown'
    year = md.date if md and md.date else 'Unknown'
    
    # === Extract key ===
    key_sig = None
    for ks in score.recurse().getElementsByClass('KeySignature'):
        key_sig = ks
        break
    
    if key_sig:
        detected_key = key_sig.asKey().name
    else:
        detected_key = score.analyze('key').name
    
    # === Add metadata to df.attrs ===
    df.attrs['artist'] = artist
    df.attrs['title'] = title
    df.attrs['year'] = year
    df.attrs['key'] = detected_key
    df.attrs['rel_paths'] = rel_paths
    df.attrs['fnames'] = fnames
    
    return df
