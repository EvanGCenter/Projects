# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:11:10 2019

@author: Evan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 16:47:37 2017

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

runfile('C:/Users/Evan/Anaconda2/Scripts/intact_diffeo_objects_quest.py', wdir='C:/Users/Evan/Anaconda2/Scripts')
runfile('C:/Users/Evan/Anaconda2/Scripts/intact_diffeo_objects_main.py', wdir='C:/Users/Evan/Anaconda2/Scripts')

datapath = 'data'                   # directory to save data in
impath = 'C:\Users\Evan\Anaconda2\Images\objects'       #directory where images can be found
dmpath = 'C:\Users\Evan\Anaconda2\Images\diffeomorphed'
mask_path = 'C:\\Users\\Evan\\Anaconda2\\Images\\20_overlay_mask.tif'
imlist_g = [f for f in os.listdir(impath) if not f.startswith('.') and f.endswith('a.TIF')]
imlist_b = [f for f in os.listdir(impath) if not f.startswith('.') and f.endswith('b.TIF')]
dmlist_g = [f for f in os.listdir(dmpath) if not f.startswith('.') and f.endswith('a.TIF')]
dmlist_b = [f for f in os.listdir(dmpath) if not f.startswith('.') and f.endswith('b.TIF')]

scrsize = (1024,768)                 # screen size in pixels
timelimit = 1.6                       # trial time limit in seconds
exp_dur_g = 20         # image presentation frames
exp_dur_b = 20
msk_dur = 30
break_time = 30
n_quest = 240

#========================================
# Store info about the experiment session
#========================================
 
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Diffeo intact/scrambled'
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
#if not os.path.isdir(datapath):
#    os.makedirs(datapath)
#data_fname = 'intact_diffeo_obj_' + exp_info['participant'] + '_' + exp_info['date']
#data_fname = os.path.join(datapath, data_fname)

#===============================
# Creation of window and stimuli
#===============================

# Open a window
#win = visual.Window(size=scrsize, color='white', units='pix', fullscr=True)
win = visual.Window(size=[800,600], color='white', units='pix', fullscr=False) #debugging window
m = event.Mouse(win=win)
m.setVisible(False)

# Define trial start text
start_message = visual.TextStim(win,
                                text="Use the left control key to say the image was clear. Use the right control key to say the image was noisey. Press spacebar to begin.",
                                color='black', height=20)
end_message = visual.TextStim(win,
                              text="Done with this section! Please inform the experimenter.",
                              color='black', height=20)
load_message = visual.TextStim(win,
                               text = 'Loading...',
                               color='black', height = 20)
final_message = visual.TextStim(win,
                               text = 'All done with the experiment! Please inform the experimenter.',
                               color='black', height = 20)

load_message.draw()
win.flip()

all_im_paths_g = [os.path.join(impath,im) for im in imlist_g]
all_im_paths_b = [os.path.join(impath,im) for im in imlist_b]
all_dm_paths_g = [os.path.join(dmpath,dm) for dm in dmlist_g]
all_dm_paths_b = [os.path.join(dmpath,dm) for dm in dmlist_b]

all_paths = all_im_paths_g+all_dm_paths_g+all_im_paths_b+all_dm_paths_b
rnd.shuffle(all_paths)

shffl_images = all_paths

full_imset = [visual.ImageStim(win,im) for im in shffl_images]
mask = visual.ImageStim(win,mask_path)

exp_dur = ido_quest()
ido_main()

keys = 0
while keys == 0:
        final_message.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.flip()

m.setVisible(True)
win.close()
core.quit()