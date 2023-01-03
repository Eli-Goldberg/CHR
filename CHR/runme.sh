#!/bin/bash
# select gpu devices
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:128

python -m CHR.main --batch-size 8 |& tee -a log
