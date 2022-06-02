from research.about_model.npy_concat import npy_concat
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

tSNE = TSNE(n_components=2, learning_rate='auto', init='random')
channels = [11, 13, 15, 17]
tSNE_columns=['tSNE_component_1','tSNE_component_2']
# irisDF_tSNE = pd.DataFrame(columns=tSNE_columns)
df = pd.DataFrame(columns=[])

for channel in channels:

    feat_dir = f'/mnt/data/VQA/feature_method_changed/vqa_channel_{channel}/'
    feat, _ = npy_concat(feat_dir)
    # print(f'최초 shape : {feat.shape}')
    feat_scaled = StandardScaler().fit_transform(feat)
    # tSNE.fit(feat_scaled)
    feat_tSNE = tSNE.fit_transform(feat_scaled)
    # print(f'tSNE 이후 shape : {feat_tSNE.shape}')
    globals()['featDF_tSNE_{}'.format(channel)] = pd.DataFrame(feat_tSNE, columns=tSNE_columns)
    globals()['featDF_tSNE_{}'.format(channel)]['channel'] = channel


df = pd.concat([featDF_tSNE_11, featDF_tSNE_13, featDF_tSNE_15, featDF_tSNE_17], axis =0)

#setosa를 세모, versicolor를 네모, virginica를 동그라미로 표시
markers=['^', 's', 'o', 'v']
#tSNE_component_1 을 x축, pc_component_2를 y축으로 scatter plot 수행. 
for channel, marker in zip(channels, markers):
    x_axis_data = df[df['channel']==channel]['tSNE_component_1']
    y_axis_data = df[df['channel']==channel]['tSNE_component_2']
    plt.scatter(x_axis_data, y_axis_data, marker=marker)
plt.legend()
plt.xlabel('tSNE_component_1')
plt.ylabel('tSNE_component_2')
plt.show()
plt.savefig('/home/nextlab/projects/athena-runner-algo-test/research/' +
            't-SNE_plot.png')
plt.clf()
print('저장 완료')