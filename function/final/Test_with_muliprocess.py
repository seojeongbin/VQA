import os
import multiprocessing

from py import process
from algorithm.vqa.rapique.feature.rapique_features import calc_rapique_features
from algorithm.vqa.rapique.feature.rapique_features_videopath import calc_rapique_features_videopath
from collections import deque
from multiprocessing import Process, Queue
from threading import Thread
from algorithm.vqa.rapique.regressor import Logger
from common.logger import set_logger
from research.VQA.about_model.npy_concat import npy_concat
import warnings
import cv2
import numpy as np
import joblib
import time
import glob
import pandas as pd
import sys
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'




# 전체에 공유되면서, 변하지않는 값.
#### ___________________ global parameters ______________________ ###
regressor = joblib.load(
    '/home/nextlab/projects/athena-runner-algo-test/research/VQA/pkl/2022-05-18/regressor(grid).pkl')
scaler = joblib.load(
    '/home/nextlab/projects/athena-runner-algo-test/research/VQA/pkl/2022-05-18/scaler(grid).pkl')
frame_pass_cnt = 3
#### ___________________ global parameters ______________________ ###



def predict(feat, regressor, scaler):

    np.nan_to_num(feat, copy=False)
    X = feat.reshape(1, -1)
    X = scaler.transform(X)
    predicted_mos = regressor.predict(X)
    return predicted_mos


def calc_mos(frames, cluster_idx, output_queue):

    feat = calc_rapique_features(frames)
    output_queue.put((feat, cluster_idx))


def split_video(video_path, split_sec, verbose_option=False):

    start = time.time()

    if verbose_option == False:
        set_logger('main_logger').setLevel(50)  # 20이 default, 50은 심각한 문제인경우
    else:
        set_logger('main_logger').setLevel(20)

    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_runnig_time = int(total_frames / fps)
    frame_unit = split_sec * frame_pass_cnt
    # 한 구간으로 결정되는 frame 수 = (fps // 3) * frame_unit -> fps 나누면 (초) -> 즉 원하는 초의 * 3 이 frame_unit?

    print(
        f'\n* 비디오 정보 => length : {video_runnig_time}sec, total_frames : {total_frames}frames, fps : {fps}, frame_unit : {frame_unit}frames \n')

    frame_queue = deque([], maxlen=frame_unit)  # frame unit 만큼 수용하는 공간

    cluster_idx = 0  # 몇번째 군집인지 : 이거 지우면 안됨
    procs = []
    # df = pd.DataFrame(columns=[])
    score_dict = {}

    # # output_queue = Queue() -> ★★★★★ 이거안하면 프로세스 3번부터는 join안됨
    output_queue = multiprocessing.Manager().Queue()
    for frame_index in range(total_frames):
        _, frame = video.read()

        if frame_index % max(fps // frame_pass_cnt, 1) != 0:
            continue

        frame_queue.append(frame)

        if len(frame_queue) == frame_queue.maxlen:

            proc = Process(target=calc_mos, args=(
                frame_queue, cluster_idx, output_queue))
            print(f'\n{cluster_idx+1}번째 process 할당')
            cluster_idx += 1
            proc.start()
            procs.append(proc)
            print(f'현재 procs : {procs}\n')
            frame_queue.clear()

    for proc in procs:
        proc.join()  # 주의

    while output_queue.qsize() > 0:

        feat, cluster = output_queue.get()
        mos = predict(feat, regressor, scaler)
        pred_score = round(mos[0], 4)
        # df = df.append({'section': int(cluster+1), 'predict_score': pred_score},
        #                ignore_index=True)  # append말고 concat을 권장하심
        score_dict[f'cluster_{int(cluster+1)}'] = pred_score
    
    pred_average = round(sum(score_dict.values()) / len(score_dict),4)
    sorted_dict = dict(sorted(score_dict.items()))
    
    video.release()
    print(f'\n소요시간 : {round(time.time() - start, 4)}sec')

    return sorted_dict, pred_average  # df 말고 리스트(혹은 딕셔너리) => 딕셔너리


if __name__ == "__main__":

    video_path = '/mnt/data/VQA/video/all_channels/video_0001.mp4'
    split_sec = 2
    dict, avg = split_video(video_path, split_sec)
    print(dict,'\t* 평균점수 : ',avg)

