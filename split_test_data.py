import os
import json
import kfbReader
import cv2

WIDTH, HEIGHT, STRIDE = 1000, 1000, 750

test_data_dir = "/data/DigitalBody/pos_images/VOC2012/datasets_new"


def split_data(kfb_path):
    reader = kfbReader.reader()
    scale = 20
    reader.ReadInfo(kfb_path, scale, False)

    x_num = int(reader.getWidth() / STRIDE) + 1
    y_num = int(reader.getHeight() / STRIDE) + 1

    for i in range(x_num):
        for j in range(y_num):
            square = reader.ReadRoi(STRIDE * i, STRIDE * j, WIDTH, HEIGHT, 20)
            file_name = test_data_dir + '/' + kfb_path.split('/')[-1].split('.')[0] \
                        + '_' + str(i) + '_' + str(j) + ".jpg"
            # print(file_name)
            cv2.imwrite(file_name, square)


for i in range(4):
    kfb_dir = "/data/DigitalBody/test_" + str(i)
    kfb_files = os.listdir(kfb_dir)
    for kfb_file in kfb_files:
        kfb_path = kfb_dir + '/' + kfb_file
        # print(kfb_path)

        print(kfb_path, "is processing...")

        split_data(kfb_path)

