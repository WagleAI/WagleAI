import cv2
import os

args_file = './filelist.txt'
file = open(args_file, 'w')
input_list = []

while True:
    line = file.readline()
    if not line : break

    if os.path.isfile(line):
        input_list.append(line)


for i in range(len(input_list)):
    globals()['Cap_{}'.format(i)] = cv2.VideoCapture(input_list[i])
    globals()['ret_{}'.format(i)] = 0
    globals()['frame_{}'.format(i)] = 0


for i in range(len(input_list)):



file.close()
