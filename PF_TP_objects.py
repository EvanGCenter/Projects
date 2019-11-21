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
from psychopy import visual, event, core, gui, data, logging

#==============================================
# Settings that we might want to tweak later on
#==============================================

n_files = 180     
break_time = 20              
datapath = 'data'                   # directory to save data in
impath = 'C:\Python27\images'       #directory where images can be found
imlist1 = np.random.choice(range(1,n_files+1,1),n_files,replace=False)              # image names without the suffixes
imlist1 = map(str,imlist1)
imlist2 = np.random.choice(range(1,n_files+1,1),n_files,replace=False)
imlist2 = map(str,imlist2)
asfx = 'a.tif'                      # suffix for the first image
bsfx = 'b.tif'                      # suffix for the second image
scrsize = (1280,1024)                 # screen size in pixels
timelimit = 3                       # trial time limit in seconds
#changetime1 = range(18,43,3)         # image presentation frames
changetime1 = range(18,43,3)
mult = n_files/len(changetime1)
changetime1 = np.repeat(changetime1, mult, axis=0)
#np.random.shuffle(changetime1)
changetime1 = changetime1.tolist()
changetime2 = np.median(changetime1)
changetime2 = int(changetime2)
changetime2 = np.repeat(changetime2, n_files, axis=0)
changetime2 = changetime2.tolist()
order = range(1,5)
mult2 = n_files/len(order)
order = np.tile(order, mult2)
#np.random.shuffle(order)
order = order.tolist()
combo = np.column_stack((changetime1,order))
np.random.shuffle(combo)
changetime1 = combo[:,0]
changetime1 = changetime1.tolist()
order = combo[:,1]
order = order.tolist()

#========================================
# Store info about the experiment session
#========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'PF TP objects 1'
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
data_fname = 'time' + exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)


#========================
# Prepare condition lists
#========================

# Check if all images exist
for im in imlist1:
    if (not os.path.exists(os.path.join(impath, im+asfx)) or
        not os.path.exists(os.path.join(impath, im+bsfx))):
        raise Exception('Image files not found in image folder: ' + str(im))

#===============================
# Creation of window and stimuli
#===============================

# Open a window
win = visual.Window(size=scrsize, color='white', units='pix', fullscr=True)
m = event.Mouse(win=win)
m.setVisible(False)
rate = win.getActualFrameRate(nIdentical=10, nMaxFrames=100, nWarmUpFrames=10, threshold=1)

# Define trial start text
start_message = visual.TextStim(win,
                                text="Use the left key to say the first image lasted longer. Use the right key to say the second image lasted longer. Press spacebar to begin.",
                                color='blue', height=20)
block_message = visual.TextStim(win,
                                text="Please take a short break. You may press the spacebar when you are ready to contintue.",
                                color='blue', height=20)
end_message = visual.TextStim(win,
                              text="All done! Please inform the experimenter.",
                              color='blue', height=20)

# Define bitmap stimulus (contents can still change)
bitmap1 = visual.ImageStim(win, size=None)
bitmap2 = visual.ImageStim(win, size=None)

# Define the fixation
fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((-5, 0), (5, 0)), pos=(0, 0))
fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((0, -5), (0, 5)), pos=(0, 0))

#==========================
# Define the trial sequence
#==========================

# Define a list of trials with their properties:
#   - Which image (without the suffix)
#   - Which orientation
stim_order = []
for trial_num, im1, im2, ordr, time1, time2 in zip(range(1,n_files+1), imlist1, imlist2, order, changetime1, changetime2):
    stim_order.append({'trial_num': trial_num, 'im1': im1, 'im2': im2, 'order': ordr, 'time1': time1, 'time2': time2})

trials = data.TrialHandler(stim_order, nReps=1, extraInfo=exp_info,
                           method='sequential', originPath=datapath)


#=====================
# Start the experiment
#=====================

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

