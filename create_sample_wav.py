import mido
from mido import Message, MidiFile, MidiTrack

notes = [
    (60, 1),
    (60, 1),
    (67, 1),
    (67, 1),
    (69, 1),
    (69, 1),
    (67, 1),
    (65, 1),
    (65, 1),
    (64, 1),
    (64, 1),
    (62, 1),
    (62, 1),
    (60, 2)
 ]

#MIDIファイルの作成
mid = MidiFile(ticks_per_beat=480)
track = MidiTrack()
mid.tracks.append(track)

#テンポ設定(例: 120BPM)
tempo = mido.bpm2tempo(120)
track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

#各ノートをMIDIイベントに変換
for note, duration in notes:
    #note_on イベント
    track.append(Message('note_on', note=note, velocity=64, time=0))
    #拍数をticksに変換してnote_offイベントを設定
    duration_ticks = int(duration * mid.ticks_per_beat)
    track.append(Message('note_off', note=note, velocity=64, time=duration_ticks))
    
    #MIDIファイルとして保存
    mid.save('kaeru_no_uta.mid')