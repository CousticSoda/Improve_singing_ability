import crepe
import librosa
import matplotlib.pyplot as plt

#1. 音声ファイルの読み込み(CREPEの推奨サンプリングレートは16kHz)
audio_file = 'sepa_YourUnknownStory.wav'
audio, sr = librosa.load(audio_file, sr=16000)

#2. CREPEによるピッチ推定
#   - step_size:推定するフレーム間隔
#   - viterbi: Trueにすると、 Viterbiアルゴリズムによる平滑化が適用されます
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

#3.結果の可視化
plt.figure(figsize=(10,4))
plt.plot(time, frequency, label='Estimated F0', color='b')
plt.xlabel('Time(s)')
plt.ylabel('Frequency(Hz)')
plt.title('CREPE Pitch Estimation')
plt.legend()
plt.show()