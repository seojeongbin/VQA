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
from sklearn.metrics import mean_squared_error, r2_score
import warnings
import scipy 


'''
사용할모델 종류 : svr, lgbm, xgb, lasso
변경사항 : 랜덤서치 최적 값을 받아오거나 최적 모델을 알아서 받아올 수 있도록 & 일일이 이걸 학습시킬 수 없으므로 필히 저장하고 갖고오는 식으로 해야함!!
'''

svr = SVR(C = 16, gamma = 0.0078125)
lgbm = lgb.LGBMRegressor(n_estimators = 8000,
    learning_rate = 0.05,
    colsample_bytree= 0.3,
    subsample= 0.7,
    scale_pos_weight = 1.5,
    boosting = 'dart',
    metric = 'rmse')
xgb = xgb.XGBRegressor(learning_rate = 0.05, subsample = 0.7)
alpha = 0.0033000000000000004
lasso = LassoCV(alphas = [alpha * .6, alpha * .65, alpha * .7, alpha * .75, alpha * .8, 
                          alpha * .85, alpha * .9, alpha * .95, alpha, alpha * 1.05, 
                          alpha * 1.1, alpha * 1.15, alpha * 1.25, alpha * 1.3, alpha * 1.35, 
                          alpha * 1.4], 
                max_iter = 50000, cv = 10, n_jobs=-1)




def blending(X_train, X_test, y_train, y_test) :

    scaler = preprocessing.MinMaxScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    svr_model = svr.fit(X_train, y_train)
    print('svr 학습완료')
    xgb_model = xgb.fit(X_train, y_train)
    print('xgb 학습완료')
    lgbm_model = lgbm.fit(X_train, y_train)
    print('lgbm 학습완료')
    lasso_model = lasso.fit(X_train, y_train)
    print('lasso 학습완료') # 얘네 한번 학습한뒤에는 저장하고 로드하는식으로 관리해야할듯함.

    y_test_pred = 0.55* svr_model.predict(X_test) + 0.25 * lgbm_model.predict(X_test) + 0.1 *xgb_model.predict(X_test)
    + 0.1*lasso_model.predict(X_test)

    print(f'y_test : {y_test[:10]}')
    print(f'y_test_pred : {y_test_pred[:10]}')

    rmse = (mean_squared_error(y_test, y_test_pred))**0.5
    r_square = r2_score(y_test, y_test_pred)
    plcc = scipy.stats.pearsonr(y_test, y_test_pred)[0]
    srcc = scipy.stats.spearmanr(y_test, y_test_pred)[0]

    indicator_list = ['RMSE', 'R_suare', 'PLCC', 'SRCC']
    result_dict = {}

    for idx, indicator in enumerate([rmse, r_square, plcc, srcc]) :
        indicator = round(indicator, 4)
        result_dict[f'{indicator_list[idx]}'] = indicator # 'mse' : mse값
    
    print('=====================================')
    return result_dict
