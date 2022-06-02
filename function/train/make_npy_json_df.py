import sys
import pandas as pd
import glob
from pathlib import Path
# from .research.VQA.function.research.video_json_rename import sort_and_rename

'''
input : json dir, npy dir
output : dataframe (columns : file name, json path, npy path)
설명 : 입력받은 json, npy 디렉토리로 부터 순서대로 append한다. filename의 경우 Path().stem을 이용하여 구한다.
'''
'''
*수정사항* : npy가 8천개중 3천개만 만들어지고 이런경우가 있어서 npy에서 정상적인 인덱스 보고 갈아끼우는 식으로 바꿈
'''

def make_df_npy_json(json_dir, npy_dir) : 

    df = pd.DataFrame(columns=[])
    json_dir = sorted(glob.glob(json_dir + '*.json'))
    npy_dir = sorted(glob.glob(npy_dir + '*.npy'))

    if len(json_dir) != len(npy_dir) :
        print(f'json_dir의 len : {len(json_dir)}, npy_dir의 len : {len(npy_dir)}')
        print('정상적이지 않은 입력입니다')
        sys.exit()

    for json_path, npy_path in zip(json_dir, npy_dir) :


        df_temp = pd.DataFrame({'file_name' : [Path(json_path).stem],
        'json_path' : [json_path], 
        'npy_path' : [npy_path]})

        df = pd.concat([df, df_temp], ignore_index = True, axis = 0)

    print('json dir, npy dir로 부터 dataframe 생성완료')
    print('=====================================')
    return df


def make_df_npy_json(npy_dir) : 

    df = pd.DataFrame(columns=[])
    npy_dir = sorted(glob.glob(npy_dir + '*.npy'))

    for npy_path in npy_dir : 

        name = '/' + str(Path(npy_path).stem)
        parent = Path(npy_path).parent
        # json의 경우 npy_path를 기준으로 중간경로랑 확장자만 바꿔주는 셈이다
        json_path = str(parent) + str(name) + '.json'
        json_path = json_path.replace('feature','video')
        json_path = json_path.replace('json_2','json') # ★ 여기 나중에 바꿔야함

        df_temp = pd.DataFrame({'video_name' : [name[1:] + '.mp4'],
        'json_path' : [json_path], 
        'npy_path' : [npy_path]})

        df = pd.concat([df, df_temp], ignore_index = True, axis = 0)

    print('dataframe(csv) 생성완료')
    print('=====================================')
    return df


if __name__ == "__main__":

    # json_dir = '/mnt/data/VQA/video/all_channels_with_json/' # mp4, json 파일이 있는 디렉토리
    npy_dir = '/mnt/data/VQA/feature/all_channels_with_json_2/' # rapique extracted feature 들이 있는 디렉토리
    result = make_df_npy_json(npy_dir)
    print(result)