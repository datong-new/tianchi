import os
import json
import time
from mmdet.apis import init_detector, inference_detector, show_result

config_file = "/mmdetection/configs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712.py"
checkpoint_file = "/data/DigitalBody/work_dir/latest.pth"

model = init_detector(config_file, checkpoint_file)

dataset_dir = "/data/DigitalBody/tests/datasets"
result_dir = "/data/DigitalBody/tests/result_jpg"
json_dir = "/data/DigitalBody/tests/result_json"

imgs = os.listdir(dataset_dir)

count = 0
t0 = time.time()
for img in imgs:
    image = dataset_dir + '/' + img
    result = inference_detector(model, image)
    show_result(image, result, model.CLASSES, out_file=result_dir + '/' + img)

    labels = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            label = result[i][j]
            temp = {"x": int(label[0]), "y": int(label[1]), \
                    "w": int(label[2] - label[0]), "h": int(label[3] - label[1]), \
                    "p": float("%.5f" % label[4])}
            labels.append(temp)
    with open(json_dir + '/' + img.split('.')[0] + ".json", "w") as output:
        json.dump(labels, output)
    t1 = time.time()
    count += 1
    if count % 100 == 0:
        print("used time: " + str(round(t1 - t0, 2)) + " s, " + str(count) + " finished, " + str(377328 - count) + " remained, " \
            + "estimate time: " + str(round((377328 - count)/(count/(t1 - t0)), 2))+ " s.")

# show_result(img, result, model.CLASSES, out_file="result.jpg")
# imgs = ['test1.jpg', 'test2.jpg']
# for i, result in enumerate(inference_detector(model, imgs, device='cuda:0')):
#    show_result(imgs[i], result, model.CLASSES, out_file='result_{}.jpg'.format(i))

