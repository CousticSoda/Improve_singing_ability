import noisereduce as nr
import librosa
import soundfile as sf

#録音ファイルの読み込み
audio, sr = librosa.load('your_unknown_story.wav', sr=None)

#ノイズプロファイルとして、録音の最初の数秒間を使用する
noise_sample = audio[0:int(0.5 * sr)]

#ノイズ除去処理
#nr.reduce_noise(録音ファイル, sr ,サンプルファイル)

reduced_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_sample)

sf.write('spectrum_reduced_your_unknown_story.wav', reduced_audio, sr)