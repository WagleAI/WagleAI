

def yolo_argument_exit(status):
    if status.lower() == 'pass':
        print('**** Arguments passed well. ****')
    else:
        print('!!!! Wrong arguments passed. '
              'The program will be stopped. !!!!')
        exit(1)


def yolo_path_exit(status):
    if status.lower() == 'pass':
        print('**** This is a valid path. ****')
    else:
        print('!!!! Something wrong with path. '
              'Check the path and try again. !!!!')
        exit(1)


def yolo_config_file_exit(status):
    if status.lower() == 'pass':
        print('**** The config file loaded well. ****')
    else:
        print('!!!! The config file was not loaded. '
              'The program will be stopped. !!!!')
        exit(1)


def yolo_create_exit(status):
    if status.lower() == 'pass':
        print('**** The file or the folder created well. ****')
    else:
        print('!!!! The file or the folder did not create. '
              'The program will be stopped. !!!!')
        exit(1)


def yolo_model_exit(status):
    if status.lower() == 'pass':
        print('**** The h5 file loaded well. ****')
    else:
        print('!!!! The model file was not loaded. '
              'The program will be stopped. !!!!')
        exit(1)


def yolo_weights_exit(status):
    if status.lower() == 'pass':
        print('**** The w')


def yolo_image_file_exit(status):
    if status.lower() == 'pass':
        print('**** The image file loaded well. ****')
    else:
        print('!!!! The image file was not loaded. '
              'The program will be stopped !!!!')
        exit(1)


def yolo_video_file_exit(status):
    if status.lower() == 'pass':
        print('**** The video file loaded well. ****')
    else:
        print('!!!! The video file was not loaded. '
              'The program will be stopped !!!!')
        exit(1)


def yolo_webcam_exit(status):
    if status.lower() == 'pass':
        print('**** The webcam connected successfully. ****')
    else:
        print('!!!! The webcam disconnected. '
              'Check the connection and try again. !!!!')
        exit(1)


def yolo_release_exit(status):
    if status.lower() == 'pass':
        print('**** The processes released well. ****')
    else:
        print('!!!! Some errors occurred while releasing processes. '
              'The program will be stopped !!!!')
        exit(1)


def yolo_save_exit(status):
    if status.lower() == 'pass':
        print('**** The image saved well. ****')
    else:
        print('!!!! Some errors occurred while saving the image. '
              'The program will be stopped. !!!!')
        exit(1)


def yolo_process_exit(status):
    if status.lower() == 'pass':
        print('**** All processes ended completely. ****')
    else:
        print('!!!! Some errors occurred before the process ends. '
              'The program will be stopped. !!!!')
        exit(1)


def webcam_exit(status):
    if status.lower() == 'pass':
        print('**** The Webcams are completely connected. ****')
    else:
        print("!!!! There are no webcams connected."
              "The program will be stopped. !!!!")
        exit(1)