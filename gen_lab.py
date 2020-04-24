import pysinsy
import os

from glob import glob
from os.path import join, basename, splitext
from nnmnkwii.io import hts
import config
from util import merge_sil

sinsy = pysinsy.sinsy.Sinsy()
assert sinsy.setLanguages("j", "/usr/local/lib/sinsy/dic")


# generate full/mono labels by sinsy
files = sorted(glob("musicxml/*.xml"))
for path in files:
    assert sinsy.loadScoreFromMusicXML(path)
    print(path)
    for is_mono in [True, False]:
        n = "sinsy_mono" if is_mono else "sinsy_full"
        labels = sinsy.createLabelData(is_mono, 1, 1).getData()
        lab = hts.HTSLabelFile()
        for l in labels:
            lab.append(l.split(), strict=False)
        lab = merge_sil(lab)
        dst_dir = join(config.out_dir, f"{n}")
        os.makedirs(dst_dir, exist_ok=True)
        name = splitext(basename(path))[0]
        with open(join(dst_dir, name + ".lab"), "w") as f:
            f.write(str(lab))
    sinsy.clearScore()

# Prepare mono label with 100ns unit.
files = sorted(glob("mono_label/*.lab"))
dst_dir = join(config.out_dir, "kiritan_mono")
os.makedirs(dst_dir, exist_ok=True)
for m in files:
    h = hts.HTSLabelFile()
    with open(m) as f:
        for l in f:
            s,e,l = l.strip().split()
            s,e = int(float(s) * 1e7), int(float(e) * 1e7)
            h.append((s,e,l))
        with open(join(dst_dir, basename(m)), "w") as of:
            of.write(str(h))

# Rounding
for name in ["sinsy_mono", "sinsy_full", "kiritan_mono"]:
    files = sorted(glob(join(config.out_dir, name, "*.lab")))
    dst_dir = join(config.out_dir, name + "_round")
    os.makedirs(dst_dir, exist_ok=True)

    for path in files:
        lab = hts.load(path)
        name = basename(path)

        for x in range(len(lab)):
            lab.start_times[x] = round(lab.start_times[x] / 50000) * 50000
            lab.end_times[x] = round(lab.end_times[x] / 50000) * 50000

        # Check if rounding is done property
        if name == "kiritan_mono":
            for i in range(len(lab)-1):
                if lab.end_times[i] != lab.start_times[i+1]:
                    print(path)
                    print(i, lab[i])
                    print(i+1, lab[i+1])
                    import ipdb; ipdb.set_trace()

        with open(join(dst_dir, name), "w") as of:
            of.write(str(lab))