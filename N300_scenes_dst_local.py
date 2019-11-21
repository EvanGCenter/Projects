# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 13:36:36 2018

@author: Evan
"""

def N300_dst_local():
   
    rnd.seed()
    
    standard_val = 8
    deviant_val = 9
    
    bgPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\bg\\'       #directory where images can be found
    cgPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\cg\\'
    fgPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\fg\\'
    hgPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\hg\\'
    mgPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\mg\\'
    ogPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\good\\og\\'

    gPaths = [bgPath,cgPath,fgPath,hgPath,mgPath,ogPath]

    bbPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\bb\\'
    cbPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\cb\\'
    fbPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\fb\\'
    hbPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\hb\\'
    mbPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\mb\\'
    obPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\N300_scenes\\bad\\ob\\'

    bPaths = [bbPath,cbPath,fbPath,hbPath,mbPath,obPath]
    
    bgList = [os.path.join(bgPath,f) for f in os.listdir(bgPath) if not f.startswith('.')]
    cgList = [os.path.join(cgPath,f) for f in os.listdir(cgPath) if not f.startswith('.')]
    fgList = [os.path.join(fgPath,f) for f in os.listdir(fgPath) if not f.startswith('.')]
    hgList = [os.path.join(hgPath,f) for f in os.listdir(hgPath) if not f.startswith('.')]
    mgList = [os.path.join(mgPath,f) for f in os.listdir(mgPath) if not f.startswith('.')]
    ogList = [os.path.join(ogPath,f) for f in os.listdir(ogPath) if not f.startswith('.')]

    bbList = [os.path.join(bbPath,f) for f in os.listdir(bbPath) if not f.startswith('.')]
    cbList = [os.path.join(cbPath,f) for f in os.listdir(cbPath) if not f.startswith('.')]
    fbList = [os.path.join(fbPath,f) for f in os.listdir(fbPath) if not f.startswith('.')]
    hbList = [os.path.join(hbPath,f) for f in os.listdir(hbPath) if not f.startswith('.')]
    mbList = [os.path.join(mbPath,f) for f in os.listdir(mbPath) if not f.startswith('.')]
    obList = [os.path.join(obPath,f) for f in os.listdir(obPath) if not f.startswith('.')]

    good_lists = [bgList,cgList,fgList,hgList,mgList,ogList]
    bad_lists = [bbList,cbList,fbList,hbList,mbList,obList]
    
    all_lists = good_lists+bad_lists
    devil_lists = []
    scene_lists = []
    
    # randomly select some deviants
    for i in range(len(all_lists)):
        devil_lists.append(list(rnd.choice(all_lists[i],len(all_lists[i])/5,replace=False)))
    
    # create fresh lists that don't include deviants
    for i in range(len(all_lists)):
        non_repeats = [item for item in all_lists[i] if item not in devil_lists[i]]
        scene_lists.append(non_repeats)
    
    # line up the lists properly    
    scene_lists.sort()
    devil_lists.sort()
    devil_lists = devil_lists*2
    devil_lists = devil_lists[6:18]
    
    # shuffle contents of each individual list
    for i in range(len(scene_lists)):
        rnd.shuffle(scene_lists[i])

    for i in range(len(devil_lists)):
        rnd.shuffle(devil_lists[i])

    dev1 = list(np.repeat(4,4))        # we want deviants to appear every 4 standards minimum
    dev2 = list(np.repeat(5,4))        # and every 6 standards max
    dev3 = list(np.repeat(6,4))        # there are 12 deviants per 48 standards
    devs = dev1+dev2+dev3
    
    for i in range(len(scene_lists)):
        rnd.shuffle(devs)
        j = 0
        for k in range(len(devil_lists[i])):
            j += devs[k]
            scene_lists[i].insert(j,devil_lists[i][k])
        
    rnd.shuffle(scene_lists)
            
    trial_scenes = []

    for sublist in scene_lists:
        for item in sublist:
            trial_scenes.append(item)
    
    scene_type = []
    
    for scene in trial_scenes:
        if type(scene) == str:
            scene_type.append('standard')
        else:
            scene_type.append('deviant')
    
    # scene stimulus stuff
    bitmaps = [visual.ImageStim(win, img, ori=0, pos=[0, 0]) for img in trial_scenes]
        
    response = list(np.repeat(None,n_standards_dst+n_deviants_dst+1))
    N3stim_order = []
    
    N3data_fname = 'N300_scenes_dst_local_' + exp_info['participant'] + '_' + exp_info['date']
    N3data_fname = os.path.join(datapath, N3data_fname)
    
    for trial_num, im, role, resp in zip(range(1,len(trial_scenes)+1), trial_scenes, scene_type, response):
        N3stim_order.append({'trial_num': trial_num, 'im': im, 'role': role, 'resp': resp})
    
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
        
        if  trial['role'] == 'standard':
            port_val = standard_val
        elif trial['role'] == 'deviant':
            port_val = deviant_val
    
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
            block_tot = np.divide(len(trial_scenes),break_time)
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
        