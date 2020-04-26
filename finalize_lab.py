import pysinsy
import os

from glob import glob
from os.path import join, basename, splitext, exists
from nnmnkwii.io import hts
from scipy.io import wavfile
import librosa
import soundfile as sf
import sys
from tqdm import tqdm
import numpy as np
import config
from util import fix_offset, trim_sil_and_pau, get_note_indices

full_align_dir = join(config.out_dir, "full_dtw_seg")
full_score_dir = join(config.out_dir, "sinsy_full_round_seg")


def sanity_check_lab(lab):
    for b,e,l in lab:
        assert e-b > 0


### Prepare data for time-lag models

dst_dir = join(config.out_dir, "timelag")
lab_align_dst_dir  = join(dst_dir, "label_phone_align")
lab_score_dst_dir  = join(dst_dir, "label_phone_score")

for d in [lab_align_dst_dir, lab_score_dst_dir]:
    os.makedirs(d, exist_ok=True)

print("Prepare data for time-lag models")
for n in tqdm(range(1, config.num_annotated_files+1)):
    seg_idx = 0

    while True:
        lab_align_path = join(full_align_dir, f"{n:02}_seg{seg_idx}.lab")
        lab_score_path = join(full_score_dir, f"{n:02}_seg{seg_idx}.lab")
        name = basename(lab_align_path)
        assert seg_idx > 0 or exists(lab_align_path)
        if not exists(lab_align_path):
            break
        assert exists(lab_score_path)

        lab_align = hts.load(lab_align_path)
        lab_score = hts.load(lab_score_path)
        sanity_check_lab(lab_align)

        # Pau/sil lenghts may differ in score and alignment, so remove it in case.
        lab_align = trim_sil_and_pau(lab_align)
        lab_score = trim_sil_and_pau(lab_score)

        # Extract note onsets and let's compute a offset
        note_indices = get_note_indices(lab_score)

        # offset = argmin_{b} \sum_{t=1}^{T}|x-(y+b)|^2
        # assuming there's a constant offset; tempo is same through the song
        onset_align = np.asarray(lab_align[note_indices].start_times)
        onset_score = np.asarray(lab_score[note_indices].start_times)
        offset = (onset_align - onset_score).mean()
        offset = int(round(offset / 50000) * 50000)
        print(f"{name} Offset (in sec): {offset * 1e-7}")

        if offset * 1e-7 > 1.0:
            print("Large offset is detected! Bug or wrong score?")

        # Offset adjustment
        lab_score.start_times = list(np.asarray(lab_score.start_times) + offset)
        lab_score.end_times = list(np.asarray(lab_score.end_times) + offset)

        # Note onsets as labels
        lab_align = lab_align[note_indices]
        lab_score = lab_score[note_indices]

        # Save lab files
        lab_align_dst_path = join(lab_align_dst_dir, name)
        with open(lab_align_dst_path, "w") as of:
            of.write(str(lab_align))

        lab_score_dst_path = join(lab_score_dst_dir, name)
        with open(lab_score_dst_path, "w") as of:
            of.write(str(lab_score))

        seg_idx += 1

### Prepare data for duration models

dst_dir = join(config.out_dir, "duration")
lab_align_dst_dir  = join(dst_dir, "label_phone_align")

for d in [lab_align_dst_dir, lab_score_dst_dir]:
    os.makedirs(d, exist_ok=True)

print("Prepare data for duration models")
for n in tqdm(range(1, config.num_annotated_files+1)):
    seg_idx = 0

    while True:
        lab_align_path = join(full_align_dir, f"{n:02}_seg{seg_idx}.lab")
        name = basename(lab_align_path)
        assert seg_idx > 0 or exists(lab_align_path)
        if not exists(lab_align_path):
            break

        lab_align = hts.load(lab_align_path)
        sanity_check_lab(lab_align)
        lab_align = fix_offset(lab_align)

        # Save lab file
        lab_align_dst_path = join(lab_align_dst_dir, name)
        with open(lab_align_dst_path, "w") as of:
            of.write(str(lab_align))

        seg_idx += 1

### Prepare data for acoustic models

dst_dir = join(config.out_dir, "acoustic")
wav_dst_dir  = join(dst_dir, "wav")
lab_align_dst_dir  = join(dst_dir, "label_phone_align")
lab_score_dst_dir  = join(dst_dir, "label_phone_score")

for d in [wav_dst_dir, lab_align_dst_dir, lab_score_dst_dir]:
    os.makedirs(d, exist_ok=True)

print("Prepare data for acoustic models")
for n in tqdm(range(1, config.num_annotated_files+1)):
    wav_path = join(config.wav_dir, f"{n:02}.wav")
    assert exists(wav_path)
    # sr, wave = wavfile.read(wav_path)
    wav, sr = librosa.load(wav_path, sr=48000)

    seg_idx = 0
    while True:
        lab_align_path = join(full_align_dir, f"{n:02}_seg{seg_idx}.lab")
        lab_score_path = join(full_score_dir, f"{n:02}_seg{seg_idx}.lab")
        name = basename(lab_align_path)
        assert seg_idx > 0 or exists(lab_align_path)
        if not exists(lab_align_path):
            break
        lab_align = hts.load(lab_align_path)
        lab_score = hts.load(lab_score_path)

        # Make a slice of audio and then save it
        b, e = int(lab_align[0][0] * 1e-7 * sr), int(lab_align[-1][1] * 1e-7 * sr)
        wav_silce = wav[b:e]
        wav_slice_path = join(wav_dst_dir, name.replace(".lab", ".wav"))
        # TODO: consider explicit subtype
        sf.write(wav_slice_path, wav_silce, sr)

        # Set the beginning time to be zero for convenience
        lab_align = fix_offset(lab_align)
        sanity_check_lab(lab_align)
        lab_score = fix_offset(lab_score)

        # Save label
        lab_align_dst_path = join(lab_align_dst_dir, name)
        with open(lab_align_dst_path, "w") as of:
            of.write(str(lab_align))

        lab_score_dst_path = join(lab_score_dst_dir, name)
        with open(lab_score_dst_path, "w") as of:
            of.write(str(lab_score))

        seg_idx += 1

sys.exit(0)