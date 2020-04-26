# Common settings

from os.path import join, expanduser

# Output directory
# All the igenerated labels, intermediate files, and segmented wav files
# will be saved in the following directory
# Note that manually corrected files are managed by the following repository:
# https://github.com/r9y9/kiritan_singing_extra
out_dir = "kiritan_singing_extra"

# PLEASE CHANGE THE PATH BASED ON YOUR ENVIRONMENT
wav_dir = join(expanduser("~"), "data/kiritan_singing/wav/")

# Split song by silences (in sec)
segmentation_threshold = 2.5

# TODO(ryuichi): progress 31/50
num_annotated_files = 31