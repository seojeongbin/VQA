from sklearn.model_selection import GridSearchCV, train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
import numpy as np
import pandas as pd
import time
import sys
from datetime import datetime
import os
import warnings
# from algorithm.vqa.rapique.regressor import Logger
# from common.logger import set_logger

'''
input : X, y
output : X_train, X_test, y_train, y_test
함수설명 : 테스트 셋 없이 X, y만 넣은경우 train test split 해준다. 원하는 경로에 현재 시간으로 저장도 해준다
'''

# ========== param ============
split_data_save_path = '/home/nextlab/projects/athena-runner-algo-test/research/VQA/dataset/'
train_test_ratio = 0.2
# ========== param ============


def split_dataset(X, y, save_option):
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=train_test_ratio, random_state=1)
    if X_train.shape[1] > 4000:
        print('feature 4000이 초과하였습니다')
        return

    if save_option == True : 
        # X_train, X_test 를 오늘날짜로 폴더에 저장 -> 시 분 초 까지 되도록 구체화
        path = split_data_save_path
        # os.makedirs(path+f'/{str(datetime.today())[:10]}', exist_ok=True)
        # path = path + str(datetime.today())[:10]
        os.makedirs(path + f'{datetime.now().strftime("%Y-%m-%d_%I %M-%S_%p")}')
        path += datetime.now().strftime("%Y-%m-%d_%I %M-%S_%p")
        print(f'dataset save path : {path}')

        for idx, data in enumerate([X_train, X_test]):
            if idx == 0:
                name = 'X_train'
            else:
                name = 'X_test'
            with open(f'/{path}/{name}.csv', 'w') as FOUT:
                np.savetxt(FOUT, data)
            
    print(f'학습 데이터 수 : {len(X_train)}개, 테스트 데이터 수 : {len(X_test)}개')
    print('=====================================')

    # return values
    return X_train, X_test, y_train, y_test

# 이거 저장 데이터프레임으로 해야할듯?