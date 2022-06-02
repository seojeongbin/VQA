from pathlib import Path
from datetime import datetime
from collections import OrderedDict
from glitchify import glitchify
from down_up_scale import down_up_scale
import json
import os
import sys

'''
input : video_path, rr, fr, gr
output : glitchify => down up scale 순으로 적용된 mix - distorted video path
descript : down up scale + glitchify 가 섞인 방법으로 왜곡 비디오를 만듦
'''

writer_path = '/mnt/data/VQA/video/distorted/test'

def mix(video_path, rr, fr, gr) :
    
    video_name = Path(video_path).stem
    time_now = datetime.now()

    glitched_path= glitchify(video_path, gr, False)
    mixed_path = down_up_scale(glitched_path, rr, fr, False)
    changed_mixed_path = writer_path + f'/{video_name}_mixed_{time_now}.mp4'
    os.rename(mixed_path, changed_mixed_path)
    
    print('=> mix 완료')
    os.remove(glitched_path)
    
    # json 데이터 생성 및 저장
    
    file_data = OrderedDict()
    file_data['intensity'] = gr    
    file_data['resize_ratio'] = rr
    file_data['frame_ratio'] = fr
    
    json_path = writer_path + f'/{video_name}_mixed_{time_now}.json'
    with open(json_path, 'w', encoding='utf-8') as make_file :
        json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
    print('=> json 저장 완료')
    
    return changed_mixed_path
