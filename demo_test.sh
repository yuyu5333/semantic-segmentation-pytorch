#!/bin/bash

# Image and model names
TEST_IMG=/data/user8302433/home/work_fish/proper_work/image/10.jpg
MODEL_NAME=ade20k-resnet50dilated-ppm_deepsup
MODEL_PATH=ckpt/$MODEL_NAME
RESULT_PATH=./image/

ENCODER=$MODEL_NAME/encoder_epoch_2.pth
DECODER=$MODEL_NAME/decoder_epoch_2.pth

# Download model weights and image
# if [ ! -e $MODEL_PATH ]; then
#   mkdir -p $MODEL_PATH
# fi
# if [ ! -e $ENCODER ]; then
#   wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$ENCODER
# fi
# if [ ! -e $DECODER ]; then
#   wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$DECODER
# fi
# if [ ! -e $TEST_IMG ]; then
#   wget -P $RESULT_PATH http://sceneparsing.csail.mit.edu/data/ADEChallengeData2016/images/validation/$TEST_IMG
# fi

# if [ -z "$DOWNLOAD_ONLY" ]
# then

# Inference
python3 -u test.py \
  --imgs $TEST_IMG \
  --cfg config/self_config.yaml \
  DIR $MODEL_PATH \
  TEST.result ./ \
  TEST.checkpoint epoch_2.pth \
  # --gpu 2
# fi

# python3 -u test.py --imgs ./image/ --cfg config/self_config.yaml DIR ckpt/ade20k-resnet50dilated-ppm_deepsup/ TEST.result ./image/result TEST.checkpoint epoch_4.pth


