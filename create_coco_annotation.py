import json
from tianchi import CONSTANT
import pycocotools.mask as mask
import os
import time

def create_image_info(filename, image_id, data_captured="2019-11-17 00:00:00",
                      flickr_url="http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
                      coco_url = "coco_url.jpg",
                      height = 1000, width=1000, licenses=1
                      ):
    image = {"license": licenses, "file_name": filename, "coco_url": coco_url, "height": height, "width": width,
             "data_captured": data_captured, "flickr_url": flickr_url, "id": image_id}

    return image

def create_segmentation_from_bbox(bbox):
    left_top_x, left_top_y, width, height = bbox[0], bbox[1], bbox[2], bbox[3]
    return [[left_top_x, left_top_y,
            left_top_x, left_top_y+height,
            left_top_x+width, left_top_y+height,
            left_top_x+width, left_top_y]]

"""
bbox = [left_top_x, left_top_y, width, height]
"""
def create_annotation(bbox, image_id, ann_id, segmentation=None, iscrowd=0, category_id=1, area=None):
    if area is None:
        area = bbox[2] * bbox[3]
    annotation = {"bbox": bbox, "image_id": image_id, "id": ann_id, "iscrowd": iscrowd, "category_id": category_id,
                  "area": area}
    if segmentation is None:
        segmentation = create_segmentation_from_bbox(bbox)
    annotation["segmentation"] = segmentation
    return annotation

def create_coco_dataset(json_name, image_id, ann_id):
    images = []
    annotations = []

    file_name = json_name.split(".")[0] + ".jpg"

    image = create_image_info(file_name, image_id)
    images.append(image)

    with open(CONSTANT.POS_JSON_PATH + json_name) as f:
        contents = json.load(f)
    for content in contents:
        bbox = [content["new_x"], content["new_y"], content["new_w"], content["new_h"]]
        annotation = create_annotation(bbox, image_id, ann_id)
        ann_id += 1
        annotations.append(annotation)
    return images, annotations, ann_id

start_time =  time.localtime(time.time())
TEST_IMAGE_PATH = "/root/DigitalBody/pos_images/VOC2012/datasets"
files = os.listdir(TEST_IMAGE_PATH)
image_id = 1
images, annotations = [], []
for filename in files:
    print(image_id, "st image")
    images.append(create_image_info(filename, image_id))
    image_id += 1

TEST_COCO_PATH = "/root/DigitalBody/pos_images/VOC2012/test_coco.json"
TEST_COCO = CONSTANT.COCODATASET
TEST_COCO["images"] = images
TEST_COCO["annotations"] = annotations
with open(TEST_COCO_PATH, "w") as f:
    json.dump(TEST_COCO, f)



"""
JSON_PATH = CONSTANT.POS_JSON_PATH
files = os.listdir(JSON_PATH)
final_images, final_anns = [], []
image_id, ann_id = 1, 1

for file in files:
    print(image_id, "st image")
    images, annos, ann_id = create_coco_dataset(file, image_id, ann_id)
    image_id += 1
    final_images += images
    final_anns += annos

print("start time:", start_time)
print("end time:", time.localtime(time.time()))
COCODATASET = CONSTANT.COCODATASET
COCODATASET["images"] = final_images
COCODATASET["annotations"] = final_anns
with open(CONSTANT.COCODATASET_PATH, "w") as f:
    json.dump(COCODATASET, f)
"""








