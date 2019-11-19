import os
import random
IMAGE_PATH = "/data/DigitalBody/pos_images/JPEGImages/"
IMAGESET_PATH = "/data/DigitalBody/pos_images/ImageSets/Main/"
files = os.listdir(IMAGE_PATH)

trainval = open(IMAGESET_PATH+"trainval.txt", "w")
test = open(IMAGESET_PATH + "test.txt", "w")
for file in files:
    filename = file.split(".")[0]
    train_or_test = (random.uniform(0,1) >= 0.2)
    if train_or_test:
        trainval.write(filename+"\n")
    else:
        test.write(filename+"\n")
trainval.close()
test.close()


