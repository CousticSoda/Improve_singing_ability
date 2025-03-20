# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:37:59 2025

@author: Kaito_Akahori
"""

import librosa
import soundfile as sf
import scipy.signal
import os

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut /nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    filtered_data = scipy.signal.filtfilt(b, a, data)
    return filtered_data

audio, sr = librosa.load(r'C:\Users\Kaito_Akahori\.spyder-py3\YourUnknownStory.wav', sr=None)

filtered_audio = bandpass_filter(audio, lowcut=80, highcut=3000, fs=sr, order=6)

sf.write('bandpass_YourUnknownStory.wav', filtered_audio, sr)

print("バンドパスフィルタ処理が完了し、 'bandpass_YourUnknownStory.wav'に保存されました。")

print("現在の作業ディレクトリ:", os.getcwd()) 