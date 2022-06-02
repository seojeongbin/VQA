import os 
import glob


'''
input : video_json_dir (영상과 json이 같이 있는, 구글 드라이브에서 막 압축해제한 거대 디렉토리)
output : 변경사항이 적용된 path
함수설명 : 구글 드라이브에서 압축해제 한 디렉토리를 넣으면 왜곡 세기에 따라(생성날짜 정렬) 오름차순을 하고 0001 ~ len 만큼 주기 및 이름변경을 한다
'''

# 다음과정은 extract_features.py -> make_npy_json.py

def sort_and_rename(path) :
    
    # length = len(glob.glob(path + '/*mp4')) # 8000
    # zfill_num = len(str(length)) # 4
    length = 8000
    zfill_num = 4

    for idx, video in enumerate(sorted(glob.glob(path + '/*mp4'))) :
        idx += 1
        idx = str(idx).zfill(zfill_num)
        os.rename(video, path + f'/video_{idx}.mp4')

    for idx, video in enumerate(sorted(glob.glob(path + '/*json'))) :
        idx += 1
        idx = str(idx).zfill(zfill_num)
        os.rename(video, path + f'/video_{idx}.json')

    print('정렬 및 파일이름 변경완료')
    print('=====================================')
    return path

    
if __name__ == "__main__" :

    video_json_dir = '/mnt/data/VQA/video/all_channels_with_json'
    sort_and_rename(video_json_dir)
