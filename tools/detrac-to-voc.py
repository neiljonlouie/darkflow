# Usage: ./detrac-to-voc.py /path/to/detrac/annotations /output/dir
import os, sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

annot_dir = sys.argv[1]
output_dir = sys.argv[2]

if os.path.exists(output_dir):
    if not os.path.isdir(output_dir):
        print('"%s" is not a directory')
        sys.exit(-1)
else:
    os.mkdir(output_dir)

for file_name in os.listdir(annot_dir):
    annot_tree = ET.parse(os.path.join(annot_dir, file_name))
    annot_root = annot_tree.getroot()

    dir_name = annot_root.attrib['name']
    output_file_path = os.path.join(output_dir, dir_name)
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)

    for frame in annot_root.findall('frame'):
        frame_num = int(frame.attrib['num'])
        output_root = ET.Element('annotation')
        folder = ET.Element('folder')
        folder.text = dir_name
        output_root.append(folder)

        output_name = 'img%05d.xml' % frame_num
        output_str = minidom.parseString(ET.tostring(output_root))
        output_str = output_str.toprettyxml(indent='    ')
        with open(os.path.join(output_file_path, output_name), 'w') as file:
            file.write(output_str)
            file.close()

        break

    break