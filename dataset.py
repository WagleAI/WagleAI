import os
import cv2
import random
import shutil
import utils.utils
from testcase import *
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse


class XML:
    root = None
    tree = None

    def __init__(self, image=None, image_path=None, image_list=None,
                 frame_num=None, label_list=None, filtered_list=None,
                 filtered_class=None, MOT=False):

        self.image = image
        self.image_path = image_path
        self.image_list = image_list
        self.frame_num = frame_num
        self.label_list = label_list
        self.filtered_list = filtered_list
        self.filtered_class = filtered_class
        self.MOT = MOT

        self.initialize_root()

    def initialize_root(self):
        self.root = Element('annotation')
        self.tree = None

    def set_filtered_info(self, filtered_list, filtered_class):
        self.filtered_list = filtered_list
        self.filtered_class = filtered_class

    def make_xml_head(self):
        SubElement(self.root, 'folder').text = self.image_path

        if self.MOT:
            SubElement(self.root, 'filename').text = \
                self.image_list[self.frame_num]
            SubElement(self.root, 'path').text = \
                self.image_path + "/" + self.image_list[self.frame_num]
        else:
            SubElement(self.root, 'filename').text = \
                self.image_list
            SubElement(self.root, 'path').text = \
                self.image_path + '/' + self.image_list

        source = SubElement(self.root, 'source')
        SubElement(source, 'database').text = 'Unknown'

        size = SubElement(self.root, 'size')

        if self.MOT:
            SubElement(size, 'width').text = str(self.image.shape[1])
            SubElement(size, 'height').text = str(self.image.shape[0])
            SubElement(size, 'depth').text = '3'
        else:
            SubElement(size, 'width').text = str(self.label_list[0][0])
            SubElement(size, 'height').text = str(self.label_list[0][1])
            SubElement(size, 'depth').text = '3'

        SubElement(self.root, 'segmented').text = '0'

        if self.MOT:
            for filtered_class in range(len(self.filtered_list)):
                if self.filtered_list[filtered_class][7] == '1' or \
                        self.filtered_list[filtered_class][7] == '2':
                    self.set_filtered_info(self.filtered_list, filtered_class)
                    obj = SubElement(self.root, 'object')
                    SubElement(obj, 'name').text = 'person'
                    SubElement(obj, 'pose').text = 'Unspecified'
                    SubElement(obj, 'truncated').text = '0'
                    SubElement(obj, 'difficult').text = '0'

                    bbox = SubElement(obj, 'bndbox')
                    SubElement(bbox, 'xmin').text = \
                        self.filtered_list[self.filtered_class][2]
                    SubElement(bbox, 'ymin').text = \
                        self.filtered_list[self.filtered_class][3]
                    SubElement(bbox, 'xmax').text = \
                        str(int(self.filtered_list[self.filtered_class][2]) +
                            int(self.filtered_list[self.filtered_class][4]))
                    SubElement(bbox, 'ymax').text = \
                        str(int(self.filtered_list[self.filtered_class][3]) +
                            int(self.filtered_list[self.filtered_class][5]))

            self.tree = ElementTree(self.root)
            return self.tree

        else:
            for i in range(len(self.label_list)):
                obj = SubElement(self.root, 'object')
                SubElement(obj, 'name').text = self.label_list[i][2]
                SubElement(obj, 'pose').text = 'Unspecified'
                SubElement(obj, 'truncated').text = '0'
                SubElement(obj, 'difficult').text = '0'

                box = SubElement(obj, 'bndbox')
                SubElement(box, 'xmin').text = self.label_list[i][3]
                SubElement(box, 'ymin').text = self.label_list[i][4]
                SubElement(box, 'xmax').text = self.label_list[i][5]
                SubElement(box, 'ymax').text = self.label_list[i][6]

            self.tree = ElementTree(self.root)
            return self.tree


def get_human_image_name(xml_root):
    image_list = []
    for images in xml_root.iter("image"):
        label_list = []
        for boxes in images.iter("box"):
            label_list.append(boxes.attrib["label"])

        if "person" in label_list:
            image_list.append(images.attrib["name"])

    return image_list


