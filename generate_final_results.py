import os
import json

json_dir = "/data/DigitalBody/tests/result_json"
final_results_dir = "/data/DigitalBody/tests/final_results"

WIDTH, HEIGHT = 1000, 1000
THRESHOLD = 0.0

labels = {}
json_files = os.listdir(json_dir)
for json_file in json_files:
    s = json_file.split('.')[0].split('_')
    i, j = int(s[2]), int(s[3])
    index = s[0] + '_' + s[1]
    labels[index] = []

for json_file in json_files:
    s = json_file.split('.')[0].split('_')
    i, j = int(s[2]), int(s[3])
    index = s[0] + '_' + s[1]
    with open(json_dir + '/' + json_file, "r") as f:
        content = json.load(f)
        if len(content):
            for label in content:
                label["x"] += WIDTH * i
                label["y"] += HEIGHT * j
                if label["p"] > THRESHOLD:
                    labels[index].append(label)

for index in labels:
    print(index, labels[index])
    with open(final_results_dir + '/' + index + ".json", "w") as output:
        json.dump(labels[index], output)

