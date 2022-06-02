import scipy.io
import numpy as np
from matplotlib import pyplot as plt


matlab_npy_path = r'G:\공유 드라이브\MOS\glitched_10sec_clean_RAPIQUE_feats.mat'
python_npy_path = r'G:\공유 드라이브\MOS\python_result.npy'


mat = scipy.io.loadmat(matlab_npy_path)
matlab_npy = np.asarray(mat['feats_mat'], dtype=np.float)

python_npy = np.load(python_npy_path)


# matlab_npy = np.nanmean(matlab_npy, axis=0)
# python_npy = np.nanmean(python_npy, axis=0)
# matlab_npy = matlab_npy[0]
# python_npy = python_npy[0]
print(matlab_npy.shape, python_npy.shape)

# for e1, e2 in zip(matlab_npy, python_npy):
#     print(e1, e2)

for mat_ftr, py_ftr in zip(matlab_npy, python_npy):
    print(mat_ftr.shape, py_ftr.shape)
    fig = plt.figure()
    plt.ylim(0, 5)
    plt.scatter(range(mat_ftr.shape[0]), mat_ftr, s=0.1)
    plt.scatter(range(py_ftr.shape[0]), py_ftr, s=0.1)
    plt.show()
    plt.close()
