import matplotlib.pyplot as plt
import pandas as pd
import sys
import seaborn as sns

df = pd.read_csv('/home/nextlab/projects/athena-runner-algo-test/research/multiprocess_result/csv/result.csv') 

# pred_list = df['predict_score'].to_list()
video_num = 5
section_num = 6

for video_idx in range(video_num) : 
    pred_list = (df.loc[df["video_num"]==video_idx + 1, "predict_score"]).to_list()
    line_chart = plt.plot(range(1,section_num+1), pred_list)
    #df = df.loc[df["video_num"]==video_idx + 1, :]
    #sns.scatterplot(data=df, x=df['section'].to_list(),y=df['ground_truth'].to_list())

text_x_loc = 3.2
text_y_loc = 3.5
average_run_time = df['video_runtime'].mean()
plt.text(text_x_loc, text_y_loc, 'fps : 60, length : 60sec, section : 10sec')
plt.text(text_x_loc, text_y_loc-0.125, f'average runtime : {round(average_run_time,2)}sec')
plt.title('Prediction Scores For Each Video Section')
plt.xlabel('Cluster (section)')
plt.ylabel('Mos_Pred')
plt.grid(True, axis = 'x')
plt.show() 
save_path = '/home/nextlab/projects/athena-runner-algo-test/research/multiprocess_result/plot/'
plt.savefig( save_path+ 'test_lineplot.png')

sys.exit()


sales1 = [1, 5, 8, 9, 7, 11, 8, 12, 14, 9, 5] # 걍 mos 점수 목록들을 list로 넣으면됨
sales2 = [3, 7, 9, 6, 4, 5, 14, 7, 6, 16, 12]
line_chart1 = plt.plot(range(1,12), sales1) # cluster에 맞게 range 조절
line_chart2 = plt.plot(range(1,12), sales2)
plt.title('Prediction score for each video section')
plt.xlabel('Cluster')
plt.ylabel('Mos_Pred')
plt.grid(True, axis = 'x')
plt.legend(['year 2016', 'year 2017'], loc=4)
plt.show()
save_path = '/home/nextlab/projects/athena-runner-algo-test/research/multiprocess_result/plot/'
plt.savefig( save_path+ 'test_lineplot.png')

'''
1. ground_truth 넣기 : https://pythonguides.com/put-legend-outside-plot-matplotlib/ <- Label ground_truth로 통일표기 -> macro block이 균등하게 나오는게 아니라 ground truth 비교하는거 아님!
2. 눈금넣기 : plt.grid(True, axis = 'x')
3. 각종 정보기입
'''