# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 12:35:05 2017

@author: Evan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 14:17:00 2016

@author: Evan
"""

#===============
# Import modules
#===============

import os                           # for file/folder operations
import numpy as np
import numpy.random as rnd          # for random number generators
from psychopy import visual, event, core, gui, data

#==============================================
# Settings that we might want to tweak later on
#==============================================

rnd.seed()
break_time = 20              
datapath = 'C:\Python27\Scripts\data'                   # directory to save data in
impath = 'C:\Python27\Images\scenes\upsidedown'       #directory where images can be found

imlist_full = [f for f in os.listdir(impath) if not f.startswith('.')]
n_files = len(imlist_full)/2
rnd.shuffle(imlist_full)
imlist1 = imlist_full[0:n_files]
imlist2 = imlist_full[n_files:n_files*2]

scrsize = (1280,960)                 # screen size in pixels
timelimit = 3                       # trial time limit in seconds
#changetime1 = range(18,43,3)         # image presentation frames
changetime1 = range(18,43,3)
blank_time = 30
mult = n_files/len(changetime1)
changetime1 = np.repeat(changetime1, mult, axis=0)
changetime1 = changetime1.tolist()
changetime2 = np.median(changetime1)
changetime2 = int(changetime2)
changetime2 = np.repeat(changetime2, n_files, axis=0)
changetime2 = changetime2.tolist()
order = range(1,5)
mult2 = n_files/len(order)
order = np.tile(order, mult2)
order = order.tolist()
combo = np.column_stack((changetime1,order))
rnd.shuffle(combo)
changetime1 = combo[:,0]
changetime1 = changetime1.tolist()
order = combo[:,1]
order = order.tolist()

#========================================
# Store info about the experiment session
#========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'PF TP orientation'
exp_info = {
            'participant': '',
            'gender': ('male', 'female'),
            'age':'',
            'left-handed':False
            }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = 'time_scenes_ori' + exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)


#===============================
# Creation of window and stimuli
#===============================

# Open a window
win = visual.Window(size=scrsize, color='gray', units='pix', fullscr=True)
#win = visual.Window(size=[800,600], color='gray', units='pix', fullscr=False) #debugging window
m = event.Mouse(win=win)
m.setVisible(False)
rate = win.getActualFrameRate(nIdentical=10, nMaxFrames=100, nWarmUpFrames=30, threshold=1)
exp_info['tfr'] = rate

# Define trial start text
start_message = visual.TextStim(win,
                                text="Use the left key to say the first image lasted longer. Use the right key to say the second image lasted longer. Press spacebar to begin.",
                                color='black', height=20)
end_message = visual.TextStim(win,
                              text="All done! Please inform the experimenter.",
                              color='black', height=20)

# Define bitmap stimulus (contents can still change)
#bitmap1 = visual.ImageStim(win, size=None)
#bitmap2 = visual.ImageStim(win, size=None)

# Define the fixation
fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((-5, 0), (5, 0)), pos=(0, 0))
fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((0, -5), (0, 5)), pos=(0, 0))

#==========================
# Define the trial sequence
#==========================

# Define a list of trials with their properties:
#   - Which image (without the suffix)
#   - Which orientation
stim_order = []
for trial_num, im1, im2, order, time1, time2 in zip(range(1,n_files+1), imlist1, imlist2, order, changetime1, changetime2):
    stim_order.append({'trial_num': trial_num, 'im1': im1, 'im2': im2, 'order': order, 'time1': time1, 'time2': time2})

trials = data.TrialHandler(stim_order, nReps=1, extraInfo=exp_info,
                           method='sequential', originPath=datapath)


#=====================
# Start the experiment
#=====================

load_message = visual.TextStim(win,
                                text="Loading...",
                                color='black', height=20)
                                
load_message.draw()
win.flip()

im_addresses1 = [os.path.join(impath,pic) for pic in imlist1]
im_addresses2 = [os.path.join(impath,pic) for pic in imlist2]

bitmap1 = [visual.ImageStim(win, img, ori=0, pos=[0,0]) for img in im_addresses1]
bitmap2 = [visual.ImageStim(win, img, ori=180, pos=[0,0]) for img in im_addresses2]

# Initialize two clocks:
#   - for image change time
#   - for response time
change_clock = core.Clock()
rt_clock = core.Clock()

# Display trial start text
start_message.draw()
win.flip()

# Wait for a spacebar press to start the trial, or escape to quit
keys = event.waitKeys(keyList=['space', 'escape'])
fix1.draw()
fix2.draw()
win.flip()
core.wait(1)

stim1_clock = core.Clock()
blank_clock = core.Clock()
stim2_clock = core.Clock()

p = 0

# Run through the trials
for trial in trials:

    # Set the images, set the orientation
#    im_fname1 = os.path.join(impath, trial['im1'])
#    im_fname2 = os.path.join(impath, trial['im2'])
#    bitmap1.setImage(im_fname1)
#    bitmap2.setImage(im_fname2)
#    bitmap1.ori = 0
#    bitmap2.ori = 180
        
    # Set the clocks to 0
    change_clock.reset()
    rt_clock.reset()

    # Empty the keypresses list
    # Leave an 'escape' press in for immediate exit
    keys = []

    # Start the trial
    # Stop trial if spacebar or escape has been pressed, or if 30s have passed
    while len(keys) == 0 and rt_clock.getTime() < timelimit:
        
        if trial['order'] == 1: #UC -> DS
            stim1_clock.reset()
            for frame in range(trial['time1']):
                bitmap1[p].draw() #show upright first for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim1 = stim1_clock.getTime()
            
            blank_clock.reset()
            for frame in range(blank_time):
                fix1.draw()
                fix2.draw()
                win.flip()
            t_blank = blank_clock.getTime()
            
            stim2_clock.reset()                
            for frame in range(trial['time2']):
                bitmap2[p].draw() #show upsidedown second for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim2 = stim2_clock.getTime()

        elif trial['order'] == 2: #DS -> UC
            stim2_clock.reset()
            for frame in range(trial['time2']):
                bitmap2[p].draw() #show upsidedown first for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim2 = stim2_clock.getTime()
                
            blank_clock.reset()
            for frame in range(blank_time):
                fix1.draw()
                fix2.draw()
                win.flip()
            t_blank = blank_clock.getTime()
            
            stim1_clock.reset()                
            for frame in range(trial['time1']):
                bitmap1[p].draw() #show upright second for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()        
            t_stim1 = stim1_clock.getTime()
        
        elif trial['order'] == 3: #DC -> US
            stim1_clock.reset()
            for frame in range(trial['time1']):
                bitmap2[p].draw() #show upsidedown first for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim1 = stim1_clock.getTime()
                
            blank_clock.reset()
            for frame in range(blank_time):
                fix1.draw()
                fix2.draw()
                win.flip()
            t_blank = blank_clock.getTime()
            
            stim2_clock.reset()                
            for frame in range(trial['time2']):
                bitmap1[p].draw() #show upright second for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim2 = stim2_clock.getTime()
                
        elif trial['order'] == 4: #US -> DC
            stim2_clock.reset()
            for frame in range(trial['time2']):
                bitmap1[p].draw() #show upright first for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim2 = stim2_clock.getTime()
                
            blank_clock.reset()
            for frame in range(blank_time):
                fix1.draw()
                fix2.draw()
                win.flip()
            t_blank = blank_clock.getTime()
            
            stim1_clock.reset()                
            for frame in range(trial['time1']):
                bitmap2[p].draw() #show upsidedown second for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
            t_stim1 = stim1_clock.getTime()
            
        fix1.draw()
        fix2.draw()
        win.flip()
        rt_clock.reset()

        # For the duration of trial time,
        # Listen for a response or escape press
        change_clock.reset()
        keys = event.waitKeys(keyList=['left', 'right', 'escape'],maxWait=timelimit)
        if change_clock.getTime() >= timelimit:
            keys = []
            break
    
    # Analyze the keypress
    if keys:
        rt = rt_clock.getTime()
        if 'escape' in keys:
            # Escape press = quit the experiment
            m.setVisible(True)
            break
        elif trial['order']%2 == 1:
            if 'left' in keys and trial['time1'] >= trial['time2']:
                #comparison time first, comparison time longer, first image selected
                acc = 1
                cjl = 1
            elif 'right' in keys and trial['time2'] > trial['time1']:
                #comparison time first, comparison time shorter, second image selected
                acc = 1
                cjl = 0
            elif 'left' in keys and trial['time2'] > trial['time1']:
                #comparison time first, comparison time shorter, first image selected
                acc = 0
                cjl = 1
            elif 'right' in keys and trial['time1'] >= trial['time2']:
                #comparison time first, comparison time longer, second image selected
                acc = 0
                cjl = 0
                
        elif trial['order']%2 == 0:
            if 'left' in keys and trial['time2'] >= trial['time1']:
                #comparison time second, comparison time shorter, first image selected
                acc = 1
                cjl = 0
            elif 'right' in keys and trial['time1'] > trial['time2']:
                #comparison time second, comparison time longer, second image selected
                acc = 1
                cjl = 1
            elif 'left' in keys and trial['time1'] > trial['time2']:
                #comparison time second, comparison time longer, first image selected
                acc = 0
                cjl = 0
            elif 'right' in keys and trial['time2'] >= trial['time1']:
                #comparison time second, comparison time shorter, second image selected
                acc = 0
                cjl = 1

    else:
        # No press = failed response; maximal response time
        acc = 0
        cjl = None
        rt = timelimit

    # Add the current trial's data to the TrialHandler
    keys = []   
    trials.addData('rt', rt)
    trials.addData('acc', acc)
    trials.addData('cjl', cjl)
    trials.addData('mcd', t_stim1)
    trials.addData('msd', t_stim2)
    trials.addData('mbd', t_blank)
    
    p += 1

    # Advance to the next trial after brief pause
    core.wait(rnd.uniform(.5,1.5))    
    
    if trial['trial_num'] == n_files:
        end_message.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()
        if keys != 0:
            m.setVisible(True)
            win.close()
            #core.quit()
            break

    elif trial['trial_num']%break_time == 0:
        block_num = np.divide(trial['trial_num'],break_time)
        block_tot = np.divide(n_files,break_time)
        block_missive = 'You have completed block ' + str(block_num) + ' out of ' + str(block_tot) + '. ' + 'Please take a short break and press the spacebar when you are ready to continue.'
        block_message = visual.TextStim(win, text=block_missive, color='black', height=20)        
        block_message.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()
        core.wait(.5)
        

#======================
# End of the experiment
#======================

# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')

# Quit the experiment
#m.setVisible(True)
#win.close()
core.quit()