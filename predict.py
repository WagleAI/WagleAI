import os
import cv2
import json
import time
import numpy as np
import threading
from socket import *
from tqdm import tqdm
from testcase import *
from keras.models import load_model
from utils.bbox import draw_boxes, count_person
from utils.utils import get_yolo_boxes, makedirs
from utils.density import density_estimator, show_density


def predict_main_(args):
    config_path = args.conf
    input_path = args.input
    output_path = args.output

    HOST = args.host
    PORT = 8080


    socket_client = socket(AF_INET, SOCK_STREAM)
    socket_client.connect((HOST, PORT))

    yolo_config_file_exit('pass') \
        if os.path.exists(config_path) \
        else yolo_config_file_exit('fail')

    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    makedirs(output_path)
    yolo_create_exit('pass') \
        if os.path.isdir(output_path) \
        else yolo_create_exit('fail')

    ###############################
    #   Set some parameter
    ###############################

    net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    ###############################
    #   Load the model
    ###############################

    yolo_model_exit('pass') \
        if os.path.isfile(config['train']['saved_weights_name']) \
        else yolo_model_exit('fail')

    infer_model = load_model(config['train']['saved_weights_name'],
                             compile=False)

    ###############################
    #   Predict bounding boxes 
    ###############################
    if 'webcam' in input_path:  # do detection on the first webcam
        tuples = (config['train']['saved_weights_name'], (net_h, net_w),
                  config['model']['anchors'], (obj_thresh, nms_thresh))

        webcam_num = 0
        for file in os.listdir("/dev"):
            if file.startswith("video"):
                webcam_num += 1

        if webcam_num:
             yolo_process_exit('pass')
        else:
            yolo_process_exit('fail')

        try:
            yolo_process_exit('pass')
        except RuntimeError as e:
            yolo_process_exit('fail')

        batch_size = 1
        for i in range(webcam_num):
            globals()['images_{}'.format(i)] = []

        while True:
            for i in range(webcam_num):
                globals()['video_{}'.format(i)] = cv2.VideoCapture(i)
                globals()['ret_{}'.format(i)], \
                globals()['frame_{}'.format(i)] = globals()['video_{}'.format(i)].read()

                if globals()['ret_{}'.format(i)]:
                    string = 'Cam ' + str(i)
                    globals()['images_{}'.format(i)] += [globals()['frame_{}'.format(i)]]

                    if (len(globals()['images_{}'.format(i)]) == batch_size) or \
                            (globals()['ret_{}'.format(i)] is False and \
                                    len(globals()['images_{}'.format(i)])):
                        globals()['batch_boxes_{}'.format(i)] = get_yolo_boxes(infer_model,
                                                                               globals()['images_{}'.format(i)],
                                                                               net_h, net_w, config['model']['anchors'],
                                                                               obj_thresh, nms_thresh)
                        draw_boxes(globals()['images_{}'.format(i)][0], globals()['batch_boxes_{}'.format(i)][0],
                                    config['model']['labels'], obj_thresh)
                        globals()['person_{}'.format(i)], globals()['use_boxes_{}'.format(i)] = count_person(globals()['batch_boxes_{}'.format(i)][0],
                                                                                                             config['model']['labels'],
                                                                                                             obj_thresh)
                        globals()['average_density_{}'.format(i)] = density_estimator(globals()['person_{}'.format(i)], globals()['use_boxes_{}'.format(i)])
                        globals()['images_{}'.format(i)] = []

                    #print(globals()['average_density_{}'.format(i)])

                    message = 'video_' + str(i) + '/' + str(globals()['person_{}'.format(i)]) + '/' + str(globals()['average_density_{}'.format(i)])
                    print(message)
                    socket_client.send(message.encode())

                globals()['video_{}'.format(i)].release()
            i = 0
            time.sleep(5)
            cv2.destroyAllWindows()

    elif input_path[-4:] == '.txt':  # do detection on a video
        yolo_video_file_exit('pass') \
            if os.path.isfile(input_path) \
            else yolo_video_file_exit('fail')

        file = open(input_path, 'r')
        line_number = 0

        while True:
            line = file.readline().rstrip('\n')
            if not line : break
            globals()['video_out_{}'.format(line_number)] = output_path + line.split('/')[-1]
            globals()['video_reader_{}'.format(line_number)] = cv2.VideoCapture(line)
            globals()['nb_frames_{}'.format(line_number)] = int(globals()['video_reader_{}'.format(line_number)].get(cv2.CAP_PROP_FRAME_COUNT))
            globals()['nb_frames_h_{}'.format(line_number)] = int(globals()['video_reader_{}'.format(line_number)].get(cv2.CAP_PROP_FRAME_HEIGHT))
            globals()['nb_frames_w_{}'.format(line_number)] = int(globals()['video_reader_{}'.format(line_number)].get(cv2.CAP_PROP_FRAME_WIDTH))

            globals()['video_writer_{}'.format(line_number)] = cv2.VideoWriter(globals()['video_out_{}'.format(line_number)],
                                                                               cv2.VideoWriter_fourcc(*'MPEG'),
                                                                               50.0,
                                                                               (globals()['nb_frames_w_{}'.format(line_number)],
                                                                                globals()['nb_frames_h_{}'.format(line_number)]))
            globals()['images_{}'.format(line_number)] = []
            line_number += 1

        batch_size = 1

        while True:
            for i in range(line_number):
                globals()['ret_{}'.format(i)], globals()['frame_{}'.format(i)] = globals()['video_reader_{}'.format(i)].read()

                if globals()['ret_{}'.format(i)]:
                    globals()['images_{}'.format(i)] += [globals()['frame_{}'.format(i)]]

                    if (len(globals()['images_{}'.format(i)]) == batch_size) or \
                            (globals()['ret_{}'.format(i)] is False and
                             len(globals()['images_{}'.format(i)])):
                        globals()['batch_boxes_{}'.format(i)] = get_yolo_boxes(
                            infer_model,
                            globals()['images_{}'.format(i)],
                            net_h, net_w, config['model']['anchors'],
                            obj_thresh, nms_thresh)

                        for j in range(len(globals()['images_{}'.format(i)])):
                            draw_boxes(globals()['images_{}'.format(i)][j],
                                       globals()['batch_boxes_{}'.format(i)][j],
                                       config['model']['labels'], obj_thresh)

                            globals()['person_{}'.format(i)], \
                            globals()['use_boxes_{}'.format(i)] = count_person(
                                globals()['batch_boxes_{}'.format(i)][j],
                                config['model']['labels'],
                                obj_thresh)

                            globals()['average_density_{}'.format(i)] = \
                                density_estimator(
                                globals()['person_{}'.format(i)],
                                globals()['use_boxes_{}'.format(i)])
                            print(globals()['average_density_{}'.format(i)])

                            string = 'video_' + str(i)
                            print(string)
                            #message = string
                            #socket_client.send(message.encode())
                            message = string + '/' + str(globals()['person_{}'.format(i)]) + '/' + str(globals()['average_density_{}'.format(i)])
                            socket_client.send(message.encode())

                            if i == 0:
                                cv2.imshow(string, globals()['images_{}'.format(i)][j])
                                cv2.waitKey(1)
                        globals()['images_{}'.format(i)] = []
            time.sleep(5)
            cv2.destroyAllWindows()

        globals()['video_reader_{}'.format(i)].release()
        yolo_release_exit('pass') \
            if not globals()['video_writer_{}'.format(i)].release() \
            else yolo_release_exit('fail')

        try:
            yolo_process_exit('pass')
        except RuntimeError as e:
            yolo_process_exit('fail')

    else:  # do detection on an image or a set of images
        image_paths = []
        yolo_image_file_exit('pass') \
            if os.path.isfile(input_path) \
            else yolo_image_file_exit('fail')

        if os.path.isdir(input_path):
            for inp_file in os.listdir(input_path):
                image_paths += [input_path + inp_file]
        else:
            image_paths += [input_path]

        image_paths = [inp_file for inp_file in image_paths if
                       (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]

        # the main loop
        for image_path in image_paths:
            yolo_path_exit('pass') \
                if os.path.isfile(image_path) \
                else yolo_path_exit('fail')

            image = cv2.imread(image_path)

            # predict the bounding boxes
            boxes = get_yolo_boxes(infer_model, [image], net_h, net_w,
                                   config['model']['anchors'], obj_thresh,
                                   nms_thresh)[0]

            # draw bounding boxes on the image using labels
            draw_boxes(image, boxes, config['model']['labels'], obj_thresh)

            # print the number of predicted boxes
            person, use_boxes = count_person(boxes,
                                             config['model']['labels'],
                                             obj_thresh)
            average_density = density_estimator(person, use_boxes)
            show_density(image, person, average_density)

            cv2.imshow('video with bboxes', image)
            cv2.waitKey(3000)

            # write the image with bounding boxes to file
            yolo_save_exit('pass') \
                if cv2.imwrite(output_path + image_path.split('/')[-1],
                               np.uint8(image)) \
                else yolo_save_exit('fail')

            try:
                yolo_process_exit('pass')
            except RuntimeError as e:
                yolo_process_exit('fail')

"""if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Predict with a trained yolo model')
    argparser.add_argument('-c', '--conf', help='path to configuration file')
    argparser.add_argument('-i', '--input',
                           help='path to an image, a directory of images, a video, or webcam')
    argparser.add_argument('-o', '--output',
                           default='output/', help='path to output directory')
    
    args = argparser.parse_args()
    _main_(args)
    """
