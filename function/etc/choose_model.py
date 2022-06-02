from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
import numpy as np
from sklearn.utils import shuffle
from research.about_model.functions import make_2000, preprocess_y
import pandas as pd
import time
from sklearn.svm import SVR

start = time.time()
prior_time = start

Model = []
RMSE = []
R_sq = []
Time = []
cv = KFold(5, random_state = 1, shuffle=True)

def input_scores(name, model, x, y):
    global prior_time
    Model.append(name)
    RMSE.append(np.sqrt((-1) * cross_val_score(model, x, y, cv=cv, 
                                               scoring='neg_mean_squared_error').mean()))
    R_sq.append(cross_val_score(model, x, y, cv=cv, scoring='r2').mean())
    run_time = time.time() - prior_time
    Time.append(run_time)
    prior_time = time.time()

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor, 
                              AdaBoostRegressor)
import xgboost
import lightgbm
import catboost

# names = ['Linear Regression', 'Ridge Regression', 'Lasso Regression',
#          'K Neighbors Regressor', 'Decision Tree Regressor', 
#          'Random Forest Regressor', 'Gradient Boosting Regressor',
#          'Adaboost Regressor', 'Xgboost Regressor', 'Lightgbm Regressor']
# models = [LinearRegression(), Ridge(), Lasso(),
#           KNeighborsRegressor(), DecisionTreeRegressor(),
#           RandomForestRegressor(), GradientBoostingRegressor(), 
#           AdaBoostRegressor(), xgboost.XGBRegressor(), lightgbm.LGBMRegressor()]

names = ['Xgboost Regressor', 'Lightgbm Regressor']
models = [xgboost.XGBRegressor(), lightgbm.LGBMRegressor()]

df, feat = make_2000()
df = preprocess_y(df)


for name, model in zip(names, models):
    input_scores(name, model, feat, df)

evaluation = pd.DataFrame({'Model': Model,
                           'RMSE': RMSE,
                           'R Squared': R_sq,
                           'Running Time(초)' : Time})

print("FOLLOWING ARE THE TRAINING SCORES: ")
print(evaluation)
evaluation.to_csv('result_compare_model.csv', mode='w')
print(f'총 소요시간 : {time.time() - start}초')

# 필요없는거 줄이고 svr, catboost 추가하기