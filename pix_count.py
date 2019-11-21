# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:57:10 2017

@author: Evan RAs
"""

import scipy
import numpy as np

impath = 'C:\\Python27\\images\\'
n_pairs = 181
tally = range(1,n_pairs)
tally = np.repeat(tally,2)
pix_count_a = np.zeros((n_pairs,1))
pix_count_b = np.zeros((n_pairs,1))
ima = np.zeros((450,450,3))
imb = np.zeros((450,450,3))

for i in tally:

    ima = scipy.misc.imread(impath + str(i) + 'a.tif')
    imb = scipy.misc.imread(impath + str(i) + 'b.tif')


    for j in range(1,len(ima)):
        for k in range(1,len(ima)):
            if sum(ima[j,k,:]) < 765:
                pix_count_a[i] = pix_count_a[i]+1
            if sum(imb[j,k,:]) < 765:
                pix_count_b[i] = pix_count_b[i]+1
    
    print(str(i) + ' DONE')