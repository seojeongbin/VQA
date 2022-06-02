# 잘못 배치되었을경우 intensity_1 ~ 100 폴더에 있는 전체 비디오들을 상위폴더에 다시넣기

import os
import glob
import shutil


def move_video_files(from_path, to_path):
    for video in glob.glob(from_path + '/*mp4'):
        shutil.move(video, to_path)

# usage : from_dir은 끝이 /면 안됨
def move_all_files(from_dir, to_dir) :
    file_list = os.listdir(from_dir) # 입력받은 디렉토리에 있는 전체 파일 목록
    for file in file_list :
        shutil.move(from_dir + file, to_dir)
    print('파일 이동 완료') 



if __name__ == "__main__":

    to_path = '/mnt/data/VQA/video/all_channels_with_json/'
    dir_box = ['/mnt/data/download/12000_16000/vqa_sample/']
    
    for dir in dir_box :
        move_all_files(dir, to_path)