# Run through the trials
for trial in trials:

    # Set the images, set the orientation
    im_fname1 = os.path.join(impath, trial['im1'])
    im_fname2 = os.path.join(impath, trial['im2'])
    bitmap1.setImage(im_fname1 + asfx)
    bitmap2.setImage(im_fname2 + bsfx)

    # Set the clocks to 0
    change_clock.reset()
    rt_clock.reset()

    # Empty the keypresses list
    # Leave an 'escape' press in for immediate exit
    keys = []

    # Start the trial
    # Stop trial if spacebar or escape has been pressed, or if 30s have passed
    while len(keys) == 0 and rt_clock.getTime() < timelimit:
        
        if trial['order'] == 1: #GC -> BS
            for frame in range(trial['time1']):
                bitmap1.draw() #show good exemplar first for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
                
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(.5)
                            
            for frame in range(trial['time2']):
                bitmap2.draw() #show bad exemplar second for standard time
                fix1.draw()
                fix2.draw()
                win.flip()

        elif trial['order'] == 2: #BS -> GC
            for frame in range(trial['time2']):
                bitmap2.draw() #show bad exemplar first for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
                
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(.5)
                            
            for frame in range(trial['time1']):
                bitmap1.draw() #show good exemplar second for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()        
        
        elif trial['order'] == 3: #BC -> GS
            for frame in range(trial['time1']):
                bitmap2.draw() #show bad exemplar first for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
                
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(.5)
                            
            for frame in range(trial['time2']):
                bitmap1.draw() #show good exemplar second for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
                
        elif trial['order'] == 4: #GS -> BC
            for frame in range(trial['time2']):
                bitmap1.draw() #show good exemplar first for standard time
                fix1.draw()
                fix2.draw()
                win.flip()
                
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(.5)
                            
            for frame in range(trial['time1']):
                bitmap2.draw() #show bad exemplar second for comparison time
                fix1.draw()
                fix2.draw()
                win.flip()
            
        fix1.draw()
        fix2.draw()
        win.flip()
        rt_clock.reset()

        # For the duration of trial time,
        # Listen for a response or escape press
        change_clock.reset()
        while change_clock.getTime() <= timelimit:
            keys = event.getKeys(keyList=['left', 'right', 'escape'])
            if len(keys) > 0:
                break

    # Analyze the keypress
    if keys:
        if 'escape' in keys:
            # Escape press = quit the experiment
            m.setVisible(True)
            break
        elif trial['order']%2 == 1:
            if 'left' in keys and trial['time1'] >= trial['time2']:
                #comparison time first, comparison time longer, first image selected
                acc = 1
                cjl = 1
                rt = rt_clock.getTime()
            elif 'right' in keys and trial['time2'] > trial['time1']:
                #comparison time first, comparison time shorter, second image selected
                acc = 1
                cjl = 0
                rt = rt_clock.getTime()
            elif 'left' in keys and trial['time2'] > trial['time1']:
                #comparison time first, comparison time shorter, first image selected
                acc = 0
                cjl = 1
                rt = rt_clock.getTime()
            elif 'right' in keys and trial['time1'] >= trial['time2']:
                #comparison time first, comparison time longer, second image selected
                acc = 0
                cjl = 0
                rt = rt_clock.getTime()
                
        elif trial['order']%2 == 0:
            if 'left' in keys and trial['time2'] >= trial['time1']:
                #comparison time second, comparison time shorter, first image selected
                acc = 1
                cjl = 0
                rt = rt_clock.getTime()
            elif 'right' in keys and trial['time1'] > trial['time2']:
                #comparison time second, comparison time longer, second image selected
                acc = 1
                cjl = 1
                rt = rt_clock.getTime()
            elif 'left' in keys and trial['time1'] > trial['time2']:
                #comparison time second, comparison time longer, first image selected
                acc = 0
                cjl = 0
                rt = rt_clock.getTime()
            elif 'right' in keys and trial['time2'] >= trial['time1']:
                #comparison time second, comparison time shorter, second image selected
                acc = 0
                cjl = 1
                rt = rt_clock.getTime()

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
    

    # Advance to the next trial after brief pause
    core.wait(rnd.uniform(.5,1.5))
    
    if trial['trial_num'] == n_files:
        end_message.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()

    elif trial['trial_num']%break_time == 0:
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
m.setVisible(True)
win.close()
core.quit()