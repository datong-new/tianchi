import json
from tianchi import CONSTANT

def store_annotation(filename, label_json):
    with open(CONSTANT.POS_JSON_PATH + filename+".json", "w") as output:
        json.dump(label_json, output)


def create_annotations(filename, label_json):
    xml_object = ""
    for lbl in label_json:
        xml_object += CONSTANT.PASCAL_OBJECT.format(
            int(lbl["truncated"]) , lbl["new_x"], lbl["new_y"], lbl["new_x"]+lbl["new_w"], lbl["new_y"]+lbl["new_h"])
        xml_object += "\n"
    xml = CONSTANT.PASCAL_XML_HEADER.format(filename+".jpg") + \
           xml_object + CONSTANT.PASCAL_XML_FOOTER

    with open(CONSTANT.POS_ANNOTATION_PATH + filename + ".xml", "w") as f:
        f.write(xml)

