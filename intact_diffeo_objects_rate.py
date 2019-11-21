# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:46:30 2019

@author: Evan
"""
    
def ido_rate():
    
    # Create a unique filename for the experiment data
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    data_fname = 'intact_diffeo_rate_' + exp_info['participant'] + '_' + exp_info['date']
    data_fname = os.path.join(datapath, data_fname)
    
    instruct_message = visual.TextStim(win,
                               text = 'For this section, you will rate how typical each viewpoint of each object seems to you. This section is not timed. Please take a moment to consider each item. Press "space" to begin.',
                               color='black', height = 20)
    
    rate_message = visual.TextStim(win,
                               text = 'How typical is this viewpoint for this object? Please use the number pad to rate it on a scale from 1 to 7 with 1 representing very atypical and 7 representing very typical.',
                               color='black', height = 20, pos = (0,-600))
    
    n_files = n_quest
    
    # Define the fixation
    fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((-5, 0), (5, 0)), pos=(0, 0))
    fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='blue', fillColor='blue', vertices=((0, -5), (0, 5)), pos=(0, 0))
    
    
    #==========================
    # Define the trial sequence
    #==========================
    
    # Define a list of trials with their properties:
    #   - Which image (without the suffix)
    #   - Which orientation
    
    shffl_images_g = list(rnd.choice(all_im_paths_g,n_files/2,replace=False))
    shffl_images_b = list(rnd.choice(all_im_paths_b,n_files/2,replace=False))
    shffl_imrate = shffl_images_g+shffl_images_b
    rnd.shuffle(shffl_imrate)
    rate_imset = [visual.ImageStim(win,im) for im in shffl_imrate]
    
    im_names = ['IM_'+os.path.basename(f) for f in shffl_imrate]
    
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
    instruct_message.draw()
    win.flip()
    
    # Wait for a spacebar press to start the trial, or escape to quit
    keys = event.waitKeys(keyList=['space', 'escape'])
    win.flip()
    core.wait(2)
    
    stan_time = []
    comp_time = []
    wait_time = []
    
    stan_clock = core.Clock()
    comp_clock = core.Clock()
    
    p = 0
    
    # Run through the trials
    for trial in trials:
        
        stan_clock.reset()    
        
        current_image = rate_imset[p]
        p += 1
        
        # Set the clocks to 0
        change_clock.reset()
        rt_clock.reset()
    
        # Empty the keypresses list
        # Leave an 'escape' press in for immediate exit
        keys = []
    
        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        while len(keys) == 0:
            
            current_image.draw()
            rate_message.draw()
            win.flip()
                        
            rt_clock.reset()

            # For the duration of 'changetime',
            # Listen for a spacebar or escape press
            keys = event.waitKeys(keyList=['escape','num_1','num_2','num_3','num_4','num_5','num_6','num_7'])
            if 'escape' in keys:
                # Escape press = quit the experiment
                m.setVisible(True)
                win.close()
                break
            
        rt = rt_clock.getTime()
        
        # Add the current trial's data to the TrialHandler
        trials.addData('rt', rt)
        trials.addData('rating', keys)
        keys = []
        
        fix1.draw()
        fix2.draw()
        win.flip()
        core.wait(1)
        
        if trial['trial_num'] == n_files:
            end_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            win.flip()
    
    #======================
    # End of the experiment
    #======================
    
    # Save all data to a file
    trials.saveAsWideText(data_fname + '.csv', delim=',', appendFile=False)
    
    # Quit the experiment
    m.setVisible(True)
    win.close()
    core.quit()