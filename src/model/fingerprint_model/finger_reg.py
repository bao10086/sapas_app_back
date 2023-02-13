import os
import time

from src.model.fingerprint_model import finger_train
from src.model.fingerprint_model import mel
from src.model.fingerprint_model import split_wav


# 待传入参数


def finger_reg_main(raw_wav, user_phone):
    tim_now = time.time()
    unfilter_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/raw_wav/" + user_phone + "/" + raw_wav
    # os.makedirs(unfilter_path, exist_ok=True)
    filter_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/filtered_wav/" + user_phone + "/"
    os.makedirs(filter_path, exist_ok=True)
    wav_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/wav/" + user_phone + "/"
    os.makedirs(wav_path, exist_ok=True)
    pic_dir = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/pic/" + user_phone + "/train/" + str(
        tim_now) + "/"
    os.makedirs(pic_dir, exist_ok=True)
    pic_val_dir = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/pic/" + user_phone + "/val/" + str(
        tim_now) + "/"
    os.makedirs(pic_val_dir, exist_ok=True)
    train_dir = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/src/model/fingerprint_model/models/pic/" + user_phone + "/"
    os.makedirs(train_dir, exist_ok=True)

    # filtered_wav=filter.filter_main(unfilter_path,filter_path)
    filtered_wav = unfilter_path
    split_wav_dirs = split_wav.split_wav(filtered_wav, wav_path)

    img_dir = mel.mel_main(split_wav_dirs, pic_dir, pic_val_dir)
    finger_train.finger_train_main(user_phone, train_dir, class_cnt=1)
    return True
