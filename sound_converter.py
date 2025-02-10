import librosa
import numpy as np
import mido
import math

def detect_pitch(input_wav):
    #音声ファイル読み込み
    y, sr = librosa.load(input_wav)
    #ピッチ検出
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    pitch_values = []
    for i in range(pitches.shape[1]):
        idx = np.argmax(magnitudes[:,i])
        pitch = pitches[idx, i]
        pitch_values.append(pitch)
        
    return pitch_values


def freq_to_midi_note(freq):
    if freq <= 0:
        return 0
    note = 69 + 12 * math.log2(freq/440.0)
    return int(round(note))

def pitches_to_midi(pitch_values, out_mid="output_sound2025.mid"):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    #テンポ設定(120 BPM)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120),time=0))
    
    time_per_slice = 0.1
    for pitch in pitch_values:
        note_number = freq_to_midi_note(pitch) if pitch > 0 else 0
        if note_number > 0:
            track.append(mido.Message('note_on', note=note_number, velocity=64, time=0))
            #0.1秒後にnote_off
            dt = mido.second2tick(time_per_slice, mid.ticks_per_beat, mido.bpm2tempo(120))
            track.append(mido.Message('note_off', note=note_number, velocity=64, time=int(dt)))
        else:
            #無音スライス
            dt = mido.second2tick(time_per_slice, mid.ticks_per_beat, mido.bpm2tempo(120))
            track.append(mido.Message('note_off', note=0, velocity=0, time=int(dt)))
            
    mid.save(out_mid)
    print(f"saved{out_mid}")

if __name__ == '__main__':
    pitch_values = detect_pitch("sound2025.wav")
    pitches_to_midi(pitch_values, out_mid="output_sound2025.mid")
