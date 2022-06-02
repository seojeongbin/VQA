from research.about_model.npy_concat import npy_concat
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt
import sys
import numpy as np
from sklearn.manifold import TSNE

pca = PCA(n_components=3)
channels = [11,13,15,17]
pca_columns=['pca_component_1','pca_component_2','pca_component_3']
# irisDF_pca = pd.DataFrame(columns=pca_columns)
df = pd.DataFrame(columns=[])

for channel in channels:

    feat_dir = f'/mnt/data/VQA/feature_method_changed/vqa_channel_{channel}/'
    feat, _ = npy_concat(feat_dir)
    # print(f'최초 shape : {feat.shape}')
    feat_scaled = StandardScaler().fit_transform(feat)
    pca.fit(feat_scaled)
    feat_pca = pca.transform(feat_scaled)
    # print(f'pca 이후 shape : {feat_pca.shape}')
    globals()['featDF_pca_{}'.format(channel)] = pd.DataFrame(feat_pca, columns=pca_columns)
    globals()['featDF_pca_{}'.format(channel)]['channel'] = channel


df = pd.concat([featDF_pca_11, featDF_pca_13, featDF_pca_15, featDF_pca_17], axis =0)

#setosa를 세모, versicolor를 네모, virginica를 동그라미로 표시
markers=['^', 's', 'o', 'v']
# #pca_component_1 을 x축, pc_component_2를 y축으로 scatter plot 수행. 
# for channel, marker in zip(channels, markers):
#     x_axis_data = df[df['channel']==channel]['pca_component_1']
#     y_axis_data = df[df['channel']==channel]['pca_component_2']
#     plt.scatter(x_axis_data, y_axis_data, marker=marker)
# plt.legend()
# plt.xlabel('pca_component_1')
# plt.ylabel('pca_component_2')
np.random.seed(19680801)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for channel, marker in zip(channels, markers):
    x_axis_data = df[df['channel']==channel]['pca_component_1']
    y_axis_data = df[df['channel']==channel]['pca_component_2']
    z_axis_data = df[df['channel']==channel]['pca_component_3']
    ax.scatter(x_axis_data, y_axis_data, z_axis_data, marker = marker)

plt.show()
plt.savefig('/home/nextlab/projects/athena-runner-algo-test/research/' +
            'pca_plot_3d.png')
plt.clf()
print('저장 완료')