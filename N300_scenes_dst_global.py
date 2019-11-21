# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 21:31:12 2018

@author: Evan
"""

def N300_dst_global():
    
    rnd.seed()
    
    good_val = 6
    bad_val = 7
    
    end_message = visual.TextStim(win,
                               text="Done with this section! Take a short break and press start when you are ready to begin the next section.",
                               color='black', height=20)
    
    # scene stimulus stuff
    bitmaps = [visual.ImageStim(win, img, ori=0, pos=[0, 0]) for img in N3tList_dg]
        
    response = list(np.repeat(None,n_good_dst+n_bad_dst+1))
    N3stim_order = []
    
    N3data_fname = 'N300_scenes_dst_global_' + exp_info['participant'] + '_' + exp_info['date']
    N3data_fname = os.path.join(datapath, N3data_fname)
    
    for trial_num, im, resp in zip(range(1,len(N3tList_dg)+1), N3tList_dg, response):
        N3stim_order.append({'trial_num': trial_num, 'im': im, 'resp': resp})
    
    N3trials = data.TrialHandler(N3stim_order, nReps=1, extraInfo=exp_info,
                                   method='sequential', originPath=datapath)

    # distraction stimuli parameters 
    bubble_height = 20
    bubble_width = 20
    bubble = visual.Circle(win,(bubble_width,bubble_height),lineColor='yellow',fillColor='gray')
    bubble.pos = [0,0]
    bug = visual.Circle(win,(2,2),lineColor='green',fillColor='green')
    bug.pos = [0,0]
    bug_jump = 1 #how far the bug can move each frame
    mov_amount = 1 #how far the user can influence the bug each frame
    old_mood = rnd.randint(2)
    stay = .995 #probability of bug staying in same mood per frame
    switch = 1.0-stay
        
    joy.quit()
    joy.init()
    buttons = 0
    xAxis = []
    yAxis = []
    keys = []
    
    p_port.setData(0) # make sure ports are initialized to 0
        
    load_message.draw()
    win.flip()
        
    bug.pos = [0,0]
    
    go_button = 0
    while go_button == 0:
        distract_message.draw()
        win.flip()
        go_button = joy.get_button(9)
        keys = event.getKeys(keyList=['space','escape'])
        if 'escape' in keys:
            m.setVisible(True)
            win.close()
            core.quit()
    
    # Wait for a spacebar press to start the trial, or escape to quit
    
    bubble.draw()
    bug.draw()
    win.flip()
    core.wait(1)

    i = 0
    
    # Run through the trials
    for trial in N3trials:
        
        bitmap = bitmaps[i]
        i += 1
        
        if 'good' in trial['im']:
            port_val = good_val
        elif 'bad' in trial['im']:
            port_val = bad_val
        # Set the images, set the orientation
    
        # Empty the keypresses list
        # Leave an 'escape' press in for immediate exit
        if 'escape' in keys:
            break
    
        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        stimFailTime = 0
        for frame in range(im_time):
            bitmap.draw()
            bubble.draw()
            old_pos = bug.pos
            bug.pos = (old_pos[0]+rnd.randint(-bug_jump,bug_jump+1),old_pos[1]+rnd.randint(-bug_jump,bug_jump+1))
            
            if old_mood == 0:
                probA = stay
                probB = switch
            elif old_mood == 1:
                probA = switch
                probB = stay
                
            mood = rnd.choice(2,1,p=[probA,probB])
            old_mood = mood
            
            if mood == 0:
                bug.fillColor = 'green'
                bug.lineColor = 'green'
            else:
                bug.fillColor = 'red'
                bug.lineColor = 'red'
            bug.draw()
            win.flip()
            
            if frame == 0:        
                p_port.setData(port_val)
                core.wait(.001)
                p_port.setData(0)
                
            keys = event.getKeys(keyList=['space','escape','up','down','left','right'])
            buttonA = joy.get_button(1)
            buttonB = joy.get_button(2)
            xAxis = joy.get_axis(0)*mov_amount
            yAxis = joy.get_axis(1)*mov_amount
            quit_buttons = joy.get_button(1),joy.get_button(9),joy.get_button(4),joy.get_button(5)
            if sum(quit_buttons)==4:
                win.close()
                core.quit()
            
            old_pos = bug.pos
            
            if mood == 0:
                if buttonA == 1 and buttonB == 0:
                    bug.pos = (old_pos[0]+xAxis,old_pos[1]-yAxis)
            elif mood == 1:
                if buttonA == 0 and buttonB == 1:
                    bug.pos = (old_pos[0]+xAxis,old_pos[1]-yAxis)
            else: bug.pos = old_pos
            
            # NEED TO DO SOME TESTING HERE TO ADD ALL FRAMES TO A CELL?
            if bug.overlaps(bubble) == False:
                stimFailTime += 1
            elif bug.overlaps(bubble) == True:
                stimFailTime += 0
            
            if 'escape' in keys:
                break
        
        blankFailTime = 0                
        for frame in range(blank_time):
    #            fix1.draw()
    #            fix2.draw()
            bubble.draw()
            old_pos = bug.pos
            bug.pos = (old_pos[0]+rnd.randint(-bug_jump,bug_jump+1),old_pos[1]+rnd.randint(-bug_jump,bug_jump+1))
            if old_mood == 0:
                probA = stay
                probB = switch
            elif old_mood == 1:
                probA = switch
                probB = stay
            mood = rnd.choice(2,1,p=[probA,probB])
            old_mood = mood
            
            if mood == 0:
                bug.fillColor = 'green'
                bug.lineColor = 'green'
            else:
                bug.fillColor = 'red'
                bug.lineColor = 'red'
                
            bug.draw()
            win.flip()
            
            keys = event.getKeys(keyList=['space','escape','up','down','left','right'])
            buttonA = joy.get_button(1)
            buttonB = joy.get_button(2)
            xAxis = joy.get_axis(0)*mov_amount
            yAxis = joy.get_axis(1)*mov_amount
            quit_buttons = joy.get_button(1),joy.get_button(9),joy.get_button(4),joy.get_button(5)
            if sum(quit_buttons)==4:
                win.close()
                core.quit()
            
            old_pos = bug.pos
            
            if mood == 0:
                if buttonA == 1 and buttonB == 0:
                    bug.pos = (old_pos[0]+xAxis,old_pos[1]-yAxis)
            elif mood == 1:
                if buttonA == 0 and buttonB == 1:
                    bug.pos = (old_pos[0]+xAxis,old_pos[1]-yAxis)
            else: bug.pos = old_pos
            
            if bug.overlaps(bubble) == False:
                blankFailTime += 1
            elif bug.overlaps(bubble) == True:
                blankFailTime += 0
            
            if 'escape' in keys:
                break
    
        # For the duration of trial time,
        # Listen for a response or escape press
        N3trials.addData('stimAcc', stimFailTime)
        N3trials.addData('blankAcc', blankFailTime)
        keys = event.getKeys(keyList=['space','escape'])
        
        
        if bug.overlaps(bubble) == True:
            trial['resp'] = 1
        else:
            trial['resp'] = 0
            
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
            bug.pos = (0,0)
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
        