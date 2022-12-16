
import numpy as np
import os
from scipy.io import wavfile
import scipy.signal

#常量设置
lowcut = 3000
highcut = 15000
FRAME_RATE = 44100




def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = scipy.signal.lfilter(b, a, data)
    return y

def bandpass_filter(buffer):
    return butter_bandpass_filter(buffer, lowcut, highcut, FRAME_RATE, order=6)




def getwavfiles(path):
    wav = []
    for root, _, files in os.walk(path):
        for file in files:
            wav.append(os.path.join(path, file))
    return wav



def filtered_write(wave,filtered_path):
    print(wave)
    print(os.path.join(wave))
    samplerate, data = wavfile.read(os.path.join(wave))

    assert samplerate == FRAME_RATE
    filtered = np.apply_along_axis(bandpass_filter, 0, data).astype('int16')
    print(222222)
    print(wave)
    #print(wave.split("/")[3])
    wavfile.write(os.path.join(filtered_path+wave), samplerate, filtered)










def filter_main(root,filtered_path):
    print(root)

    #wavs = getwavfiles(root)
    # for wav in wavs:
    #     print(wav)
    #     print(11111111111111)
    filtered_write(root,filtered_path)
    print("过滤完毕")
    #传给split
    print(filtered_path)
    return filtered_path
