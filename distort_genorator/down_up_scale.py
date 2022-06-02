from re import L
import cv2
import os
import glob
import random
import numpy as np
from pathlib import Path
import json
from collections import OrderedDict
from datetime import datetime
from sympy import Order

'''
input : video path, resize ratio, frame ratio
output : path of distorted video
description : 왜곡을 주고자 하는 비디오 경로 1개를 입력하면 인자로 준 비율에 따라 왜곡된 비디오를 만들어준다
주의사항 : rr은 낮을수록 , fr은 높을수록 더 왜곡이 강하게 적용된 비디오가 만들어진다
'''

# ========= param =========
writer_path = '/mnt/data/VQA/video/distorted/test'
fourcc_MP4V = cv2.VideoWriter_fourcc(*'mp4v')  # 이거로 안하면 오류
# ========= param =========


def down_up_scale(video_path, resize_ratio, frame_ratio, json_option = True):

    # writer_path = '/mnt/data/VQA/video/distorted/down_up_scaled'
    target_w, target_h = (resize_ratio, resize_ratio)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_name = Path(video_path).stem

    time_now = datetime.now()
    distort_video_path = writer_path + f'/{video_name}_scaled_{time_now}.mp4'
    writer = cv2.VideoWriter(distort_video_path,fourcc_MP4V, fps, (width, height)) 

    frame_idx = 0
    random_frame_number = random.randint(0, round(total_frame*(1-frame_ratio))-1)

    while True:

        frame_idx += 1
        ret, frame = cap.read()

        if not ret:
            break

        # 무한루프이므로 while이 아니라 if임을 주의..
        if random_frame_number <= frame_idx <= random_frame_number + total_frame*frame_ratio:

            frame = cv2.resize(frame, (int(
                width * target_w), int(height * target_h)), interpolation=cv2.INTER_AREA) # cv2.INTER_NEAREST : 속도는 빠른데 품질은 안좋다고함 : 이거로 시험해보기 ㄱㄱ !
            frame = cv2.resize(frame, (width, height))
            # cv2.putText(frame, 'distorted', (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

        writer.write(frame)

    print(f'=> down up scale 완료')

    # json 데이터 생성 및 저장
    if json_option == True :
        file_data = OrderedDict()    
        file_data['resize_ratio'] = resize_ratio
        file_data['frame_ratio'] = frame_ratio

        json_path = writer_path + f'/{video_name}_scaled_{time_now}.json'
        with open(json_path, 'w', encoding='utf-8') as make_file :
            json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
        print(f'=> json 저장 완료')
        ### return value : 왜곡된 비디오의 경로 ###
    return distort_video_path

