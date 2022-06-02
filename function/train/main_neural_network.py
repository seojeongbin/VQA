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
from neural_network import *
# import tensorflow as tf
from tensorflow import keras
# =====================================================
warnings.filterwarnings("ignore")
# set_logger('main_logger').setLevel(50)  # 20이 default, 50은 심각한 문제인경우에만 뜬다..


if __name__ == "__main__":

    savepath = '/home/nextlab/projects/athena-runner-algo-test/research/VQA/function/research/temp_save/'
    feat = np.load(savepath + 'saved_feat.npy')
    open_file = open(savepath + 'saved_mos.pkl', "rb")
    mos = pickle.load(open_file)
    open_file.close()

    X_train, X_test, y_train, y_test = split_dataset(feat, mos, False)

    X_train, X_valid, y_train, y_valid, X_test, y_test = train_valid_test_split(
        X_train, y_train, X_test, y_test)

    # model = model_build()
    # model_fitted = complie_and_fit(model, X_train, y_train, X_valid, y_valid)
    model_fitted = keras.models.load_model('/home/nextlab/projects/athena-runner-algo-test/saved_model.h5')
    result_dict = test(model_fitted, X_test, y_test)

    print(result_dict)
