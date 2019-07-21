#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:51:57 2019
@author: shangranq
"""

import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import matplotlib.pyplot as plt
from numpy import random

def load_txt(txt_dir, txt_name):
    List = []
    with open(txt_dir + txt_name, 'r') as f:
        for line in f:
            List.append(line.strip('\n').replace('.nii', '.npy'))
    return List

def padding(tensor, win_size=23):
    A = np.ones((tensor.shape[0]+2*win_size, tensor.shape[1]+2*win_size, tensor.shape[2]+2*win_size)) * tensor[-1,-1,-1]
    A[win_size:win_size+tensor.shape[0], win_size:win_size+tensor.shape[1], win_size:win_size+tensor.shape[2]] = tensor
    return A.astype(np.float32)

def get_confusion_matrix(preds, labels):
    labels = labels.data.cpu().numpy()
    preds = preds.data.cpu().numpy()
    matrix = [[0, 0], [0, 0]]
    for index, pred in enumerate(preds):
        if np.amax(pred) == pred[0]:
            if labels[index] == 0:
                matrix[0][0] += 1
            if labels[index] == 1:
                matrix[0][1] += 1
        elif np.amax(pred) == pred[1]:
            if labels[index] == 0:
                matrix[1][0] += 1
            if labels[index] == 1:
                matrix[1][1] += 1
    return matrix

def matrix_sum(A, B): 
    return [[A[0][0]+B[0][0], A[0][1]+B[0][1]],
            [A[1][0]+B[1][0], A[1][1]+B[1][1]]]

def get_accu(matrix):
    return float(matrix[0][0] + matrix[1][1])/ float(sum(matrix[0]) + sum(matrix[1]))

def get_MCC(matrix):
    TP, TN, FP, FN = float(matrix[0][0]), float(matrix[1][1]), float(matrix[0][1]), float(matrix[1][0])
    upper = TP * TN - FP * FN
    lower = (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)
    return upper / (lower**0.5 + 0.000000001)
    
def softmax(x1, x2):
    return np.exp(x2) / (np.exp(x1) + np.exp(x2))

def get_AD_risk(raw):
    raw = raw[0, :, :, :, :].cpu()
    a, x, y, z = raw.shape
    risk = np.zeros((x, y, z))
    for i in range(x):
        for j in range(y):
            for k in range(z):
                risk[i, j, k] = softmax(raw[0, i, j, k], raw[1, i, j, k])
    return risk