def remove_images(data_path):
    folder_list = os.listdir(data_path)
    folder_list.sort()
    print(folder_list)

    for ped_fol in folder_list:
        bbox_data_path = data_path + "/" + ped_fol
        xml_file_folder_list = os.listdir(bbox_data_path)
        xml_file_folder_list.sort()

        for xml_fol in xml_file_folder_list:
            xml_file_path = bbox_data_path + "/" + xml_fol
            xml_file_list = \
                [file for file in os.listdir(xml_file_path) if
                 file.endswith(r".xml")]

            xml_tree = parse(xml_file_path + "/" + xml_file_list[0])
            xml_root = xml_tree.getroot()

            human_image_list = get_human_image_name(xml_root)
            image_list = [file for file in os.listdir(xml_file_path) if
                          file.endswith(r".jpg") or file.endswith(r".png")]

            for file in image_list:
                if file not in human_image_list:
                    os.remove(xml_file_path + "/" + file)


def make_xml_label(images, image_file_list):
    label_list = []
    if images.attrib["name"] in image_file_list:
        width = images.attrib["width"]
        height = images.attrib["height"]

        for boxes in images.iter("box"):
            if boxes.attrib["label"] == "person":
                label_list.append([width, height, boxes.attrib["label"],
                                   boxes.attrib["xtl"], boxes.attrib["ytl"],
                                   boxes.attrib["xbr"], boxes.attrib["ybr"]])

    else:
        pass

    return label_list


def parse_images(data_path):
    folder_list = os.listdir(data_path)
    folder_list.sort()

    for ped_fol in folder_list:
        bbox_data_path = data_path + "/" + ped_fol
        xml_file_folder_list = os.listdir(bbox_data_path)
        xml_file_folder_list.sort()

        for xml_fol in xml_file_folder_list:
            xml_file_path = bbox_data_path + "/" + xml_fol
            xml_file_list = [file for file in os.listdir(xml_file_path) if
                             file.endswith(r".xml")]
            image_file_list = [file for file in os.listdir(xml_file_path) if
                                file.endswith(r".jpg") or file.endswith(r".png")]

            xml_tree = parse(xml_file_path + "/" + xml_file_list[0])
            xml_root = xml_tree.getroot()

            for images in xml_root.iter("image"):
                human_label_list = make_xml_label(images, image_file_list)
                if human_label_list:
                    xml = XML(images, xml_file_path, images.attrib["name"],
                              label_list=human_label_list, MOT = False)
                    tree = xml.make_xml_head()
                    tree.write(xml_file_path + "/" +
                               images.attrib["name"][:-4] + '.xml')
                else :
                    continue


def parse_mot(data_path):
    folder_list = os.listdir(data_path)
    folder_list.sort()

    for mot_fol in folder_list:
        train_folder_path = data_path + "/" + mot_fol + "/train"
        train_video_list = os.listdir(train_folder_path)
        train_video_list.sort()

        for video_fol in train_video_list:
            gt_path = train_folder_path + "/" + video_fol + "/gt"
            image_path = train_folder_path + "/" + video_fol + "/img1"

            gt_list = []
            image_list = \
                [file for file in os.listdir(image_path) if
                 file.endswith(r".jpg")]
            image_list.sort()

            with open(gt_path + "/gt.txt", "r") as gt:
                gt_file = gt.readlines()

            for line_num in range(len(gt_file)):
                line = gt_file[line_num][:-1].split(",")
                gt_list.append(line)

            gt_list = sorted(gt_list, key = lambda x : x[0])

            for frame_num in range(len(image_list)):
                filtered_list = [x for x in gt_list if x[0] == str(frame_num+1)]
                image = cv2.imread(image_path + "/" + image_list[frame_num],
                                   cv2.IMREAD_COLOR)

                xml = XML(image, image_path, image_list, frame_num, filtered_list=filtered_list, MOT=True)
                tree = xml.make_xml_head()
                tree.write(image_path + "/" + image_list[frame_num][:-3] + 'xml')


