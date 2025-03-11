[y1,fs1] = audioread('change_gakki.wav');
if size(y1, 2) > 1   %モノラル↔ステレオ　変換
    y1 = mean(y1, 2);
end
t1 =  (0:length(y1)-1) / fs1;

[y2, fs2] = audioread('spectrum_reduced.wav');
if size(y2, 2) > 1
    y2 = mean(y2, 2);
end
t2 = (0:length(y2)-1) / fs2;

figure;

%ファイル1の波形の表示
subplot(2,2,1);
plot(t1, y1);
xlabel('time(s)');
ylabel('Amplitude');
title('Waveform: change_gakki');

%ファイル2の波形
subplot(2,2,2);
plot(t2, y2);
xlabel('Time(s)');
ylabel('Amplitude');
title('Waveform: spectrum_reduced');

%ファイル1のスペクトログラム表示
subplot(2,2,3);
spectrogram(y1, 1024, 512, 1024, fs1, 'yaxis');
title('Spectrogram: change_gakki');
colorbar;

%ファイル2のスペクトログラム表示
subplot(2,2,4);
spectrogram(y2, 1024, 512, 1024, fs2, 'yaxis');
title('Spectrogram: spectrum_reduced');
colorbar;