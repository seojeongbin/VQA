import sys
import glob
from research.VQA.function.research.npy_concat import npy_concat

from research.VQA.function.research.make_mos import make_mos_list # 내가 이걸 지워버림 ㅎㅎ;;
from research.VQA.function.research.legacy_write_mosfile import write_mos

'''
input : 채널번호 (정수 하나)
output : 입력받은 채널에 대한 feat, mos 리턴
함수설명 : 채널을 입력하면 해당 채널에 대한 테스트 셋을 반환한다
'''
# ========== param ============
col_num = 3884
# ========== param ============

def make_test_channel_data(channel_num) : 

    feat_dir = f'/mnt/data/VQA/feature/vqa_channel_{channel_num}/'
    video_dir = f'/mnt/data/VQA/video/vqa_channel_{channel_num}/'
    feat, problem_list = npy_concat(feat_dir)
    # mos = make_mos_list(video_dir, problem_list)
    mos_list = write_mos(video_dir, 50 ,20)
    result_mos_list = []
    for idx, mos in enumerate(mos_list) :
        if idx in problem_list :
            continue
        result_mos_list.append(mos)

    print('=====================================')
    return feat, result_mos_list
