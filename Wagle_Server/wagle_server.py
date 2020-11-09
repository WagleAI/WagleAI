from socket import *
from _thread import *
from datetime import datetime
import json


HOST = '127.0.0.1'
PORT = 8080

socket_server = socket(AF_INET, SOCK_STREAM)
socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket_server.bind((HOST, PORT))
socket_server.listen()

print('server start')


def threaded(socket_client, addr):
    print('Connected by :', addr[0], ":", addr[1])

    while True:

        try:
            data = socket_client.recv(1024)

            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            print('Received from ' + addr[0], ":", addr[1], data.decode('utf-8'))

            #socket_client.send(data)

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

        json_data = {}
        data_lists = str(data.decode('utf-8'))
        data_list = data_lists.split('/')
        if data[0] == 'connected successly':
            continue

        name_string3 = 'video_' + data_list[0][-1] + '.json'

        with open(name_string3, 'r') as json_file:
            json_data = json.load(json_file)

        #print(json_data)

        if data_list[0][-1] == '0':
            loc = "hongdae"
            latitude = 37.5572654
            longitude = 126.9241721
        elif data_list[0][-1] == '1':
            loc = "gangnam"
            latitude = 37.5076804
            longitude = 126.9529051
        elif data_list[0][-1] == '2':
            loc = 'shinchon'
            latitude = 37.5580362
            longitude = 126.9389666
        elif data_list[0][-1] == '3':
            loc = 'itaewon'
            latitude = 37.5388338
            longitude = 126.9834483
        elif data_list[0][-1] == '4':
            loc = 'sindorim'
            latitude = 37.5106925
            longitude = 126.8739066
        elif data_list[0][-1] == '5':
            loc = 'gosok terminal'
            latitude = 37.5049142
            longitude = 127.0027264
        elif data_list[0][-1] == '6':
            loc = 'Seoul station'
            latitude = 37.5536972
            longitude = 126.9669926
        elif data_list[0][-1] == '7':
            loc = 'sadang'
            latitude = 37.5023383
            longitude = 126.914903
        elif data_list[0][-1] == '8':
            loc = 'suwon'
            latitude = 37.266388
            longitude = 126.9982113
        else:
            loc = 'incheon airport'
            latitude = 37.4601908
            longitude = 126.438507

        now = datetime.now()
        json_date = now.strftime('%Y-%m-%d')
        json_time = now.strftime('%H:%M:%S')
        json_data['density'].append({
            "Date": json_date,
            "Time": json_time,
            "Location": loc,
            "Latitude" : latitude,
            "Longitude" : longitude,
            "Person": data_list[1],
            "Density": data_list[2]
        })

        with open(name_string3, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

    socket_client.close()

length = 0

#file = open('./filelist.txt', 'r')
file = open('./webcamlist.txt', 'r')
while True:
    line = file.readline()
    if not line : break
    length += 1

file.close()

for i in range(length):
    json_data_temp = {}
    json_data_temp['density'] = []
    now = datetime.now()
    json_date = now.strftime('%Y-%m-%d')
    json_time = now.strftime('%H:%M:%S')
    json_data_temp['density'].append({
        "Date": json_date,
        "Time": json_time,
        "Location": 999,
        "Latitude" : 0.0,
        "Longitude" :0.0,
        "Person": 0,
        "Density": 0
    })
    name_string3 = 'video_' + str(i) + '.json'
    with open(name_string3, 'w', encoding='utf-8') as make_file:
        json.dump(json_data_temp, make_file, indent=4)

while True:
    print('wait')

    socket_client, addr = socket_server.accept()
    start_new_thread(threaded, (socket_client, addr))

socket_server.close()
