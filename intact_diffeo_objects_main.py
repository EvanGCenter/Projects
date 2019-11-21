    ## -*- coding: utf-8 -*-
    #"""
    #Created on Wed Feb 20 16:12:08 2019
    #
    #@author: Evan
    #"""
    #
    
def ido_main():
    
    ##===============
    ## Import modules
    ##===============
    #
    #import os                           # for file/folder operations
    #import numpy as np
    #import numpy.random as rnd          # for random number generators
    #from psychopy import visual, event, core, gui, data
    #
    ##==============================================
    ## Settings that we might want to tweak later on
    ##==============================================
    #rnd.seed()
    #datapath = 'data'                   # directory to save data in
    #impath = 'C:\Users\Evan\Anaconda2\Images\objects'       #directory where images can be found
    #dmpath = 'C:\Users\Evan\Anaconda2\Images\diffeomorphed'
    #mask_path = 'C:\\Users\\Evan\\Anaconda2\\Images\\20_overlay_mask.tif'
    #imlist_g = [f for f in os.listdir(impath) if not f.startswith('.') and f.endswith('a.TIF')]
    #imlist_b = [f for f in os.listdir(impath) if not f.startswith('.') and f.endswith('b.TIF')]
    #dmlist_g = [f for f in os.listdir(dmpath) if not f.startswith('.') and f.endswith('a.TIF')]
    #dmlist_b = [f for f in os.listdir(dmpath) if not f.startswith('.') and f.endswith('b.TIF')]
    #
    #scrsize = (1024,768)                 # screen size in pixels
    #timelimit = 1.6                       # trial time limit in seconds
    ##exp_dur_g = 20         # image presentation frames
    ##exp_dur_b = 20
    #msk_dur = 30
    #break_time = 20
    #
    ##========================================
    ## Store info about the experiment session
    ##========================================
    #
    ## Get subject name, gender, age, handedness through a dialog box
    #exp_name = 'Diffeo intact/scrambled'
    #exp_info = {
    #            'participant': '',
    #            'gender': ('male', 'female'),
    #            'age':'',
    #            'left-handed':False
    #            }
    #dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    #
    ## If 'Cancel' is pressed, quit
    #if dlg.OK == False:
    #    core.quit()
    #
    ## Get date and time
    #exp_info['date'] = data.getDateStr()
    #exp_info['exp_name'] = exp_name
    #
    # Create a unique filename for the experiment data
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    data_fname = 'intact_diffeo_main_' + exp_info['participant'] + '_' + exp_info['date']
    data_fname = os.path.join(datapath, data_fname)
    #
    ##===============================
    ## Creation of window and stimuli
    ##===============================
    #
    ## Open a window
    #win = visual.Window(size=scrsize, color='white', units='pix', fullscr=True)
    ##win = visual.Window(size=[800,600], color='white', units='pix', fullscr=False) #debugging window
    #m = event.Mouse(win=win)
    #m.setVisible(False)
    #
    ## Define trial start text
    #start_message = visual.TextStim(win,
    #                                text="Use the left control key to say the image was clear. Use the right control key to say the image was noisey. Press spacebar to begin.",
    #                                color='black', height=20)
    #end_message = visual.TextStim(win,
    #                              text="All done! Please inform the experimenter.",
    #                              color='black', height=20)
    #load_message = visual.TextStim(win,
    #                               text = 'Loading...',
    #                               color='black', height = 20)
    #
    #load_message.draw()
    #win.flip()
    #
    #all_im_paths_g = [os.path.join(impath,im) for im in imlist_g]
    #all_im_paths_b = [os.path.join(impath,im) for im in imlist_b]
    #all_dm_paths_g = [os.path.join(dmpath,dm) for dm in dmlist_g]
    #all_dm_paths_b = [os.path.join(dmpath,dm) for dm in dmlist_b]
    #
    #all_paths = all_im_paths_g+all_dm_paths_g+all_im_paths_b+all_dm_paths_b
    #rnd.shuffle(all_paths)
    #
    #shffl_images = all_paths
    #
    #full_imset = [visual.ImageStim(win,im) for im in shffl_images]
    #mask = visual.ImageStim(win,mask_path)
    
    n_files = len(full_imset) - n_quest
    
    # Define the fixation
    fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((-5, 0), (5, 0)), pos=(0, 0))
    fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((0, -5), (0, 5)), pos=(0, 0))
    
    #==========================
    # Define the trial sequence
    #==========================
    
    # Define a list of trials with their properties:
    #   - Which image (without the suffix)
    #   - Which orientation
    
    im_names = ['DM_'+os.path.basename(f) if 'diffeomorphed' in f else 'IM_'+os.path.basename(f) for f in shffl_images]
    
    stim_order = []
    for trial_num, im in zip(range(1,n_files+1), im_names):
        stim_order.append({'trial_num': trial_num, 'im': im})
    
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
    fix1.draw()
    fix2.draw()
    win.flip()
    core.wait(2)
    
    stan_time = []
    comp_time = []
    wait_time = []
    
    stan_clock = core.Clock()
    comp_clock = core.Clock()
    
    p = n_quest
    
    # Run through the trials
    for trial in trials:
        
        stan_clock.reset()    
        
        current_image = full_imset[p]
        p += 1
        
        # Set the clocks to 0
        change_clock.reset()
        rt_clock.reset()
    
        # Empty the keypresses list
        # Leave an 'escape' press in for immediate exit
        keys = []
    
        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        while len(keys) == 0 and rt_clock.getTime() < timelimit:
            
            for frame in range(exp_dur):
                current_image.draw()
                fix1.draw()
                fix2.draw()
                win.flip()
            
            comp_i = comp_clock.getTime()
            comp_time.append(comp_i)  
                            
            for frame in range(msk_dur):
                mask.draw()
                fix1.draw()
                fix2.draw()
                win.flip()
                
            stan_i = stan_clock.getTime()
            stan_time.append(stan_i)
                    
            fix1.draw()
            fix2.draw()
            win.flip()
            rt_clock.reset()
    
            # For the duration of 'changetime',
            # Listen for a spacebar or escape press
            change_clock.reset()
            keys = event.waitKeys(keyList=['lctrl','rctrl','escape'],maxWait=timelimit)
            if change_clock.getTime() >= timelimit:
                keys = []
            break
    
        # Analyze the keypress
        if keys:
            if 'escape' in keys:
                # Escape press = quit the experiment
                m.setVisible(True)
                break
            elif 'DM' in trial['im']:
                if 'lctrl' in keys:
                    acc = 0
                    rt = rt_clock.getTime()
                elif 'rctrl' in keys:
                    acc = 1
                    rt = rt_clock.getTime()
                else:
                    acc = 0
                    rt = rt_clock.getTime()
            else:
                if 'lctrl' in keys:
                    acc = 1
                    rt = rt_clock.getTime()
                elif 'rctrl' in keys:
                    acc = 0
                    rt = rt_clock.getTime()
                else:
                    acc = 0
                    rt = rt_clock.getTime()
    
        else:
            # No press = failed change detection; maximal response time
            acc = 0
            rt = timelimit
        
#        print keys
#        print 'acc',acc
#        print trial['im']
        
        # Add the current trial's data to the TrialHandler
        trials.addData('rt', rt)
        trials.addData('acc', acc)
        keys = []
        
        core.wait(rnd.random()+.5)
        
        if trial['trial_num'] == n_files:
            end_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            win.flip()
    
        elif trial['trial_num']%break_time == 0:
            trials.saveAsWideText(data_fname + '.csv', delim=',', appendFile=False)
            block_num = np.divide(trial['trial_num'],break_time)
            block_tot = np.divide(n_files,break_time)
            block_missive = 'You have completed block ' + str(block_num) + ' out of ' + str(block_tot) + '. ' + 'Please take a short break and press the spacebar when you are ready to continue.'
            block_message = visual.TextStim(win, text=block_missive, color='black', height=20)        
            block_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(2)
    
    #======================
    # End of the experiment
    #======================
    
    # Save all data to a file
    trials.saveAsWideText(data_fname + '.csv', delim=',', appendFile=False)
    
    # Quit the experiment
    m.setVisible(True)
    win.close()
    core.quit()