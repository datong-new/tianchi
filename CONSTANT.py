POS_ANNOTATION_PATH = "/data/DigitalBody/pos_images/Annotations/"
POS_IMAGE_PATH = "/data/DigitalBody/pos_images/JPEGImages/"
POS_JSON_PATH = "/data/DigitalBody/pos_images/JSON/"


PASCAL_XML_HEADER = """
<annotation>
	<folder>VOC2007</folder>
	<filename>{0}</filename>
	<source>
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
		<flickrid>341012865</flickrid>
	</source>
	<owner>
		<flickrid>Fried Camels</flickrid>
		<name>Jinky the Fruit Bat</name>
	</owner>
	<size>
		<width>1000</width>
		<height>1000</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
"""

PASCAL_XML_FOOTER = """
</annotation>
"""

PASCAL_OBJECT = """
    <object>
        <name>abnormal_cell</name>
        <truncated>{0}</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{1}</xmin>
            <ymin>{2}</ymin>
            <xmax>{3}</xmax>
            <ymax>{4}</ymax>
        </bndbox>
    </object>
"""

COCO_INFO = {
    "info": {
        "description": "COCO 2017 Dataset",
        "url": "http://cocodataset.org",
        "version": "1.0",
        "year": 2017,
        "contributor": "COCO Consortium",
        "date_created": "2017/09/01"
    }
}

print(COCO_INFO)