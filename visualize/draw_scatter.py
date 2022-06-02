import glob
from sklearn.linear_model import LinearRegression  # 통계분석(상관계수) 위함
from matplotlib import pyplot as plt
import numpy as np
import statistics
import pandas as pd
import sys
import seaborn as sns
from sklearn.metrics import mean_squared_error


def draw_scatter(df, name) :

    ax = sns.relplot(x="pred", y="mos", data=df)

    # 상관계수 구하기 (선형성 얼마나 갖는지 수치화 하기 위해)
    pred = np.array(df.loc[:, 'pred']).reshape((-1, 1))
    actual = np.array(df.loc[:, 'mos']).reshape((-1, 1))

    model = LinearRegression()
    model.fit(pred, actual)
    r_square = model.score(pred, actual)
    mse = mean_squared_error(pred, actual)

    print(f'r square : {r_square} \t mse : {mse}')

    ax.fig.suptitle(f"r_square : {r_square}, mse : {mse}",
                    fontsize=16, fontdict={"weight": "bold"})
    # ax.set(xlim=(0, 5))
    # ax.set(ylim=(0, 5))

    plt.show()
    plt.savefig('/home/nextlab/projects/athena-runner-algo-test/research/result_scatter/' + f'{name}.png')
    print('scatter 저장완료')


