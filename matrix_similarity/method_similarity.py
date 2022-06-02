'''
https://machinelearningmastery.com/distance-measures-for-machine-learning/
'''
import numpy as np
import scipy.io
from sklearn.impute import SimpleImputer
from math import sqrt

def euclidean_distance(a, b):
    return sqrt(sum((e1-e2)**2 for e1, e2 in zip(a,b)))

def hamming_distance(a, b):
    return sum(abs(e1 - e2) for e1, e2 in zip(a, b)) / len(a)

def manhattan_distance(a, b):
    return sum(abs(e1-e2) for e1, e2 in zip(a,b))

# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b)))

# def pearson_similarity(a, b):
#     return np.dot((a - np.mean(a)), (b - np.mean(b))) / ((np.linalg.norm(a - np.mean(a))) * (np.linalg.norm(b - np.mean(b))))


