import os

import filter
import finger_predict
import mel
import split_wav


# 待传入参数


def finger_login_main(raw_wav, user_phone):
    unfilter_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/" \
                    "src/model/fingerprint_model/models/raw_wav/" + user_phone + "/" + raw_wav + ".wav"
    filter_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/" \
                  "src/model/fingerprint_model/models/raw_wav/" + user_phone + "/" + raw_wav + "_filtered.wav"
    wav_path = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/" \
               "src/model/fingerprint_model/models/wav/" + user_phone + "/"
    pic_dir = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/" \
              "src/model/fingerprint_model/models/pic/" + user_phone + "/test/"
    os.makedirs(pic_dir, exist_ok=True)
    train_dir = "D:/social/QQ/files/1448931856/FileRecv/sapas_app_back/" \
                "src/model/fingerprint_model/models/pic/" + user_phone + "/"

    filtered_wav = filter.filter_main(unfilter_path, filter_path)
    split_wav_dirs = split_wav.split_wav(filtered_wav, wav_path)

    img_dir = mel.mel_main(split_wav_dirs, pic_dir)
    flag = finger_predict.finger_train_main(user_phone, train_dir)
    return True
