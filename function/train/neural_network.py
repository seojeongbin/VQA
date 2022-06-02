from sklearn.model_selection import train_test_split
from tensorflow import keras
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import sys
import scipy

### ==========param ============ ###
# build params
input_num = 3884
layer_num1 = 1024
layer_num2 = 512
layer_num3 = 64
dropout_rate = 0.8 # 드롭아웃만 달아도 확실히 오버피팅은 해결됨
### ==========param ============ ###


def train_valid_test_split(X_train_full, y_train_full, X_test_full, y_test_full):

    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_full, y_train_full)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test_full)

    return X_train, X_valid, y_train, y_valid, X_test, y_test_full


def model_build():

    model = keras.Sequential([
        keras.layers.Dense(layer_num1, activation='relu', input_shape=(
            input_num,), name='hidden_1'),  # 3884, : 튜플이여야 하는듯
        keras.layers.Dense(layer_num2, activation='relu', name='hidden_2'),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(layer_num3, activation='relu', name='hidden_3'),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(1, activation='sigmoid', name='output')
    ])
    # build 방식 wide & deep 방식도 시도해보기 (책 384p)

    model.summary()

    return model


### ==========param ============ ###
# fit params
loss_function = 'mean_squared_error'
lr = 0.0001
epochs_num = 40
### ==========param ============ ###


def complie_and_fit(model, X_train, y_train, X_valid, y_valid, save_option=True):

    y_train, y_valid = np.array(
        [x/5.0 for x in y_train]),  np.array([x/5.0 for x in y_valid]) # 시그모이드는 0~1사이로 반환하므로

    model.compile(optimizer=keras.optimizers.Adam(
        learning_rate=lr), loss=loss_function)
    model.fit(X_train, y_train, epochs=epochs_num,
              validation_data=(X_valid, y_valid))

    if save_option == True:
        model.save('saved_model.h5')

    return model


def test(model, X_test, y_test):

    y_test = np.array([x/5.0 for x in y_test]) 

    evaluate_score = model.evaluate(X_test, y_test)
    y_pred = model.predict(X_test)
    # y_pred = list(x for x in y_pred)

    # print(f'y_test 10개 : {y_test[:10]}')
    # print(f'y_pred 10개 : {y_pred[:10]}')
    # print('=====================================')

    rmse = (mean_squared_error(y_test*5, y_pred*5)) ** (0.5)  # 다시 스케일 복원
    r_square = r2_score(y_test*5, y_pred*5)
    # y_test = y_test.reshape(-1,1)
    # print(y_test.shape)
    # print(y_pred.shape) 
    # # 둘다 하나의 리스트로 넣어야할듯
    # print(y_test[:10])
    # print(y_pred[:10])
    
    # plcc = scipy.stats.pearsonr(y_test, y_pred)[0]
    # srcc = scipy.stats.spearmanr(y_test, y_pred)[0]

    indicator_list = ['model.evaluate', 'RMSE', 'R_suare']
    # indicator_list = ['model.evaluate', 'RMSE', 'R_suare', 'PLCC', 'SRCC']
    result_dict = {}

    for idx, indicator in enumerate([evaluate_score, rmse, r_square]):
        indicator = round(indicator, 4)
        result_dict[f'{indicator_list[idx]}'] = indicator

    print('=====================================')

    return result_dict
