import random
import os
from pathlib import Path
from datetime import datetime
from collections import OrderedDict
import json

output_dir = '/mnt/data/VQA/video/distorted/test/'
buffer_size = 100
header_size = 200

def glitchify(input_path, intensity, json_option = True, **_):
    video_name = Path(input_path).stem
    time_now = datetime.now()
    output_path = output_dir + f'{video_name}_glitched_{time_now}.mp4'
    with open(input_path, "rb") as fin:
        with open(output_path, "wb") as fout:
            # protect the header
            fout.write(fin.read(header_size))
            while True:
                in_byte = fin.read(buffer_size)
                if not in_byte:
                    break
                if (random.random() < intensity / 100):
                    out_byte = os.urandom(buffer_size)
                else:
                    out_byte = in_byte
                fout.write(out_byte)
    print('=> glitch 완료')

    # json 데이터 생성 및 저장
    if json_option == True :
        file_data = OrderedDict()    
        file_data['intensity'] = intensity

        json_path = output_dir + f'{video_name}_glitched_{time_now}.json'
        with open(json_path, 'w', encoding='utf-8') as make_file :
            json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
        print(f'=> json 저장 완료')
        ### return value : 왜곡된 비디오의 경로 ###
        return output_path, json_path

    else :
        return output_path
