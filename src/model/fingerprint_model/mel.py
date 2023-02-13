import os
import time

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            wav.append(os.path.join(path, file))
    return wav


def waveplot(file):
    x, fs = librosa.load(file)
    librosa.display.waveshow(x, sr=fs)

    print(x.shape)
    return x, fs


def mfcc(x, fs):
    mel_spect = librosa.feature.melspectrogram(x, sr=fs, n_fft=2048, hop_length=1024)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

    return mel_spect


def scalemfcc(mfccs, fs):
    # mfccs = sklearn.preprocessing.scale(mfccs, axis=1)

    return mfccs


def drawspec(mfcc, savename, savepath):
    plt.figure(figsize=(10, 4))
    # log
    librosa.display.specshow(mfcc, x_axis='time', y_axis='mel', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    print("savepath+savename")
    print(savepath + savename)
    print(savename)
    plt.savefig(savepath + str(time.time()) + '.png')


def drawspec2(mfcc, savename, savepath):
    plt.figure(figsize=(10, 4))
    # log
    librosa.display.specshow(mfcc, x_axis='time', y_axis='mel', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    print("savepath+savename")
    print(savepath + savename)
    print(savename)
    plt.savefig(savepath + str(time.time()) + '.png')


def mel_main(root, pic_dir, pic_val_dir):
    wavs = getwavfiles(root)

    for wav in wavs:
        x, fs = waveplot(wav)
        mfccs = mfcc(x, fs)
        mfccs = scalemfcc(mfccs, fs)
        drawspec(mfccs, wav.replace(".wav", ".png"), pic_dir)
        drawspec2(mfccs, wav.replace(".wav", ".png"), pic_val_dir)
    print("mel完毕")
    return pic_dir
