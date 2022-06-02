import sys
import pandas as pd
from make_npy_json_df import make_df_npy_json
from npy_concat import npy_concat_from_npys # 모듈 임포트 하는거는 제작하고 있는 파일과의 위치관계로 정하는듯 !!
import json
import numpy as np
import pickle

# ========== param ============
score_min = 0
score_max = 5
intensity_min = 0
intensity_max = 0.01
# ========== param ============


'''
input : intensity from one json file
output : mos converted from intensity
함수설명 : json에서 읽은 화면깨짐 intenstiy 를 넣으면 mos 점수로 반환해서 넣어준다
'''
# 인자에 따른 방식이 변경됨에 따라 해당함수도 수정소요가 발생할 수 있음
def intensity_into_mos(intensity) :
    
    multiple_num = (score_max - score_min) / (intensity_max - intensity_min)
    mos = round(intensity * multiple_num,10) # 예를들어 500 * intensity max(0.01) => 5점이 되는거임
    return mos


'''
input : dataframe
output : train에 넣을 데이터셋 (feat, mos )
함수설명 : npy, json path가 저장된 dataframe을 입력하면 feat와 mos를 반환한다. 문제있는 애들은(problem_list) 제외해준다.
'''
def load_data_from_csv(df, saveoption = False) :

    json_files = df['json_path'].tolist()
    npy_files = df['npy_path'].tolist()
    feat_ndarrays, problem_list = npy_concat_from_npys(npy_files)
    
    print(f'최초 입력받은 데이터 수 : {len(npy_files)}')
    print(f'차원이 3884차원이 아닌 npy의 수 : {len(problem_list)}')
    mos_list = []

    for idx, json_file in enumerate(json_files) :
        if idx in problem_list :
            continue
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        intensity = json_data['args']['intensity']
        mos = intensity_into_mos(intensity)
        mos_list.append(mos)

    feat_num = feat_ndarrays.shape[0]
    mos_num = len(mos_list)

    if feat_num != mos_num :
        print('정상적이지않은 입력입니다')
        sys.exit()

    if saveoption == True :
        # feat 저장
        savepath = '/home/nextlab/projects/athena-runner-algo-test/research/VQA/function/research/temp_save/'
        np.save(savepath + 'saved_feat.npy', feat_ndarrays)
        print('-> 피쳐 저장 완료')
        # mos 저장
        open_file = open(savepath + 'saved_mos.pkl', "wb")
        pickle.dump(mos_list, open_file)
        open_file.close()
        print('-> mos 저장 완료')

    print(f'데이터프레임으로부터 피쳐 및 GT 로드 완료, 데이터 수 : {feat_num}')
    print('=====================================')

    return feat_ndarrays, mos_list


if __name__ == "__main__" :

    npy_dir = '/mnt/data/VQA/feature/all_channels_with_json_2/' # rapique extracted feature 들이 있는 디렉토리
    df = make_df_npy_json(npy_dir)
    feat, mos = load_data_from_csv(df)
    print(f'feat 개수 : {feat.shape[0]}')
    print(f'mos 개수 : {len(mos)}')
    print()
    print(mos)


