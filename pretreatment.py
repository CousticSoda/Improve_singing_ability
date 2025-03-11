# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 19:36:54 2025

@author: Kaito_Akahori
"""

import numpy as np
import soundfile as sf
import noisereduce as nr
import scipy.signal
from spleeter.separator import Separator

#1. オリジナル録音ファイルの読み込み(ステレオ保持)
audio, sr = sf.read('your_unknown_story.wav')

#2. ボーカル分離：spleeterを使い、2ステム(ボーカル＋伴奏に分離)
separator = Separator('spleeter:2stems')
prediction = separator.separate(audio)
#分離結果は辞書形式で返される
#'vocals' : ボーカル成分, 'accompaniment' : 伴奏成分
vocal_audio = prediction['vocals'] #shape: (n_samples, n_channels)

#※今後の処理はモノラルで扱うため、左右平均してモノラル化
if vocal_audio.ndim == 2:
    vocal_mono = np.mean(vocal_audio, axis=1)
else:
    vocal_mono = vocal_audio
    
#3.ノイズ除去：最初の０．５秒をノイズプロファイルとして使用
noise_sample = vocal_mono[0:int(0.5 * sr)]
reduced_audio = nr.reduce_noise(y=vocal_mono, sr=sr, y_noise=noise_sample)

#4.　バンドパスフィルタ処理:人の声の主要帯域(例：80Hz~3000Hz) を抽出
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut /nyq
    b, a = scipy.signal.butter(order, [low, high], btype ='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = scipy.signal.filtfilt(b, a, data)
    return filtered_data

filtered_audio = bandpass_filter(reduced_audio, lowcut=80, highcut=3000, fs=sr, order=6)

#5.　前処理後の結果をWAVファイルとして保存
sf.write('preprocessed_vocal.wav', filtered_audio, sr)

print("前処理(ボーカル分離、ノイズ除去、　バンドパスフィルタ)の完了。")