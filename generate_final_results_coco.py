from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import json
import cv2 as cv

annFile = "/data/DigitalBody/pos_images/VOC2012/coco_test_annotation.json"
resFile = "/data/DigitalBody/pos_images/result_file.pkl.bbox.json"
img_dir = "/data/DigitalBody/pos_images/VOC2012/JPEGImages"

STRIDE = 1000
THRESHOLD = 0.05

coco = COCO(annFile)
labels = {}

with open(resFile, 'r') as f:
    items = json.load(f)
    for item in items:
        img_id = item["image_id"]
        img_name = coco.loadImgs(img_id)[0]["file_name"]
        s = img_name.split('.')[0].split('_')
        index = s[0] + '_' + s[1]
        labels[index] = []

    for item in items:
        # print(item)
        label = {}
        img_id = item["image_id"]
        bbox = item["bbox"]
        score = item["score"]
        if score > THRESHOLD:
            img_name = coco.loadImgs(img_id)[0]["file_name"]
            img = cv.imread("final_results/jpeg" + '/' + img_name, 1)
            if img is None: 
                img = cv.imread(img_dir + '/' + img_name, 1)
            s = img_name.split('.')[0].split('_')
            index = s[0] + '_' + s[1]
            i, j = int(s[2]), int(s[3])
            label['x'] = STRIDE * i + int(bbox[0])
            label['y'] = STRIDE * j + int(bbox[1])
            label['w'] = int(bbox[2])
            label['h'] = int(bbox[3])
            label['p'] = float(round(score, 5))
            labels[index].append(label)
            cv.rectangle(img, (int(bbox[0]), int(bbox[1]),\
                               int(bbox[2]), int(bbox[3])), (255, 0, 0, 0), 2)
            cv.imwrite("final_results/jpeg" + '/' + img_name, img)

for index in labels:
    with open("final_results/json" + '/' + index + ".json", 'w') as output:
        json.dump(labels[index], output)

