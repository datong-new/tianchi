import os
import json
import kfbReader
import cv2
import random
from copy import deepcopy
from tianchi.create_annotations import store_annotation
from tianchi.create_annotations import create_annotations
from tianchi import CONSTANT


def is_left_top_in_image(label, image):
    return (image["x"] < label["x"] < image["x"] + image["w"]) and \
           (image["y"] < label["y"] < image["y"] + image["h"])

def is_right_top_in_image(label, image):
    return (image["x"]<label["x"]+label["w"]<image["x"]+image["w"]) and \
           (image["y"] < label["y"] < image["y"] + image["h"])

def is_left_down_in_image(label, image):
    return (image["x"] < label["x"] < image["x"] + image["w"]) and \
           (image["y"]<label["y"]+label["h"]<image["y"]+image["h"])

def is_right_down_in_image(label, image):
    return (image["x"] < label["x"] + label["w"] < image["x"] + image["w"]) and \
           (image["y"]<label["y"]+label["h"]<image["y"]+image["h"])

def create_pos_data(label_path, kfb_path):
    with open(label_path, "r") as f:
        labels = json.load(f)
    reader = kfbReader.reader()
    scale = 20
    reader.ReadInfo(kfb_path, scale, False)

    filename = kfb_path.split("/")[-1].split(".")[0]
    pos_labels = [label for label in labels if label["class"]=="pos"]
    WIDTH, HEIGHT, DELTA = 1000, 1000, 500


    for i, label in enumerate(pos_labels):
        count = 0
        while count<3:
            is_truncated_too_small = False
            w_delta = random.randrange(-DELTA, DELTA)
            h_delta = random.randrange(-DELTA, DELTA)
            roi_x, roi_y, roi_w, roi_h = label["x"], label["y"], label["w"], label["h"]

            if roi_x + w_delta < 0:
                image_x = 0
            elif roi_x + w_delta > reader.getWidth()-WIDTH:
                image_x = reader.getWidth()-WIDTH
            else:
                image_x = roi_x + w_delta

            if roi_y + h_delta < 0:
                image_y = 0
            elif roi_y + h_delta > reader.getHeight()-HEIGHT:
                image_y = reader.getHeight()-HEIGHT
            else:
                image_y = roi_y + h_delta
            image = {"x":image_x, "y":image_y, "w":WIDTH, "h":HEIGHT}

            roi = reader.ReadRoi(image["x"], image["y"], image["w"], image["h"], 20)
            lbl_json = []
            """
            1. Distinguish if [label.x, label.y, label.w, label.h] is in [image.x, image.y
            image.width, image.height]
            2. Distinguish if label is truncated.
            3. Record label's position, its origin size=(w, h) and its new_size=(new_w, new_h) in new image.
            4. Record image's position in origin kfb file.
            """
            pos_lbls = deepcopy(pos_labels)
            for lbl in pos_lbls:
                if is_left_top_in_image(lbl, image):
                    lbl["new_x"] = lbl["x"] - image["x"]
                    lbl["new_y"] = lbl["y"] - image["y"]
                    lbl["new_w"] = min(image["x"] + image["w"] - lbl["x"], lbl["w"])
                    lbl["new_h"] = min(image["y"] + image["h"] - lbl["y"], lbl["h"])
                    lbl["truncated"] = True if (lbl["new_w"] != lbl["w"] or lbl["new_h"] != lbl["h"]) else False
                elif is_right_top_in_image(lbl, image):
                    lbl["new_x"] = 0
                    lbl["new_y"] = lbl["y"] - image["y"]
                    lbl["new_w"] = lbl["w"] - (image["x"]-lbl["x"])
                    lbl["new_h"] = min(image["y"] + image["h"] - lbl["y"], lbl["h"])
                    lbl["truncated"] = True
                elif is_left_down_in_image(lbl, image):
                    lbl["new_x"] = lbl["x"] - image["x"]
                    lbl["new_y"] = 0
                    lbl["new_w"] = min(image["x"] + image["w"] - lbl["x"], lbl["w"])
                    lbl["new_h"] = lbl["h"] - (image["y"]-lbl["y"])
                    lbl["truncated"] = True
                elif is_right_down_in_image(lbl, image):
                    lbl["new_x"], lbl["new_y"] = 0, 0
                    lbl["new_w"] = lbl["w"] - (image["x"]-lbl["x"])
                    lbl["new_h"] = lbl["h"] - (image["y"] - lbl["y"])
                    lbl["truncated"] = True
                if "new_w" in lbl:
                    cv2.rectangle(roi, (lbl["new_x"],lbl["new_y"]),
                                  (lbl["new_x"]+lbl["new_w"],lbl["new_y"]+lbl["new_h"]), (255,0,0), 2)

                    """
                    If the clopped label loss too much information, then discard it.
                    That is, only conserve the label with enough information.
                    """
                    if not (lbl["new_w"]<lbl["w"]/2 or lbl["new_h"] < lbl["h"]/2):
                        lbl_json.append(lbl)
                    else:
                        is_truncated_too_small = True
                        break
            ## Record image and label
            if is_truncated_too_small:
                continue
            elif len(lbl_json)>0:
                anno_file = filename + "_" + str(i) + "_"+str(count)
                store_annotation(anno_file, lbl_json)
                create_annotations(anno_file, lbl_json)
                cv2.imwrite(CONSTANT.POS_IMAGE_PATH+anno_file+ ".jpg", roi)
                count+=1


label_path = "/data/DigitalBody/labels/T2019_198.json"
kfb_path = "/data/DigitalBody/pos_0/T2019_198.kfb"

#label_path = "/data/DigitalBody/labels/T2019_976.json"
#kfb_path = "/data/DigitalBody/pos_4/T2019_976.kfb"
print(kfb_path.split("/")[-1].split(".")[0])

create_pos_data(label_path, kfb_path)