def make_folders(train_path, valid_path = None):
    utils.utils.makedirs(train_path)
    if valid_path:
        utils.utils.makedirs(valid_path)

    image_path = "/images"
    annot_path = "/annots"

    utils.utils.makedirs(train_path + image_path)
    utils.utils.makedirs(train_path + annot_path)
    if valid_path:
        utils.utils.makedirs(valid_path + image_path)
        utils.utils.makedirs(valid_path + annot_path)


def find_all_filelist(data_path, check):
    data_folder_list = os.listdir(data_path)
    data_folder_list.sort()

    all_file_list = []

    for data_fol in data_folder_list:
        bbox_data_path = data_path + "/" + data_fol

        if check == 'True':
            bbox_data_path = bbox_data_path

        xml_file_folder_list = os.listdir(bbox_data_path)
        xml_file_folder_list.sort()

        if check == 'True':
            #print(bbox_data_path)
            xml_folder_list = os.listdir(bbox_data_path + '/' + xml_file_folder_list[1])

            for image_fol in xml_folder_list:
                image_file_path = bbox_data_path + '/train/' + image_fol + '/img1'

                file_list = [image_file_path + "/" + name[:-4] for name in
                             os.listdir(image_file_path) if
                             name.endswith(r".jpg")]

                all_file_list.extend(file_list)

        else:
            xml_folder_list = xml_file_folder_list

            for image_fol in xml_folder_list:
                image_path = bbox_data_path + "/" + image_fol
                image_file_folder_list = os.listdir(image_path)
                image_file_folder_list.sort()
                image_file_path = bbox_data_path + "/" + image_fol

                file_list = [image_file_path + "/" + name[:-4] for name
                             in os.listdir(image_path)
                             if (name.endswith(r".jpg")
                                 or name.endswith(r".png"))]
                all_file_list.extend(file_list)

    return all_file_list


def split_folders(data_path, check, train_path, valid_path=None):

    make_folders(train_path, valid_path)
    filelist = find_all_filelist(data_path, check)
    #print(filelist[:10])

    random.seed(100)
    random.shuffle(filelist)
    if valid_path:
        pivot = int(len(filelist) * 0.7)
        train_list = filelist[:pivot]
        test_list = filelist[pivot:]

        return train_list, test_list

    else:
        return filelist, None


def move_files(filelist, path):
    for file in filelist:
        xml_file_name = file + ".xml"
        img_file_name = file + ".jpg"
        png_file_name = file + ".png"

        if os.path.isfile(xml_file_name) and (os.path.isfile(img_file_name)
                                              or os.path.isfile(png_file_name)):
            name = file.split("/")

            shutil.move(xml_file_name,
                        path+"/annots/" + ''.join(name[-1:]) + ".xml")
            if os.path.isfile(img_file_name):
                shutil.move(img_file_name,
                            path + "/images/" + ''.join(name[-1:]) + ".jpg")
            else:
                shutil.move(xml_file_name,
                            path + "/images/" + ''.join(name[-1:]) + ".png")


def dataset_main_(args):
    data_path = args.path
    mot_check = args.mot
    train_path = args.train
    test_path = args.valid

    yolo_config_file_exit('pass') \
        if os.path.isdir(data_path) \
        else yolo_config_file_exit('fail')

    if mot_check == 'False':
        remove_images(data_path)
        parse_images(data_path)
    else :
        parse_mot(data_path)

    if train_path or test_path:
        train, test = split_folders(data_path, mot_check, train_path, test_path)

        move_files(train, train_path)
        if test_path:
            move_files(test, test_path)


"""if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Make a xml format file for train/valid')

    argparser.add_argument('-d', '--directory',
                           help='path to a directory of images')
    argparser.add_argument('-m', '--MOT',
                           help='path to a mot format gt file')
    argparser.add_argument('-t', '--train',
                           help='path to a train directory')
    argparser.add_argument('-v', '--valid',
                           help='path to a valid directory')

    args = argparser.parse_args()
    _main_(args)
"""