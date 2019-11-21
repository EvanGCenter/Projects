# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 13:02:05 2018

@author: Evan
"""

# start with stuff all the modules will need
import os                           # for file/folder operations
import numpy as np
import numpy.random as rnd          # for random number generators
from psychopy import visual, core, gui, data, event
from psychopy import parallel as p
import pygame

rnd.seed()

p_port = p.PParallelInpOut32(address=0x0378)

n_files = 720

n_good_att = 180
n_bad_att = 180
n_good_dst = 180
n_bad_dst = 180
n_standards_att = 360
n_deviants_att = 360
n_standards_dst = 360
n_deviants_dst = 360

tot_trials = n_good_att+n_bad_att+n_good_dst+n_bad_dst+n_standards_att+n_deviants_att+n_standards_dst+n_deviants_dst
break_time = 60 

datapath = 'C:\\Users\\rift\\Desktop\\Evan\\data\\'      # directory to save data in

N3gPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\good\\'
N3bPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\bad\\'

# list building for local context conditions
N3gList = [os.path.join(N3gPath,f) for f in os.listdir(N3gPath) if not f.startswith('.')]
N3gList = [f for f in N3gList if not f.endswith('361a.jpg')]
N3bList = [os.path.join(N3bPath,f) for f in os.listdir(N3bPath) if not f.startswith('.')]
N3bList = [f for f in N3bList if not f.endswith('361b.jpg')]

# list building for global context conditions
N3gList_ag = list(rnd.choice(N3gList,n_good_att,replace=False))
N3bList_ag = list(rnd.choice(N3bList,n_bad_att,replace=False))    

N3gList_dg = [pic for pic in N3gList if pic not in N3gList_ag]
N3bList_dg = [pic for pic in N3bList if pic not in N3bList_ag]

N3tList_ag = N3gList_ag+N3bList_ag
rnd.shuffle(N3tList_ag)

N3tList_dg = N3gList_dg+N3bList_dg
rnd.shuffle(N3tList_dg)

scrsize = (1280,1024)                 # screen size in pixels
im_time = 12                        #number of image frames
blank_time = 30

exp_name = 'N300 Scenes'
exp_info = {'participant':'',
            'sex':['Male','Female'],
            'age':'',
            'left-handed':False}
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

#If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

#win = visual.Window(size=scrsize, color='gray', units='pix', fullscr=True)
win = visual.Window(size=[800,600], color='gray', units='pix', fullscr=False)
win.recordFrameIntervals = True
#joystick.backend = 'pyglet'
#njoys = joystick.getNumJoysticks()
pygame.init()
pygame.joystick.init()
id = 0
joy = pygame.joystick.Joystick(id)
joy.init()
#nAxes = joy.getNumAxes()
#nButtons = joy.getNumButtons()
m = event.Mouse(win=win)
m.setVisible(False)
rate = win.getActualFrameRate(nIdentical=10, nMaxFrames=100, nWarmUpFrames=10, threshold=1)

load_message = visual.TextStim(win,
                               text="Loading...",
                               color='black',height=20)

attend_message = visual.TextStim(win,
                                text="We will begin the next section. Please keep your eyes on the fixation cross at the center of the screen at all times. Meanwhile, try to pay attention to each scene that appears. If you think the scene is a bad exemplar of its category, press the red 'B' button. Press 'start' to begin.",
                                color='black', height=20)

distract_message = visual.TextStim(win,
                                text="We will begin the next section. Use the joystick to keep the bug in the bubble. While the bug is green, hold down the green 'A' button to influence it. While the bug is red, hold down the red 'B' button to influence it. Press 'start' to begin.",
                                color='black', height=20)

end_message = visual.TextStim(win,
                               text="Done with this section! Take a short break and press start when you are ready to begin the next section.",
                               color='black', height=20)

final_message = visual.TextStim(win,
                               text="You have completed the experiment! Please inform the experimenter that you are done.",
                               color='black', height=20)
load_message.draw()
win.flip()

#prac_dst()
#prac_att()
#N300_att_local()
#N300_att_global()
#N300_dst_local()
#N300_dst_global()

if int(exp_info['participant'])%4 == 1:
    prac_att()
    load_message.draw()
    win.flip()
    N300_att_global() #a
    load_message.draw()
    win.flip()
    prac_dst()
    load_message.draw()
    win.flip()
    N300_dst_global() #b
    load_message.draw()
    win.flip()
    N300_att_local() #c
    load_message.draw()
    win.flip()
    N300_dst_local() #d
elif int(exp_info['participant'])%4 == 2:
    prac_dst()
    load_message.draw()
    win.flip()
    N300_dst_global() #b
    load_message.draw()
    win.flip()
    prac_att()
    load_message.draw()
    win.flip()
    N300_att_global() #a
    load_message.draw()
    win.flip()
    N300_att_local() #c
    load_message.draw()
    win.flip()
    N300_dst_local() #d
elif int(exp_info['participant'])%4 == 3:
    prac_att()
    load_message.draw()
    win.flip()
    N300_att_global() #a
    load_message.draw()
    win.flip()
    prac_dst()
    load_message.draw()
    win.flip()
    N300_dst_global() #b
    load_message.draw()
    win.flip()
    N300_dst_local() #d
    load_message.draw()
    win.flip()
    N300_att_local() #c
elif int(exp_info['participant'])%4 == 0:
    prac_dst()
    load_message.draw()
    win.flip()
    N300_dst_global() #b
    load_message.draw()
    win.flip()
    prac_att()
    load_message.draw()
    win.flip()
    N300_att_global() #a
    load_message.draw()
    win.flip()
    N300_att_local() #d
    load_message.draw()
    win.flip()
    N300_dst_local() #c


joy.quit()
joy.init()

doneN3_button = 0   
while doneN3_button == 0:     
    final_message.draw()
    win.flip()
    doneN3_button = joy.get_button(9)
    keys = event.getKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        break

m.setVisible(True)
win.close()
core.quit()