# from algorithm.vqa.rapique.feature.rapique_features_videopath import calc_rapique_features_videopath as calc_rapique_features
from sklearn.model_selection import GridSearchCV, train_test_split, RandomizedSearchCV
import warnings
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn import preprocessing
import time
import sys
from datetime import datetime
import os
import lightgbm as lgb
import xgboost as xgb
import warnings
import numpy as np
import sys
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV, ElasticNet
from sklearn.ensemble import StackingRegressor

# from sklearn.neighbors import LocalOutlierFactor
# from sklearn.covariance import EllipticEnvelope # 이거 아웃라이어 탐지하는건데 너무 오래걸림 빼는게 나을듯? 확실한 성능을 보장해주는게 아니라면...
# from sklearn.feature_selection import SelectKBest, mutual_info_regression, f_regression # 안하는게 나음





'''
input : X_train, y_train, iterations, saveoption
output : grid(regressor), scaler
함수설명 : train 셋을 넣으면 파라미터 튜닝을 진행하여 최적의 regressor와 scaler를 반환한다, saveoption에 따라 모델을 저장할 수 도 있다
'''

'''
현재까지 최고 : best params : {'subsample': 0.7, 'scale_pos_weight': 1.7, 'n_estimators': 2000, 'metric': 'rmse', 'learning_rate': 0.05, 'colsample_bytree': 0.5, 'boosting': 'dart'}
{'RMSE': 1.1059, 'R_suare': 0.3802, 'PLCC': 0.6395, 'SRCC': 0.6331}
'''
# ========== param ============
# param_grid_lgbm = {  # 밑에서 iteration 바꿀것! & 나중에 범위별로 멀티프로세스 적용해보기..
#     'n_estimators': [2000,4000,6000,8000],
#     # 'max_bin' : [500],
#     'learning_rate': [0.05],
#     # 'max_depth': [15], # 이거 생각없이 막 늘리면 메모리 에러나서 kill 됨. 주의. 
#     # 'num_leaves' : [2**15-1],
#     'colsample_bytree': [0.3,0.5,0.7,0.9],
#     'subsample': [0.7,0.8,0.9],
#     'scale_pos_weight' : [1.5,1.7,1.9],
#     'boosting' : ['dart'],
#     'metric' : ['rmse']
# }
param_grid_lgbm = {  # 밑에서 iteration 바꿀것! & 나중에 범위별로 멀티프로세스 적용해보기..
    'n_estimators': [8000],
    # 'max_bin' : [500],
    'learning_rate': [0.05],
    # 'max_depth': [15], # 이거 생각없이 막 늘리면 메모리 에러나서 kill 됨. 주의. 
    # 'num_leaves' : [2**15-1],
    'colsample_bytree': [0.3],
    'subsample': [0.7],
    'scale_pos_weight' : [1.5],
    'boosting' : ['dart'],
    'metric' : ['rmse']
}
param_grid_svr = {'C': np.logspace(1, 10, 10, base=2),
                'gamma': np.logspace(-8, 1, 10, base=2)}
# param_grid_svr = {'C': [16.0], 'gamma' : [0.00390625]}
param_grid_xgb = {'learning_rate' : [0.05], 'subsample' : [0.7]}
param_grid_rfr = {}
param_grid_lasso = {'max_iter' : [50000], 'cv' : [10], 'n_jobs': [-1]}
param_grid_ridge = {}
param_grid_elasticnet = {'alpha' : [0.1], 'l1_ratio' : [0.5]}
path = '/home/nextlab/projects/athena-runner-algo-test/research/VQA/pkl'
# ========== param ============



# reference about lgbm : https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html , http://machinelearningkorea.com/2019/09/29/lightgbm-%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0/
def train(X_train, y_train, model_name, iterations, saveoption=True):

    start = time.time()

    
    if model_name == 'lgbm' :
        grid = RandomizedSearchCV(lgb.LGBMRegressor(), param_grid_lgbm, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
        # grid = GridSearchCV(lgb.LGBMRegressor(), param_grid_lgbm, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'svr' :
        grid = RandomizedSearchCV(SVR(), param_grid_svr, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'xgb' :
        grid = RandomizedSearchCV(xgb.XGBRegressor(), param_grid_xgb, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'rfr' :
        grid = RandomizedSearchCV(RandomForestRegressor(), param_grid_rfr, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'lasso' :
        alpha = 0.0033000000000000004
        lasso = LassoCV(alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, 
                                alpha * .85, alpha * .9, alpha * .95, alpha, alpha * 1.05, 
                                alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, alpha * 1.35, 
                                alpha * 1.4])
        grid = RandomizedSearchCV(lasso, param_grid_lasso, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'ridge' :
        alpha = 0.6
        ridge = RidgeCV(alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, alpha * .85, 
                                alpha * .9, alpha * .95, alpha, alpha * 1.05, alpha * 1.1, alpha * 1.15,
                                alpha * 1.25, alpha * 1.3, alpha * 1.35, alpha * 1.4], cv = 10)
        grid = RandomizedSearchCV(ridge, param_grid_ridge, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)
    elif model_name == 'elasticnet' :
        grid = RandomizedSearchCV(ElasticNet(), param_grid_elasticnet, random_state=42, cv=3, n_iter=iterations, scoring='neg_mean_squared_error', n_jobs=-1, verbose=10)

    scaler = preprocessing.MinMaxScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    
    grid.fit(X_train, y_train)

    print(f'best params : {grid.best_params_}')
    rmse = ((-1) * grid.best_score_)**0.5
    print(f'* 검증 지표 (RMSE : {round(rmse,4)})')

    if saveoption == True:

        os.makedirs(path + f'/{datetime.now().strftime("%Y-%m-%d_%I %M-%S_%p")}')
        path = path + '/'+datetime.now().strftime("%Y-%m-%d_%I %M-%S_%p")
        joblib.dump(grid, f'{path}/regressor(grid).pkl')
        joblib.dump(scaler, f'{path}/scaler(grid).pkl')
        print('regressor, scaler 저장완료')

    spend_time = round((time.time() - start) / 60,4) # sec -> min

    print(f'모델 종류 : {model_name}, 파라미터 튜닝 iterations : {iterations}, 저장 여부 : {saveoption} => 훈련 총 소요시간 : {spend_time}분')
    print('======================================================')
    
    return grid, scaler #, feature_selection  # ★★ grid.fit하면 그게 바로 최적화된 모델을 바로 fit하는 방법임 이거 말고 기존대로 하면 에러난다


    