'''
argument에 따라 비디오에 1) 왜곡방법 2) 그 방법의 intensity 를 적용하여
왜곡된 비디오를 만들어주는 함수
'''
import argparse
import warnings
from frame_drop import frame_drop
from down_up_scale import down_up_scale
from glitchify import glitchify
import glob
warnings.filterwarnings("ignore")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, default='scale',
                        help='kind of distort method')
    parser.add_argument('--fr', type=float, default=0.0,
                        help='frame ratio in down-up scaling') 
    parser.add_argument('--rr', type=float, default=0.0,
                        help='resize ratio in down-up scaling')
    parser.add_argument('--dr', type=float, default=0.0,
                        help='drop_ratio in frame_drop')  
    parser.add_argument('--gr', type=float, default=0.03,
                        help='glitch_ratio in glitchify')
    args = parser.parse_args()
    return args


def main(args):
    
    # 여러 종류의 왜곡을 담은 비디오를 만드는 코드를 작성하는 거임
    # 여러개 같이가 가능하도록 되어야함!!
    # 여러개 같이하는경우 매크로블럭 먼저하고 이후에 리사이즈 해야함.!!
    # glitchify에도 json 나오도록 달기.
    
    video_dir = sorted(glob.glob('/mnt/data/VQA/video/all_channels_with_json/*.mp4'))[:20]
    
    fr = args.fr
    rr = args.rr
    dr = args.dr
    gr = args.gr

    for video_path in video_dir :

        if args.method == 'scale' :
            down_up_scale(video_path, rr, fr)
            
        elif args.method == 'frame_drop' :
            frame_drop(video_path, dr)
        
        elif args.method == 'glitchify' :
            glitchify(video_path, gr)
            


if __name__ == '__main__':

    args = arg_parser()
    main(args)

