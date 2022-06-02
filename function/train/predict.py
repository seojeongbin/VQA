from algorithm.vqa.rapique.feature.rapique_features_videopath import calc_rapique_features_videopath as calc_rapique_features
import time 
import numpy as np

'''
input : video sample (path), regressor, scaler
output : predicted score
함수설명 : 평가하고자 하는 비디오 샘플 1개의 경로를 입력하면 피쳐를 뽑아서 regressor, scaler로 예상 점수를 반환한다
'''


def predict(video_path, regressor, scaler):
    

    X = calc_rapique_features(video_path)
    X = np.nan_to_num(X, copy=False)
    X = X.reshape(1, -1)
    X = scaler.transform(X)
    y = round(regressor.predict(X)[0], 4)
    print(f'* 해당 비디오의 예측 점수 : {y}')
    print('=====================================')
    return y