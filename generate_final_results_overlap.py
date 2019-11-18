#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from nms.gpu_nms import gpu_nms
from pycocotools.coco import COCO
import numpy as np


WIDTH, HEIGHT = 1000, 1000
STRIDE_X, STRIDE_Y = 750, 750 
NMS_THRESH, THRESHOLD = 0.5, 0.05


def json2dict(result_json, coco):
    bboxes_dict = dict()
    for detec in result_json:
        img_id = detec['image_id']
        img_name = coco.loadImgs(img_id)[0]['file_name']
        img_name_split = img_name.split('.')[0].split('_')
        kfb_name = '_'.join(img_name_split[0:2])
        if kfb_name not in bboxes_dict.keys():
            bboxes_dict[kfb_name] = []
        if detec['score'] > THRESHOLD:
            bbox = []
            i, j = int(img_name_split[2]), int(img_name_split[3])
            bbox.append(STRIDE_X * i + detec['bbox'][0])
            bbox.append(STRIDE_Y * j + detec['bbox'][1])
            bbox.append(bbox[0] + detec['bbox'][2])
            bbox.append(bbox[1] + detec['bbox'][3])
            bbox.append(detec['score'])
            bboxes_dict[kfb_name].append(bbox)
    return bboxes_dict


def nms_bboxes_dict(bboxes_dict):
    for kfb_name, bboxes in bboxes_dict.items():
        bboxes = np.array(bboxes).astype(np.float32)
        keep = gpu_nms(bboxes, NMS_THRESH)
        bboxes_dict[kfb_name] = []
        for bbox in bboxes[keep]:
            bbox_new = dict()
            bbox_new['x'] = int(bbox[0])
            bbox_new['y'] = int(bbox[1])
            bbox_new['w'] = max(int(bbox[2] - bbox[0]), 1)
            bbox_new['h'] = max(int(bbox[3] - bbox[1]), 1)
            bbox_new['p'] = float(bbox[4])
            bboxes_dict[kfb_name].append(bbox_new)
    return bboxes_dict 


if __name__ == "__main__":
    ann_file = "/data/DigitalBody/pos_images/VOC2012/coco_test_annotation.json"
    res_json_file = '/data/DigitalBody/pos_images/result_file.pkl.bbox.json'
    final_res_dir = "/data/DigitalBody/tests/final_results"
    # ann_file, res_json_file, final_res_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    coco = COCO(annFile)
    with open(result_json_file, 'r') as f:
        result_json = json.load(f)
    bboxes_dict = nms_bboxes_dict(json2dict(result_json, coco))
    for kfb_name in bboxes_dict:
        print(kfb_name, bboxes_dict[kfb_name])
        with open(final_res_dir + '/' + kfb_name + ".json", "w") as output:
            json.dump(bboxes_dict[kfb_name], output)


