from pydub import AudioSegment
import librosa

#待传入文件
#单个文件

#切割后音频存储路径




def split_wav(wav,wav_path):
    x, sr = librosa.load(wav)
    L = len(x)
    print('Time:', L / sr)
    print("正在切割音频")
    t1 = 0.3 * 1000 
    t2 = 0.6 * 1000
    while max(t1,t2)< L *1000/sr:
        newAudio = AudioSegment.from_wav(wav)
        newAudio = newAudio[t1:t2]
        newAudio.export(wav_path+str(t1/1000)+str(t2/1000)+'.wav', format="wav")
        t1=t2
        t2=t2+0.3*1000
    return wav_path


