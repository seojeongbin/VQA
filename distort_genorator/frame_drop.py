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
import time
import sys

'''
input : video path, drop_ratio
output : path of distorted video
description : 전체 프레임에서 drop_frame만큼 삭제 후 직전 프레임으로 freeze 시킨 영상 (멈칫거리는, 버퍼링 같은 영상) 을 생성
'''

# ========= param =========
writer_path = '/mnt/data/VQA/video/distorted/frame_drop/'
fourcc_MP4V = cv2.VideoWriter_fourcc(*'mp4v')  # 이거로 안하면 오류
drop_frame_min, drop_frame_max = 1, 10

# ========= param =========


def frame_drop(video_path, total_drop_frame, json_option=True):

    # video information
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # writer information
    video_name = Path(video_path).stem
    time_now = datetime.now()
    distort_video_path = writer_path + f'/{video_name}_scaled_{time_now}.mp4'
    writer = cv2.VideoWriter(
        distort_video_path, fourcc_MP4V, fps, (width, height))

    # create list drop frames
    all_dropped_indices = set()  # []랑 같음.
    total_frames = set(range(total_frame))  # 0 ~ 599
    while len(all_dropped_indices) < total_drop_frame:
        random_idx = random.choice(list(total_frames))  # 250
        random_num = random.randint(drop_frame_min, drop_frame_max)  # 7
        all_dropped_indices = all_dropped_indices.union(
            set(range(random_idx, min(total_frame, random_idx + random_num))))  # 합집합
        total_frames -= all_dropped_indices
    all_dropped_indices -= {0}
    # start out_video write
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx not in all_dropped_indices:  # 정상 프레임 경우
            normal_frame = frame
            writer.write(normal_frame)
        else:  # 빠져야 되는 프레임의 경우 그 전 프레임을 사용한다
            writer.write(normal_frame)
        frame_idx += 1

    print(f'=> frame_drop 비디오 생성 완료')

    # json 데이터 생성 및 저장
    if json_option == True:
        file_data = OrderedDict()
        file_data['total_drop_frame'] = total_drop_frame

        json_path = writer_path + f'/{video_name}_scaled_{time_now}.json'
        with open(json_path, 'w', encoding='utf-8') as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
        print(f'=> json 생성 완료\n')

    return distort_video_path
