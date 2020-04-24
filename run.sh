# Step 1:
# Generate full-context lables from music xml using pysinsy
# pysinsy: https://github.com/r9y9/pysinsy
python gen_lab.py

# Step 2
# Align sinsy's labels and kiritan's alignment file by DTW
# The reason we need this is because there are lots of mismatch between
# sinsy output and kiritan's provided alignment.
# e.g., long-vowel, number of pau/sil
# One solution for this is to correct alignment manually, but it would be laborious to work.
# To mitigate the problem, I decided to follow the following strategy:
#  1. Take an rough alignment using DTW
#  2. Manually check if the alignment is correct, Otherwise correct it manually.
# which should save my time for manual annotations.

# NOTE: you wouldn't need to run the following command, unless you want to reproduce what I do,
# since I provide the corrected labels at https://github.com/r9y9/kiritan_singing_extra
# The extra repository is added as a submodule in this repository.
# python align_lab.py

# Step 3:
# Perform segmentation.
python perf_segmentation.py

# Step 4:
# Make labels for training
# 1. time-lag model
# 2. duration model
# 3. acoustic model
python finalize_lab.py