import mido 
from mido import Message, MidiFile, MidiTrack, MetaMessage

def create_test_midi(output_path='sampleMIDI.mid'):
    #新しいMIDIファイルをタイプ１で作成
    mid = MidiFile(type=1)
    
    #トラックを１つ作る
    track = MidiTrack()
    mid.tracks.append(track)
    
    #1)テンポの設定(120 BPM)
    # 1拍あたりのマイクロ秒数を120で計算
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120), time=0))
    
    #2)トラック名(メタメッセージ)
    track.append(MetaMessage('track_name', name='Test Track', time=0))
    
    #3)最初のノート(Middle C = note=60)
    # - note_on(time=0で、　すぐなり始める)）
    track.append(Message('note_on', note=60, velocity=64, time=0))
    # -note_off(480ticks後にオフ)
    # -480ticksは、ticks_per_beat=480を想定すると１拍(四分音符)*一拍分
    track.append(Message('note_off', note=60, velocity=64, time=480))
    
    # 4)二つ目のノート(E = note =64)
    # -直後のtime=0で鳴らし始めると、前のノート終了時刻から連続になる
    track.append(Message('note_on', note=64, velocity=64, time=0))
    # - 再び一拍分ならしてnote_off
    track.append(Message('note_off', note=64, velocity=64, time=480))
    
    #5)(終了マーカーはmidoが自動で入れてくれます)
    # ファイル保存
    mid.save(output_path)
    print(f"Saved'{output_path}'")
    
if __name__ == '__main__':
    create_test_midi('sampleMIDI.mid')