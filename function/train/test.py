from sklearn.metrics import mean_squared_error, r2_score
import warnings
import scipy 
warnings.filterwarnings("ignore")


'''
input : X_test, y_test, grid, scaler
output : 회귀지표들
함수설명 : train.py로 부터 grid와 scaler을 받아서 테스트셋을 학습한뒤 성능에 대한 지표를 dictionary형태로 반환한다
'''


def test(X_test, y_test, grid, scaler):
    
    X_test = scaler.transform(X_test)
    #X_test = feature_selection.transform(X_test)
    y_test_pred = grid.predict(X_test)
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