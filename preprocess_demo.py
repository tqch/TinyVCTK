import numpy as np
from scipy.io import wavfile
import os
import math

data_dir = "."
train_folder = "clean_trainset_wav_16k"
test_folder = "clean_testset_wav_16k"

input_bit_depth = 16
output_bit_depth = 8
input_levels = 2**input_bit_depth
output_levels = 2**output_bit_depth


def mu_law_encode(x):
    input_levels = 2**input_bit_depth
    output_levels = 2**output_bit_depth
    # assume the possible values are centered at 0
    x = x / (input_levels // 2)  # elements of x now lie within [-1, 1]
    # mu-law transformation
    # note that the transformation does not depend on the base of logarithm
    out = np.sign(x) * np.log(1 + output_levels // 2 * np.abs(x)) / np.log(1 + output_levels // 2)
    out = ((out + 1) * (output_levels // 2)).astype(f"uint{output_bit_depth}")
    return out

threshold = 0.1

for folder in [train_folder, test_folder]:
    split = folder.split("_")[1][:-3]
    data_list = []
    speaker_list = []
    offset_list = [0]
    speaker = None
    for filename in sorted(os.listdir(folder)):
        if filename.endswith("wav"):
            sr, data = wavfile.read(os.path.join(folder, filename))
        try:
            data = data[slice(*np.where(data>=math.floor(threshold*(input_levels//2)))[0][[0,-1]])]
        except IndexError:
            continue
        data_list.append(data)
        offset_list.append(offset_list[-1]+len(data))
        if speaker is None:
            speaker_id = 0
            speaker = filename.split("_")[0]
        else:
            if filename.split("_")[0] > speaker:
                speaker_id += 1
        speaker_list.append(speaker_id)
    encoded = mu_law_encode(np.concatenate(data_list))
    filebytes = len(encoded) * (output_bit_depth//8)
    save_dir = os.path.join("processed",split)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    volume_no = 0
    max_volume_size = 99800000
    for i in range(0, filebytes, max_volume_size):
        np.save(
            os.path.join(save_dir,f"tiny-vctk-{split}-audio{volume_no}"),
            encoded[i:(i+max_volume_size)]
        )
        volume_no += 1
    np.save(os.path.join(save_dir,f"tiny-vctk-{split}-speaker"), np.array(speaker_list))
    np.save(os.path.join(save_dir,f"tiny-vctk-{split}-index"), np.array(offset_list))