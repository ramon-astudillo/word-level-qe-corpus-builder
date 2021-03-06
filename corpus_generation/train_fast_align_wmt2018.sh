#!/bin/bash
#
# This generates the alignment data for WMT2017 as an example. 
#
# Flags
set -o errexit
set -o nounset
set -o pipefail

# Check it is run from the right folder
if [ ! -d "tools/" ];then
    echo "$0 should be run from inside ./corpus_generation folder"    
    exit        
fi

OUT_FOLDER="../DATA/WMT2018"

# de-en.smt  
language_pair="de-en.smt"
echo ${language_pair}
# Train forward and backward models for fast align
echo "Training fast_align ${language_pair}"
bash ./tools/train_fast_align.sh \
    ${OUT_FOLDER}/aligner_training_data/de-en/train.tok.de.tc \
    ${OUT_FOLDER}/aligner_training_data/de-en/train.tok.en.tc \
    ${OUT_FOLDER}/temporal_files/fast_align_train/${language_pair}/ \
    ${OUT_FOLDER}/fast_align_models/${language_pair}/

# en-cs.smt    
language_pair="en-cs.smt"
echo ${language_pair}
# Train forward and backward models for fast align
echo "Training fast_align ${language_pair}"
bash ./tools/train_fast_align.sh \
    ${OUT_FOLDER}/aligner_training_data/en-cs/train.en \
    ${OUT_FOLDER}/aligner_training_data/en-cs/train.cs \
    ${OUT_FOLDER}/temporal_files/fast_align_train/${language_pair}/ \
    ${OUT_FOLDER}/fast_align_models/${language_pair}/

# en-de.nmt
language_pair="en-de.nmt"
echo ${language_pair}
# Train forward and backward models for fast align
echo "Training fast_align ${language_pair}"
bash ./tools/train_fast_align.sh \
    ${OUT_FOLDER}/aligner_training_data/en-de/train.tok.en.tc \
    ${OUT_FOLDER}/aligner_training_data/en-de/train.tok.de.tc \
    ${OUT_FOLDER}/temporal_files/fast_align_train/${language_pair}/ \
    ${OUT_FOLDER}/fast_align_models/${language_pair}/
# en-de.smt
ln -s ${OUT_FOLDER}/fast_align_models/${language_pair}/ ${OUT_FOLDER}/fast_align_models/en-de.smt

# en-lv.nmt
# Note that these models were trained from data with a minor difference in
# preprocessing (numbers were normalized). Since this does not affect tokens,
# alignments are still valid
for language_pair in en-lv.smt en-lv.nmt;do
    echo ${language_pair}
    # Train forward and backward models for fast align
    echo "Training fast_align ${language_pair}"
    bash ./tools/train_fast_align.sh \
        ${OUT_FOLDER}/NUM_PREPRO/aligner_training_data/en-lv/train.en \
        ${OUT_FOLDER}/NUM_PREPRO/aligner_training_data/en-lv/train.lv \
        ${OUT_FOLDER}/NUM_PREPRO/temporal_files/fast_align_train/${language_pair}/ \
        ${OUT_FOLDER}/NUM_PREPRO/fast_align_models/${language_pair}/
done
