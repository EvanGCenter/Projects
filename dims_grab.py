# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:57:10 2017

@author: Evan RAs
"""

import scipy
import numpy as np

impath = 'C:\\Python27\\Images\\lamem\\'
n_pairs = 361
tally = range(1,n_pairs)
tally = np.repeat(tally,2)
pix_count_a = np.zeros((n_pairs,1))
pix_count_b = np.zeros((n_pairs,1))
dimsa = np.zeros((n_pairs,2))
dimsb = np.zeros((n_pairs,2))
areaa = np.zeros((n_pairs,1))
areab = np.zeros((n_pairs,1))

for i in tally:

    ima = scipy.misc.imread(impath + str(i) + 'a.jpg')
    imb = scipy.misc.imread(impath + str(i) + 'b.jpg')

    tempa = ima.shape
    dimsa[i,:] = tempa[0:2]
    areaa[i] = np.multiply(tempa[0],tempa[1])
    tempb = imb.shape
    dimsb[i,:] = tempb[0:2]
    areab[i] = np.multiply(tempb[0],tempb[1])
    
    print(str(i) + ' DONE')