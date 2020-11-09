# WagleAI

## Introduction
YOLOv3 딥러닝 모델을 활용하여 한국의 거리 밀집도를 실시간으로 분석하고  
분석된 정보를 사용자에게 시각화하여 제공할 수 있는 오픈소스 소프트웨어입니다.

## Installing
### 1. 가상환경 설정
기본적인 실행하기 위한 과정은 다음과 같습니다.
```bash
conda create --name yolo3 python=3.7
```
### 2. 시스템 환경 설정
동작을 위해 cuda 10.0, cudnn 7.6.5, tensorflow(-gpu) 1.15.0 버전은 반드시 맞춰주세요.  
패키지들의 설치를 위해 다음 명령어를 실행해 주세요.
```bash
pip install -r requirements.txt
```

## Detection
### 1. Pre-trained model 다운로드
사람을 단일 클래스로 학습한 모델 파일은 다음 링크에서 받으실 수 있습니다.  
<a>https://drive.google.com/file/d/11d08K8r7hgqcTD-jMRbGl7lao00OlzM7/view?usp=sharing</a>  
### 2. predict 실행
Detection 하기 위한 이미지나 동영상 파일을 프로젝트의 하위 폴더에 위치시킨 뒤 다음 명령어를 입력해 주세요.
```bash
python wagle.py --mode predict -c json파일의_경로 -i 이미지/동영상_파일의_경로 --host 로그서버의 IP주소
```
탐지 결과는 ```output```폴더에 저장됩니다.

## Training
### 1. 데이터 준비
본 모델을 학습하기 위해 다음과 같은 데이터셋을 사용하였습니다.  
```
인도보행영상 : http://www.aihub.or.kr/aidata/136  
Multiple Object Tracking Benchmark : https://motchallenge.net  
```
파일 구조는 다음과 같이 설정해주세요
```
.
+-- data
|   +-- MOT
|   |   +-- MOT16
|   |   |   +-- test
|   |   |   +-- train
|   |   +-- MOT20
|   |   |   +-- test
|   |   |   +-- train
|   +-- Pedestrian
|   |   +-- Bbox_#
|   |   +-- Bbox_#
```
MOT데이터를 활용해 train/valid 폴더를 분리할 경우 다음 명령어를 입력해주세요.
```bash
python wagle.py --mode dataset -p ./data/MOT -m True -t data/train -v data/valid
```
보행자 데이터를 활용해 train/test 폴더를 분리할 경우 다음 명령어를 입력해주세요.
```bash
python wagle.py --mode dataset -p ./data/Pedestrian -m False, -t data/train -v data/valid
```
### 2. config_.json파일 수정하기
zoo 폴더 하위에 위치한 json 형식의 configuration file은 다음과 같습니다.
```python
{
    "model" : {
        "min_input_size":       416,
        "max_input_size":       512,
        "anchors":              [4,21, 6,33, 10,48, 14,68, 20,99, 29,132, 38,191, 56,242, 87,324],
        "labels":               ["person"]
    },

    "train": {
        "train_image_folder":   "/home/Users/Desktop/Human_Detection/keras-yolov3-master/data/train/image/",
        "train_annot_folder":   "/home/Users/Desktop/Human_Detection/keras-yolov3-master/data/train/annot/",
        "cache_name":           "human_train.pkl",

        "train_times":          1,
        "batch_size":           4,
        "learning_rate":        1e-4,
        "nb_epochs":            50,
        "warmup_epochs":        3,
        "ignore_thresh":        0.5,
        "gpus":                 "1",

        "grid_scales":          [1,1,1],
        "obj_scale":            5,
        "noobj_scale":          1,
        "xywh_scale":           1,
        "class_scale":          1,

        "tensorboard_dir":      "log_human",
        "saved_weights_name":   "human.h5",
        "debug":                true
    },

    "valid": {
        "valid_image_folder":   "/home/Users/Desktop/Human_Detection/keras-yolov3-master/data/valid/image/",
        "valid_annot_folder":   "/home/Users/Desktop/Human_Detection/keras-yolov3-master/data/valid/annot/",
        "cache_name":           "human_valid.pkl",

        "valid_times":          1
    }
}
```
train/valid 폴더를 이전 단계에서 생성한 경로로 바꾸어줍니다.
saved_weights_name에 지정할 pre-trained 모델이 없을 경우 다음 링크에서 backend.h5 파일을 다운받아주세요.  
https://bit.ly/39rLNoE  

### 3. 데이터셋에 맞는 Anchor mask 생성하기 (선택사항)
```bash
python wagle.py --mode gen_anchor -a 9 -c json파일의_경로
```
클러스터링을 통해 학습할 이미지들의 크기에 맞는 Anchor값 9개를 출력합니다.  
config 파일의 ```anchors```부분에 복사하여 붙여놓으시면 됩니다.

### 4. 학습 시작하기
```bash
python wagle.py --model train -c json파일의_경로
```
가장 정확도가 높았던 best model이 ```saved_weights_name``` 부분에 적었던 이름으로 저장됩니다.  
valid 셋에 대해 loss가 3epoch동안 줄어들지 않으면 early stop합니다.


