import sys
import numpy as np
import cv2
import glob
import random
import warnings
warnings.filterwarnings("ignore")


def blend_video(video_dir, name) :
    
    # 합쳐지는비디오들의 fps 및 크기들이 같다는 전제필요
    save_path = '/home/nextlab/projects/athena-runner-algo-test/research/videos/macro_block_blended/'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path + f'blended_video_{name}.mp4', fourcc, 60, (1920, 1080))

    for idx, video_path in enumerate(video_dir) :
        print(f'{idx+1}번째 비디오 합성 시작')
        video = cv2.VideoCapture(video_path)
        frame_cnt = round(video.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(frame_cnt):
            ret, frame = video.read()
            if not ret : sys.exit()
            out.write(frame)

        video.release() # 이거 주석처리해도 여전히 문제발생 (에러코드, 합성 중간까지만 됨 => 바깥 for문 전체 못돎)
    out.release()

    return out

if __name__ == "__main__" :
    
    video_dir = glob.glob('/home/nextlab/VQA/video/glitched_10seconds_clean/'+'*.mp4')
    for i in range(6) :
        print(f'{i+1}번째 시작') 
        random.shuffle(video_dir) # 이거 print하면 오류난다 저러면 바로 반영되는거라서
        want_number = 5
        blend_video(video_dir[:want_number],i+1) # 이 숫자만큼 합성이 됨 (5개니까 50초짜리 영상이 되는것) 
        print(f'{i+1}번째 종료')