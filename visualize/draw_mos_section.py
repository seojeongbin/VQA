# reference : https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html

from turtle import width
from matplotlib.ft2font import BOLD
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''
추가해야하는 사항 => ★★★ 1. line plot 으로 변경한다 2. 비디오별 표시는 서로 다른색으로 나타낸다 3. ground truth 점수를 같이 표기하거나 오차를 나타낸다 ★★★
1. 함수 불러와서 main 함수에서 같이 실행되도록 조치
2. 비디오별 소요시간 기입
3. (완료) 각 비디오 길이, 내부 섹션 길이, 6개 총 분석 소요시간 기입
'''

category_names = ['Section_1','Section_2','Section_3','Section_4','Section_5']
# results = {
#     'Video_1': [10, 15, 17, 32, 26],
#     'Video_2': [26, 22, 29, 10, 13],
#     'Video_3': [35, 37, 7, 2, 19],
#     'Video_4': [32, 11, 9, 15, 33],
#     'Video_5': [21, 29, 5, 5, 40],
#     'Video_6': [8, 19, 5, 30, 38]
# }

df = pd.read_csv(
    '/home/nextlab/projects/athena-runner-algo-test/research/multiprocess_result/csv/result.csv')
results = {}
running_time = {}

video_num = 6
section_num = 5
for j in range(video_num) :
    result_list = []
    for i in range(section_num) :
        result = df.loc[(df['video_num'] == j+1) & (
            df['section'] == i+1), 'predict_score']
        result = result.iloc[0]
        result_list.append(result)
    results[f'video_{j+1}'] = result_list
    time = df.loc[(df['video_num'] == j+1), 'time']
    time = time.iloc[0]
    running_time[f'video_{j+1}'] = time
# print(running_time)




def survey(results, category_names):

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.1, 1),
              loc='lower left', fontsize='small')

    return fig, ax


survey(results, category_names)



length = 10
section_length = 2
total_time = 114.8188
for i in range(video_num):
    x = 10
    y = 5 - i
    plt.text(x, y, running_time[f'video_{i+1}'])
plt.title(f'Each information -> video length : {length}sec, section : {section_length}sec, total_running_time = {total_time}sec', y=-0.1)
plt.show()
save_path = '/home/nextlab/projects/athena-runner-algo-test/research/multiprocess_result/plot/'
plt.savefig( save_path+ 'test.png')