# regressor 투입 전 3884개의 차원 수를 줄여서 넣어보고자 하였음
import numpy as np
from sklearn.decomposition import PCA, KernelPCA
from sklearn.manifold import LocallyLinearEmbedding as LLE
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def reduct_dimension_PCA(X_train, X_test):

    # 이거 주성분 숫자를 지정하는 것보다 보존하고자 하는 분산비율을 설정하는 것이 훨 낫단다
    pca = PCA(n_components=0.95)
    X_reduced_train = pca.fit_transform(X_train)
    X_reduced_test = pca.transform(X_test)

    print(f'train 차원 수 3884 -> {X_reduced_train.shape[1]}')
    print(f'test 차원 수 3884 -> {X_reduced_test.shape[1]}')
    print('=====================================')

    return X_reduced_train, X_reduced_test


def reduct_dimension_kPCA(X_train, X_test):

    # kPCA는 분산비율로 설정 불가인듯 : kernel_pca = KernelPCA(n_components=0.95, kernel="rbf", gamma=10, fit_inverse_transform=True, alpha=0.1)
    # n 숫자 커널 감마 어떻게 정할지 생각해야함

    Kernel_pca = KernelPCA(n_components=2, kernel='rbf', gamma=0.04) # grid 적용가능 ! 
    X_reduced_train = Kernel_pca.fit_transform(X_train)
    X_reduced_test = Kernel_pca.transform(X_test)

    print(f'train 차원 수 3884 -> {X_reduced_train.shape[1]}') # 77dimens
    print(f'test 차원 수 3884 -> {X_reduced_test.shape[1]}')
    print('=====================================')

    return X_reduced_train, X_reduced_test


def reduct_dimension_LLE(X_train, X_test):

    lle = LLE(n_components=3, n_neighbors=10)
    X_reduced_train = lle.fit_transform(X_train)
    X_reduced_test = lle.transform(X_test)

    print(f'train 차원 수 3884 -> {X_reduced_train.shape[1]}')
    print(f'test 차원 수 3884 -> {X_reduced_test.shape[1]}')
    print('=====================================')

    return X_reduced_train, X_reduced_test