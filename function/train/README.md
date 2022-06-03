### blending.py
- regressor 성능을 고도화 하고자 개별 모델을 blend하여 높은 성능을 갖는 혼합된 모델을 만드는 코드 입니다

### channel_test_data.py
- 현재는 전체 채널 (100개)를 모두 사용합니다만 특정 채널만을 이용해 학습 및 점수를 도출하고 싶은경우 사용합니다

### extract_features.py
- 입력한 비디오 디렉토리의 영상들을 chunk size만큼 멀티프로세스를 이용해서 영상을 뽑아 저장하고자 하는 경로에 저장합니다
- 프로세스 수를 특정합니다 : multiprocessing.cpu_count()  를 이용합니다

### make_npy_json_df.py
- json, npy 디렉토리를 입력하면 각 비디오 파일명, json 1개 경로, npy 1개 경로를 칼럼으로 데이터프레임을 반환합니다
![image](https://user-images.githubusercontent.com/69031537/171542612-3569c358-6e5d-48a4-8622-db574591b8fe.png)

### npy_concat.py
- npy파일들이 있는 디렉토리를 입력하면 개별 np.load하여 문제있는 파일은 제외 후 concat 한 matrix를 반환합니다

### load_data_from_csv.py
- 위의 두 py 파일을 import 
- dataframe을 입력받아서 train에 넣을 데이터셋 (X : feat, y : mos)를 반환
  - mos는 json에서 읽은 meta정보를 내부 알고리즘을 통해 점수로 변환 (range : 0 ~5)

### reduct_dimension.py
- 3884개의 차원을 그대로 모델에 넣는것이 아닌 저차원으로 줄여서 넣기위한 시도가 담긴 파일

### sort_and_rename.py
- video와 json dir을 입력하면 왜곡 세기에 따라 오름차순을 하고 0001 ~ len 만큼 주기 및 이름변경을 합니다

### split dataset.py
- 테스트 셋 없이 X, y만 넣은경우 train test split, 이후 원하는 경로에 현재 시간으로 저장까지 실시합ㄴ디ㅏ

### train.py
- 데이터셋을 입력하면 lightgbm, xgboost 등 학습하여 학습된 모델을 리턴합니다
- RandomgridSearCV를 이용해서 파라미터 튜닝을 동시에 수행합니다

### test.py
- 위에서 학습된 regressor, scaler를 학습받아서 테스트 셋을 평가하여 회귀지표를 반환합니다
- 회귀지표 : indicator_list = ['RMSE', 'R_suare', 'PLCC', 'SRCC']

### neural_network.py
- 그동안은 regressor을 머신러닝 사이킷런 모델을 사용하였지만 신경망을 사용하여 학습 및 테스트하는 과정 입니다
- 오버피팅을 막기위해 드롭아웃을 


