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

# Song segmentation by silence durations.
# TODO: would be better to split songs by phrasal information in the musical scores

# Split song by silences (in sec)
segmentation_threshold = 0.4

# Min duration for a segment
# note: there could be some execptions (e.g., the last segment of a song)
segment_min_duration = 5.0

# Force split segments if long silence is found regardless of min_duration
force_split_threshold = 5.0


# Offset correction
# If True, offset is computed in an entire song
# otherwise offset is computed for each segment
global_offset_correction = False

max_timelag = 50

# TODO(ryuichi): progress 37/50
num_annotated_files = 37