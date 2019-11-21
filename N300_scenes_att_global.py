# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:44:41 2019

@author: rift
"""

def N300_att_global():
    
    rnd.seed()
    
    good_val = 2
    bad_val = 3
    
    end_message = visual.TextStim(win,
                               text="Done with this section! Take a short break and press start when you are ready to begin the next section.",
                               color='black', height=20)
    
    # scene stimulus stuff
    bitmaps = [visual.ImageStim(win, img, ori=0, pos=[0, 0]) for img in N3tList_ag]
        
    response = list(np.repeat(None,n_good_att+n_bad_att+1))
    N3stim_order = []
    
    N3data_fname = 'N300_scenes_att_global_' + exp_info['participant'] + '_' + exp_info['date']
    N3data_fname = os.path.join(datapath, N3data_fname)
    
    for trial_num, im, resp in zip(range(1,len(N3tList_ag)+1), N3tList_ag, response):
        N3stim_order.append({'trial_num': trial_num, 'im': im, 'resp': resp})
    
    N3trials = data.TrialHandler(N3stim_order, nReps=1, extraInfo=exp_info,
                                   method='sequential', originPath=datapath)
        
    joy.quit()
    joy.init()
    buttons = 0
    xAxis = []
    yAxis = []
    keys = []
    
    p_port.setData(0) # make sure ports are initialized to 0
    
    # Define the fixation
    fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((-5, 0), (5, 0)), pos=(0, 0))
    fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((0, -5), (0, 5)), pos=(0, 0))
        
    load_message.draw()
    win.flip()
    
    go_button = 0
    while go_button == 0:
        attend_message.draw()
        win.flip()
        go_button = joy.get_button(9)
        keys = event.getKeys(keyList=['space','escape'])
        if 'escape' in keys:
            m.setVisible(True)
            win.close()
            core.quit()
    
    # Wait for a spacebar press to start the trial, or escape to quit
    
    fix1.draw()
    fix2.draw()
    win.flip()
    core.wait(1)

    i = 0
    
    # Run through the trials
    for trial in N3trials:
        
        bitmap = bitmaps[i]
        i += 1
        
        response_frames = []
        
        if 'good' in trial['im']:
            port_val = good_val
        elif 'bad' in trial['im']:
            port_val = bad_val
    
        # Leave an 'escape' press in for immediate exit
        if 'escape' in keys:
            break
    
        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        for frame in range(im_time):
            bitmap.draw()
            fix1.draw()
            fix2.draw()
            win.flip()
            
            if frame == 0:        
                p_port.setData(port_val)
                core.wait(.001)
                p_port.setData(0)
                
            keys = event.getKeys(keyList=['space','escape','up','down','left','right'])
            buttonA = joy.get_button(1)
            buttonB = joy.get_button(2)
            if buttonB == 1:
                response_frames.append(1)
            else: response_frames.append(0)
            quit_buttons = joy.get_button(1),joy.get_button(9),joy.get_button(4),joy.get_button(5)
            if sum(quit_buttons)==4:
                win.close()
                core.quit()
            
            if 'escape' in keys:
                break
        
        for frame in range(blank_time):
            fix1.draw()
            fix2.draw()
            win.flip()
            
            keys = event.getKeys(keyList=['space','escape','up','down','left','right'])
            buttonA = joy.get_button(1)
            buttonB = joy.get_button(2)
            quit_buttons = joy.get_button(1),joy.get_button(9),joy.get_button(4),joy.get_button(5)
            if sum(quit_buttons)==4:
                win.close()
                core.quit()
            
            if 'escape' in keys:
                break
    
        # For the duration of trial time,
        # Listen for a response or escape press
        keys = event.getKeys(keyList=['space','escape'])
        
        if 'bad' in trial['im'] and any(response_frames) == 1: #hit
            trial['resp'] = 1
        elif 'good' in trial['im'] and any(response_frames) == 1: #false alarm
            trial['resp'] = 0
        elif 'bad' in trial['im'] and sum(response_frames) < 1: #miss
            trial['resp'] = 0
        elif 'good' in trial['im'] and sum(response_frames) < 1: #correct rejection
            trial['resp'] = 1
        if 'escape' in keys:
            break
    
        # Advance to the next trial after brief pause
        
        if trial['trial_num'] == len(bitmaps):
            N3trials.saveAsWideText(N3data_fname + '.csv', delim=',')
            doneN3_button = 0   
            while doneN3_button == 0:     
                end_message.draw()
                win.flip()
                doneN3_button = joy.get_button(9)
                keys = event.getKeys(keyList=['space', 'escape'])
                if 'escape' in keys:
                    break
            win.flip()
            core.wait(.5)
            
            
        elif trial['trial_num']%break_time == 0:
            N3trials.saveAsWideText(N3data_fname + '.csv', delim=',')
            block_num = np.divide(trial['trial_num'],break_time)
            block_tot = np.divide(len(bitmaps),break_time)
            block_missive = 'You have completed block ' + str(block_num) + ' out of ' + str(block_tot) + '. ' + 'Please take a short break and press start when you are ready to continue.'
            block_message = visual.TextStim(win, text=block_missive, color='black', height=20)        
            block_button = 0    
            while block_button == 0:     
                block_message.draw()
                win.flip()
                block_button = joy.get_button(9)
                keys = event.getKeys(keyList=['space', 'escape'])
                if 'escape' in keys:
                    break
            win.flip()
            core.wait(.5)
            
        elif 'escape' in keys:
            break
        