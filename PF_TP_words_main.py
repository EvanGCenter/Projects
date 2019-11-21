# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:06:54 2019

@author: Evan
"""

import os                           # for file/folder operations
import numpy as np
import numpy.random as rnd          # for random number generators
from psychopy import visual, event, core, gui, data
import pygame

#==============================================
# Settings that we might want to tweak later on
#==============================================

runfile('C:/Python27/Scripts/PF_TP_words_visual.py', wdir='C:/Python27/Scripts')
runfile('C:/Python27/Scripts/PF_TP_words_visPrac.py', wdir='C:/Python27/Scripts')
runfile('C:/Python27/Scripts/PF_TP_words_audio.py', wdir='C:/Python27/Scripts')
runfile('C:/Python27/Scripts/PF_TP_words_audPrac.py', wdir='C:/Python27/Scripts')

rnd.seed()

legit_path = 'C:\\Python27\\Sounds\\tru_words\\'
pseudo_path = 'C:\\Python27\\Sounds\\non_words\\'

datapath = 'C:\Python27\Scripts\data'                   # directory to save data in
scrsize = (1280,960)                 # screen size in pixels
timelimit = 3                       # trial time limit in seconds
break_time = 18         
blank_time = 30      

exp_name = 'PF TP words exp'
exp_info = {
            'participant': '',
            'gender': '',
            'age':'',
            'handedness':('right', 'left', 'ambi')
            }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

if dlg.OK == False:
    core.quit()

# Get date and time 
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = 'PF_TP_words_pilot' + exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)

# Open a window
win = visual.Window(size=scrsize, color='gray', units='pix', fullscr=True)
#win = visual.Window(size=[800,600], color='gray', units='pix', fullscr=False) #debugging window
m = event.Mouse(win=win)
m.setVisible(False)
rate = win.getActualFrameRate(nIdentical=10, nMaxFrames=100, nWarmUpFrames=30, threshold=1)
exp_info['tfr'] = rate

if rate < 59 or rate > 61:
    print "Hi RA, please double check the refresh rate and set to 60 Hz! Thank you -Evan"
    win.close()
    core.quit()
    m.setVisible(True)

# Define trial start text
load_message = visual.TextStim(win,
                               text="Loading...",
                               color='black', height=20)
prac_message_A = visual.TextStim(win,
                                text="This is a practice block. Pay attention to the duration of each audio clip pair and try to tell which audio clip in the pair lasted longer. Use the left arrow key to say the first audio clip lasted longer. Use the right arrow key to say the second audio clip lasted longer. Try to be as quick and accurate as possible. Keep your eyes on the central fixation cross at all times. Press spacebar to begin.",
                                color='black', height=20)
start_message_A = visual.TextStim(win,
                                text="Pay attention to the duration of each spoken word or acronym pair and try to tell which item in the pair lasted longer. Pay careful attention to each item's duration, ignoring the speed at which the item is read. Use the left arrow key to say the first word or acronym lasted longer. Use the right arrow key to say the second word or acronym lasted longer. Try to be as quick and accurate as possible. You will no longer receive feedback after each trial. Keep your eyes on the central fixation cross at all times. Press spacebar to begin.",
                                color='black', height=20)
start_message_V = visual.TextStim(win,
                                text="Pay attention to the duration of each written word or acronym pair and try to tell which item in the pair lasted longer. Use the left arrow key to say the first word or acronym lasted longer. Use the right arrow key to say the second word or acronym lasted longer. Try to be as quick and accurate as possible. Keep your eyes on the central fixation cross at all times. Press spacebar to begin.",
                                color='black', height=20)
prac_message_V = visual.TextStim(win,
                                text="This is a practice block. Pay attention to the duration of each written word or acronym pair and try to tell which item in the pair lasted longer. Use the left arrow key to say the first word or acronym lasted longer. Use the right arrow key to say the second word or acronym lasted longer. Try to be as quick and accurate as possible. You will no longer receive feedback after each trial. Keep your eyes on the central fixation cross at all times. Press spacebar to begin.",
                                color='black', height=20)
section_message = visual.TextStim(win,
                               text="That's it for this section! Take a short break and press space bar when you are ready to continue on to the next section.",
                               color='black', height=20)
end_message = visual.TextStim(win,
                              text="All done with the experiment! Please inform the experimenter.",
                              color='black', height=20)

AvsV = int(exp_info['participant'])

if AvsV%2 == 1:
    load_message.draw()
    win.flip()
    prac_message_V.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_visual_prac()
    load_message.draw()
    win.flip()           
    start_message_V.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_visual()
    load_message.draw()
    win.flip()
    prac_message_A.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    PF_TP_audio_prac()
    load_message.draw()
    win.flip()
    start_message_A.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_audio()
    
elif AvsV%2 == 0:
    load_message.draw()
    win.flip()
    prac_message_A.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    PF_TP_audio_prac()
    load_message.draw()
    win.flip()
    start_message_A.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_audio()
    load_message.draw()
    win.flip()
    prac_message_V.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_visual_prac()
    load_message.draw()
    win.flip()           
    start_message_V.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    load_message.draw()
    win.flip()
    PF_TP_visual()
    
end_message.draw()
win.flip()
keys = event.waitKeys(keyList=['space', 'escape'])
win.flip()
    
m.setVisible(True)
win.close()
core.quit()
