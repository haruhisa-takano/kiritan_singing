# coding: utf-8
import jaconv
import numpy as np
from nnmnkwii.io import hts

def merge_sil(lab):
    N = len(lab)
    f = hts.HTSLabelFile()
    f.append(lab[0], strict=False)
    is_full_context = "@" in lab[0][-1]
    for i in range(1, N):
        if (is_full_context and "-sil" in f[-1][-1] and "-sil" in lab[i][-1]) \
            or (not is_full_context and f[-1][-1] == "sil" and lab[i][-1] == "sil"):
            # extend sil
            f.end_times[-1] = lab[i][1]
        else:
            f.append(lab[i], strict=False)
    return f


def segment_labels(lab, strict=True):
    segments = []
    seg = hts.HTSLabelFile()
    is_full_context = "@" in lab[0][-1]
    start_indices = []
    end_indices = []
    si = 0
    for idx, (s, e, l) in enumerate(lab):
        d = (e-s) * 1e-7
        if is_full_context:
            is_silence = ("-sil" in l or "-pau" in l)
        else:
            is_silence = (l == "sil" or l == "pau")
        if is_silence and d > 2.5:
            if len(seg) > 0:
                start_indices.append(si)
                si = 0
                end_indices.append(idx - 1)
                segments.append(seg)
                seg = hts.HTSLabelFile()
            continue
        else:
            if len(seg) == 0:
                si = idx
            seg.append((s, e, l), strict)
    if len(seg) > 0:
        segments.append(seg)

    return segments, start_indices, end_indices


def prep_ph2num():
    kiritan_phone_mapping = {}
    with open("./dic/japanese.table") as f:
        for l in f:
            s = l.strip().split()
            key = jaconv.hira2kata(s[0])
            kiritan_phone_mapping[key] = s[1:]
    sinsy_phone_mapping = {}
    with open("./dic/japanese.utf_8.table") as f:
        for l in f:
            s = l.strip().split()
            key = jaconv.hira2kata(s[0])
            sinsy_phone_mapping[key] = s[1:]
    ph2num = {}
    counter = 0
    for p in ["sil", "pau", "br"]:
        ph2num[p] = counter
        counter += 1
    for k, v in sinsy_phone_mapping.items():
        for p in v:
            if p not in ph2num:
                ph2num[p] = counter
                counter += 1
    for k, v in kiritan_phone_mapping.items():
        for p in v:
            if p not in ph2num:
                ph2num[p] = counter
                counter += 1
    # undef
    ph2num["xx"] = counter

    return ph2num


def ph2numeric(contexts, ph2num):
    return [ph2num[k] for k in contexts]


def fix_offset(lab):
    offset = lab.start_times[0]
    lab.start_times = np.asarray(lab.start_times) - offset
    lab.end_times = np.asarray(lab.end_times) - offset
    return lab


def trim_sil_and_pau(lab):
    is_full = "@" in lab.contexts[0]
    forward = 0
    while "-sil" in lab.contexts[forward] or "-pau" in lab.contexts[forward]:
        forward += 1
    backward = len(lab)-1
    while "-sil" in lab.contexts[backward] or "-pau" in lab.contexts[backward]:
        backward -= 1

    return lab[forward:backward]


def get_note_indices(lab):
    note_indices = [0]
    last_start_time = lab.start_times[0]
    for idx in range(1, len(lab)):
        if lab.start_times[idx] != last_start_time:
            note_indices.append(idx)
            last_start_time = lab.start_times[idx]
        else:
            pass
    return note_indices