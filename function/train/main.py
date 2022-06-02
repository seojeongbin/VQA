import sys
import numpy as np
import pickle
import warnings
import joblib
# ============= import user generated def =============
from make_npy_json_df import make_df_npy_json
from load_data_from_csv import load_data_from_csv
from split_dataset import split_dataset
from train import train
from test import test
from reduct_dimemsion import reduct_dimension_PCA, reduct_dimension_kPCA, reduct_dimension_LLE
from blending import blending
# ===================================================== 
warnings.filterwarnings("ignore")
# set_logger('main_logger').setLevel(50)  # 20이 default, 50은 심각한 문제인경우에만 뜬다..


if __name__ == "__main__":

    # sys.stdout = open('학습결과배치파일예약.txt', 'w')

    '''
    npy_dir = '/mnt/data/VQA/feature/all_channels_with_json_2/' # rapique extracted feature 들이 있는 디렉토리
    df = make_df_npy_json(npy_dir)
    feat, mos = load_data_from_csv(df, True) # True : df에서 load 후 저장까지 한다
    '''

    
    savepath = '/home/nextlab/projects/athena-runner-algo-test/research/VQA/function/research/temp_save/'
    feat = np.load(savepath + 'saved_feat.npy')
    open_file = open(savepath + 'saved_mos.pkl', "rb")
    mos = pickle.load(open_file)
    open_file.close()
    
    X_train, X_test, y_train, y_test = split_dataset(feat, mos, False) # 여기에 pca 항목을 추가해서 넣어야할듯
    regressor, scaler = train(X_train, y_train, iterations=300, model_name='svr', saveoption=False) # ★★저장코드 고쳐야 함 !! # lasso, ridge
    indicator_dict = test(X_test, y_test, regressor, scaler)
    
    ''' 
    <blending regressor : train, test 두줄 대신 한줄로 변경> 
    indicator_dict = blending(X_train, X_test, y_train, y_test) # blending 사용할 경우 바로 이렇게 인자주면된다
    '''
    
    print(indicator_dict)

    # sys.stdout.close()
