import pandas as pd
from method_similarity import euclidean_distance, manhattan_distance, hamming_distance
import glob
import sys
import scipy.io
import numpy as np


if __name__ == "__main__":

    features_by_python_path = '/home/nextlab/VQA/features/features_by_python5/' # python으로 뽑은 개별 feature들이 모아져있는 경로
    features_by_matlab_path = '/home/nextlab/projects/athena-runner-algo-test/research/matrix_similarity/features_by_python_intensity_clean.mat' # matlab으로 뽑은 features
    # features_by_python_path_new = '/home/nextlab/VQA/features/features_by_python_newconvolve/'

    python = sorted(glob.glob(features_by_python_path + '*.npy'))
    # python_new = sorted(glob.glob(features_by_python_path_new + '*.npy'))
    matlab = scipy.io.loadmat(features_by_matlab_path)['feats_mat']


    len = 800
    problem_idx = [295]
    df = pd.DataFrame(columns=[])

    # 각 array들을 비교
    for i in range(len):

        python_i = np.load(python[i])
        matlab_i = matlab[i]

        if i in problem_idx:
            continue
        df = df.append({'Euclidean': euclidean_distance(python_i, matlab_i),
                        'Manhattan': manhattan_distance(python_i, matlab_i),
                        'Hamming': 0},
                       ignore_index=True)

    print(df.describe())
