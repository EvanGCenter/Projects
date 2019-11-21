# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:48:35 2017

@author: Evan
"""

import os
import shutil

impath_g = 'C:\\Python27\\scenes\\good_FN\\'       #directory where images can be found
impath_b = 'C:\\Python27\\scenes\\bad_FN\\'
destpath_g = 'C:\\Python27\\scenes\\good\\'
destpath_b = 'C:\\Python27\\scenes\\bad\\'
oldnames_g = os.listdir(impath_g)
oldnames_b = os.listdir(impath_b)
suff_g = 'a.jpg'
suff_b = 'b.jpg'


n_files = range(0, len(oldnames_g))

for i in n_files:
    
    shutil.move(impath_g + oldnames_g[i], destpath_g + str(i+1) + suff_g)
    shutil.move(impath_b + oldnames_b[i], destpath_b + str(i+1) + suff_b)        