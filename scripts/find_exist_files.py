import unibox
import os
import shutil

if __name__ == '__main__':
    f1_str = r"E:\sekai\kanade_audio_copy"
    f2_str = r"E:\sekai\kanade_audio_flac_16bit_48k_poly-sinc-ext3_rerun"

    f1 = unibox.traverses(f1_str, include_extensions=[".mp3"])
    f2 = unibox.traverses(f2_str, include_extensions=[".flac"])


    basenames_f1 = [os.path.basename(i) for i in f1]
    basenames_f2 = [os.path.basename(i) for i in f2]

    not_in_f2 = []
    for i in basenames_f1:
        if i.replace(".mp3", ".flac") not in basenames_f2:
            not_in_f2.append(i)

    #copy not_in_f2 to f2
    for i in not_in_f2:
        shutil.copy(os.path.join(f1_str, i), f2_str)

    print("D")