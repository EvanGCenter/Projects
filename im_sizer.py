# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:27:50 2017

@author: Evan
"""

from PIL import Image

dimension = 2 # 1 for width 2 for height
bw = 550
bh = 450
impath = 'C:\\Python27\\Images\\prac_images_lm\\'
newhome = 'C:\\Python27\\Images\\prac_images_lm_rs\\'
n_pairs = 21
tally = range(1,n_pairs)
asfx = 'a.jpg'                    
bsfx = 'b.jpg'

for i in tally: 
    
    if dimension == 1:
        
        basewidth = bw
        
        img = Image.open(impath + str(i) + asfx)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(newhome + str(i) + asfx, "JPEG")
        
        img = Image.open(impath + str(i) + bsfx)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(newhome + str(i) + bsfx, "JPEG")
    
    elif dimension == 2:    
        
        baseheight = bh
        
        img = Image.open(impath + str(i) + asfx)
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save(newhome + str(i) + asfx, "JPEG")
        
        img = Image.open(impath + str(i) + bsfx)
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save(newhome + str(i) + bsfx, "JPEG")

    print(str(i) + ' DONE')