export TRAINING_DATA=input/train_folds.csv
export TEST_DATA=input/test.csv
export c=2
export ROOT_DIR=input/data
export N_EPOCHS=1
export LR=0.005
export MODEL=$1
export BS=16
python -m src.train
