# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 16:55:15 2017

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

n_files = 180
datapath = 'data'                   # directory to save data in
impath = 'C:\Python27\images'       #directory where images can be found
imlist1 = range(1,n_files+1,1)            # image names without the suffixes
imlist1 = map(str,imlist1)
imlist2 = range(1,n_files+1,1)
imlist2 = map(str,imlist2)
imlist = imlist1 + imlist2
asfx = 'a.tif'
asfx = np.tile(asfx,n_files)
asfx = asfx.tolist()
bsfx = 'b.tif'
bsfx = np.tile(bsfx,n_files)
bsfx = bsfx.tolist()
sfx = asfx + bsfx
#sfx = rnd.permutation(sfx)
combo = np.column_stack((imlist,sfx))
np.random.shuffle(combo)
imlist = combo[:,0]
imlist = imlist.tolist()
sfx = combo[:,1]
sfx = sfx.tolist()
scrsize = (1280,1024)                 # screen size in pixels
timelimit = 10                       # trial time limit in seconds

#========================================
# Store info about the experiment session
#========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'PF TP objects ratings'
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
data_fname = 'rate' + exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)


#========================
# Prepare condition lists
#========================

# Check if all images exist
for im, suf in zip(imlist, sfx):
    if (not os.path.exists(os.path.join(impath, im+suf))):
        raise Exception('Image files not found in image folder: ' + str(im))

#===============================
# Creation of window and stimuli
#===============================

# Open a window
win = visual.Window(size=scrsize, color='white', units='pix', fullscr=True)
m = event.Mouse(win=win)
m.setVisible(False)

# Define trial text
start_message = visual.TextStim(win,
                                text="Use the number pad to indicate how typical the view of each object is. 1 = highly atypical 2 = somewhat atypical 3 = neutral 4 = somewhat typical 5 = highly typical. Press the spacebar to begin.",
                                color='blue', height=20)
trial_message = visual.TextStim(win,
                                text="1 = highly atypical 2 = somewhat atypical 3 = neutral 4 = somewhat typical 5 = highly typical",
                                color='blue', pos = (0,-300), height=20)
end_message = visual.TextStim(win,
                              text="All done! Please inform the experimenter.",
                              color='blue', height=20)

# Define bitmap stimulus (contents can still change)
bitmap = visual.ImageStim(win, size=None)

#==========================
# Define the trial sequence
#==========================

# Define a list of trials with their properties:
#   - Which image (without the suffix)
#   - Which orientation
stim_order = []
for trial_num, im, suf in zip(range(1,n_files*2+1), imlist, sfx):
    stim_order.append({'trial_num': trial_num, 'im': im, 'suf': suf})

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
    im_fname = os.path.join(impath, trial['im'])
    bitmap.setImage(im_fname + trial['suf'])

    # Set the clocks to 0
    change_clock.reset()
    rt_clock.reset()

    # Empty the keypresses list
    # Leave an 'escape' press in for immediate exit
    keys = []

    # Start the trial
    # Stop trial if spacebar or escape has been pressed, or if 30s have passed
    while len(keys) == 0 and rt_clock.getTime() < timelimit:
        
       bitmap.draw()
       trial_message.draw()
       win.flip()
       rt_clock.reset()
       
    # Listen for a spacebar or escape press
       keys = event.getKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
       if len(keys) > 0:
            break

    # Analyze the keypress
    if keys:
        if 'escape' in keys:
            # Escape press = quit the experiment
            break
        elif '1' in keys:
            resp = 1
            rt = rt_clock.getTime()
        elif '2' in keys:
            resp = 2
            rt = rt_clock.getTime()
        elif '3' in keys:
            resp = 3
            rt = rt_clock.getTime()
        elif '4' in keys:
            resp = 4
            rt = rt_clock.getTime()
        elif '5' in keys:
            resp = 5
            rt = rt_clock.getTime()    

    else:
        # No press = failed change detection; maximal response time
        resp = None
        rt = timelimit

    # Add the current trial's data to the TrialHandler
    trials.addData('rt', rt)
    trials.addData('resp', resp)
    keys = []

    # Advance to the next trial after brief pause
    win.flip()
    core.wait(.5)
    
    if trial['trial_num'] == n_files*2:
        end_message.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        
#======================
# End of the experiment
#======================

# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')

# Quit the experiment
m.setVisible(True)
win.close()
core.quit()