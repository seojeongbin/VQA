from pathlib import Path
from multiprocessing import Process
import glob
import numpy as np
from sympy import N
# from algorithm.vqa.rapique.feature.rapique_features import calc_rapique_features
from algorithm.vqa.rapique.feature.rapique_features_videopath import calc_rapique_features_videopath as calc_rapique_features
# from .research.VQA.function.research.video_json_rename import sort_and_rename
import time
import sys
import pandas as pd
import os
import traceback
import cv2
import multiprocessing

'''
input : video dir, saved dir, chunk size
output : feature
설명 : video dir의 영상들을 chunk size만큼 멀티프로세를 이용해서 영상을 뽑아 saved dir에 저장한다
'''



def extract_feature(video_path, save_dir):
    
    name = Path(video_path).stem
    save_path = os.path.join(save_dir, f'{name}.npy')
    try:
        features = calc_rapique_features(video_path)
        assert features.shape[0] == 3884  # 이 조건이 성사되지 않으면 에러를 발생시킴.
        np.save(save_path, features)
        print(f'save npy => {save_path}')
    except Exception as e:
        np.save(save_path.replace('.npy', '_error.npy'), np.array([]))
        print(f"error {e}, {traceback.format_exc()}")
        
def chunks(lst, n):
    # 그냥 균등한 구간을 만들어주는 함수임
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

    '''
    print(f'range_list : {range_list}')
    => range_list :[range(0, 50), range(50, 100), range(100, 150), range(150, 200), range(200, 250), range(250, 300), range(300, 350), range(350, 400),
    range(400, 450),range(450, 500), range(500, 550), range(550, 600), range(600, 650), range(650, 700), range(700, 750), range(750, 800)]
    '''

def run(range_element, saved_dir):
    for idx in range_element:
        video_path = videos[idx]
        extract_feature(video_path, saved_dir)
        

if __name__ == "__main__":

    # ========== param ============
    video_dir = '/mnt/data/VQA/video/all_channels_with_json/'
    saved_dir = '/mnt/data/VQA/feature/all_channels_with_json_2/'
    # chunk_size = 80 -> 이렇게하면 프로세스 수 100개 되는셈 !! => 8000개 뽑을때마다 자꾸 3000개 정도만 나온다. 프로세스 개수 때문일까?
    # ========== param ============

    videos = sorted(glob.glob(video_dir + '/*mp4'))
    data_size = len(videos)
    num_cores = multiprocessing.cpu_count() 
    chunk_size = data_size // num_cores 

    # print(f'뽑을 영상 수 : {data_size}, 코어 수 : {num_cores}, chunk 사이즈 : {chunk_size}')
    # 한번에 프로세스 수 만큼 생성됨
    # sys.exit()

    start = time.time()
    procs = []

    range_list = list(chunks(range(data_size), chunk_size))

    for range_element in range_list:
        p = Process(target=run, args=(range_element, saved_dir))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    print(f'최종 소요시간 : {time.time() - start}')
