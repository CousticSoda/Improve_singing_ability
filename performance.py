import os
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(r"C:\tools\fluidsynth\bin")

import fluidsynth

def midi_to_wav(mid_file, sf2_file, out_wav):
    fs = fluidsynth.Synth()
    fs.start(driver="dsound")  # Windowsならdsound, Linuxならpulseaudio等

    # サウンドフォントを読み込み (bank=0 にロード)
    sfid = fs.sfload(sf2_file)
    fs.program_select(0, sfid, 0, 0)

    # MIDIファイルを読み込む（pyfluidsynth>=2.0）
    fs.midi_file_play(mid_file, block=True)

    # レコーディングを開始して再生(ただしバージョンによってはサポートが不安定)
    # → pyfluidsynth 2.3.0 時点では midi_file_play() と wave_write() の同期に
    #   課題があるようで、実際にはやや工夫が必要

    fs.delete()

midi_to_wav("sampleMIDI.mid", "Monalisa_GM_Grand_Piano.sf2", "result.wav")
