import mido
import matplotlib.pyplot as plt

# ティック（ticks）を秒（seconds）に変換する関数
def ticks_to_seconds(ticks, tempo, ticks_per_beat):
    """
    tempo: 1拍あたりのマイクロ秒数 (set_tempoイベント)
    ticks_per_beat: MidiFile().ticks_per_beat
    """
    # tempo は 1 拍 (quarter note) に要するマイクロ秒
    # 1 秒 = 1e6 マイクロ秒
    return (ticks * tempo) / (1_000_000.0 * ticks_per_beat)

# MIDIファイルを読み込む
mid = mido.MidiFile('output_sound2025.mid')

# 解析用にすべてのメッセージを単一リストにまとめる (トラックの区別をしない例)
all_messages = []
for track in mid.tracks:
    current_tick = 0
    for msg in track:
        current_tick += msg.time  # Delta timeを累積して絶対tickに
        # 新たに、絶対tickを保持する属性を付与してリスト化
        all_messages.append((current_tick, msg))

# tick順にソート (複数トラックをまとめたので安全のため)
all_messages.sort(key=lambda x: x[0])

# 変数の初期化
current_tempo = 500000  # デフォルト: 120bpm相当 (500,000マイクロ秒/拍)
notes_on = {}           # note_onが発生したノートを保持 (note番号→開始tick)
note_list = []          # (note, start_sec, end_sec) のリスト

for (abs_tick, msg) in all_messages:
    # テンポ変更があった場合は更新
    if msg.type == 'set_tempo':
        current_tempo = msg.tempo
    
    # note_on (velocity>0) → ノート開始
    if msg.type == 'note_on' and msg.velocity > 0:
        notes_on[msg.note] = abs_tick
    
    # note_off または velocity=0 の note_on → ノート終了
    if (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
        if msg.note in notes_on:
            start_tick = notes_on[msg.note]
            end_tick = abs_tick
            # ticks → seconds へ変換
            start_sec = ticks_to_seconds(start_tick, current_tempo, mid.ticks_per_beat)
            end_sec = ticks_to_seconds(end_tick, current_tempo, mid.ticks_per_beat)
            note_list.append((msg.note, start_sec, end_sec))
            del notes_on[msg.note]

# note_listには (ピッチ, 開始時刻[sec], 終了時刻[sec]) が格納された

# --- グラフ描画 ---
plt.figure(figsize=(10, 6))

for (note, start_sec, end_sec) in note_list:
    plt.hlines(note, start_sec, end_sec, color='blue', linewidth=2)

plt.xlabel('Time (seconds)')
plt.ylabel('MIDI Note Number')
plt.title('Piano Roll')
plt.grid(True)
plt.show()
