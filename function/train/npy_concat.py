import numpy as np
import glob
import sys

'''
input : .npy들 directory
output : ndarray(shape : num, 3884)
함수설명 : npy dir을 입력하면 하나하나 np.load하여 concat 후 return ndarray(shape : num, 3884)
'''
# ========== param ============
col_num = 3884
# ========== param ============

def npy_concat(feat_dir):

    result_feat = np.zeros(shape=(0, col_num))
    problem_list = []

    feats = sorted(glob.glob(feat_dir + '*.npy'))

    for idx, feat in enumerate(feats):
        
        feat = np.load(feat)
        if feat.shape[0] != col_num:
            # print(f'문제발생 : {idx+1}')
            problem_list.append(idx) # 비디오번호가 아니라 인덱스번호임으 주의 !
            continue

        result_feat = np.vstack((result_feat, feat))
        # ★ 이거 순서 매우 주의해야함!!! 이거 순서 바꿔서 진짜 일주일을 고생한듯
    np.nan_to_num(result_feat, copy=False)
    return result_feat, problem_list

# =============================

def npy_concat_from_npys(npys): # input이 npy들이 있는 전체경로가 아니라 npys(파일 리스트)인 경우 

    result_feat = np.zeros(shape=(0, col_num))
    problem_list = []
    for idx, feat in enumerate(npys):
        
        feat = np.load(feat)
        if feat.shape[0] != col_num:
            problem_list.append(idx) # 입력받은 npy파일들을 load했더니 차원이 3884가 아니면 pro_list에 넣는다 (비디오 번호가 아니라 입력받은 npy list의 인덱스 번호를 리턴해주는거)
            continue

        result_feat = np.vstack((result_feat, feat))
        # ★ 이거 순서 매우 주의해야함!!! 이거 순서 바꿔서 진짜 일주일을 고생한듯
    np.nan_to_num(result_feat, copy=False)

    # print(f'len : {result_feat.shape[0]}')
    print('npys load 및 concat 완료')
    print('=====================================')
    return result_feat, problem_list

# =============================

if __name__ == "__main__" :

    dir = '/mnt/data/VQA/feature/vqa_channel_24/'
    feat, box = npy_concat(dir)
    print(len(box))
    print(feat.shape)