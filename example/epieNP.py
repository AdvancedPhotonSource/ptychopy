import ptychopy
# import matplotlib.pyplot as plt
import time
import numpy as np
# from matplotlib import animation
import h5py
import scipy.ndimage

scanNo = 152
data_dir = '/data2/JunjingData/mlhcode/scan' + '%03d' %  (scanNo) + 'test/'
result_dir = '/data2/JunjingData/mlhcode/results/scan' + '%03d' %  (scanNo) + '/'
det_Npixel = 256
cen_x = 616; cen_y = 276
N_dp_x_input = det_Npixel
N_dp_y_input = det_Npixel
index_x_lb = (cen_x - np.floor(N_dp_x_input / 2.0)).astype(np.int)
index_x_ub = (cen_x + np.ceil(N_dp_x_input / 2.0)).astype(np.int)
index_y_lb = (cen_y - np.floor(N_dp_y_input / 2.0)).astype(np.int)
index_y_ub = (cen_y + np.ceil(N_dp_y_input / 2.0)).astype(np.int)
N_scan_y_lb = 0
N_scan_x_lb = 0
# N_scan_y = 20
# N_scan_x = 20
# dimension
N_scan_y = 51
N_scan_x = 51
filePath = 'entry/data/data'
# roi = '_example10251'
# N_scan_y = 102
# N_scan_x = 51
resampleFactor = 1
resizeFactor = 1
fileName = data_dir + 'scan' + '%03d' % (scanNo) + '_data_' + '%06d' % (1) + '.h5'
h5_data = h5py.File(fileName, 'r')
dp_temp = h5_data[filePath][()];
# dp = np.zeros((N_scan_y * N_scan_x, dp_temp.shape[1], dp_temp.shape[2]))
dp = np.zeros((N_scan_y*N_scan_x,int(N_dp_y_input*resizeFactor),int(N_dp_x_input*resizeFactor)))
print(dp.shape)
for i in range(N_scan_y):
    fileName = data_dir + 'scan' + '%03d' % (scanNo) + '_data_' + '%06d' % (i + 1 + N_scan_y_lb) + '.h5'
    h5_data = h5py.File(fileName, 'r')
    dp_temp = h5_data[filePath][()];
    for j in range(N_scan_x):
        index = i * N_scan_x + j
        # dp[index]=dp_temp[j][:][:]
        scipy.ndimage.interpolation.zoom(dp_temp[j+N_scan_x_lb, \
                                         index_y_lb:index_y_ub, \
                                         index_x_lb:index_x_ub],\
                                         [resizeFactor,resizeFactor],\
                                         dp[index,:,:], 1)
dp[dp < 0] = 0
dp[dp > 1e7] = 0

#Whole mode key work, with numpy array as input objectNP=l4,      positionNP=l2,   objectNP=l2, probeNP=l4,
ptychopy.epienp(jobID="ePIEIOTestr256", diffractionNP=dp,\
                beamSize=110e-6, qx=276, qy=616, scanDimsx=51, scanDimsy=51, stepx=100e-9, \
                stepy=100e-9, lambd=1.408911284090909e-10, iter=10, size=256, dx_d=75e-6, z=1.92,\
                probeModes=1)








