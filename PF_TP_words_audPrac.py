# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:39:57 2019

@author: APLab
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:36:17 2019

@author: APLab
"""

    # -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:00:30 2019

@author: Evan
"""

#==============================================
# Settings that we might want to tweak later on
#==============================================

def PF_TP_audio_prac():
    
    # Create a unique filename for the experiment data
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    data_fname = 'PF_TP_words_audio_prac' + exp_info['participant'] + '_' + exp_info['date']
    data_fname = os.path.join(datapath, data_fname)    
    
    rnd.seed()
    
    pygame.mixer.init()
    prac_sound = pygame.mixer.Sound("C:\Python27\Lib\site-packages\pygame\examples\data\house_lo.wav")
    
    words_list = ['one','two','three','four','five','six','seven','eight','nine','ten']
    pseudo_list = ['red','blue','green','magenta','periwinkle','gray','black','white','pink','brown']
    
    chosen_words = list(rnd.choice(words_list,5,replace=False))
    chosen_pseudo = list(rnd.choice(pseudo_list,5,replace=False))
    chosen_stan_words = [word for word in words_list if word not in chosen_words]
    chosen_stan_pseudo = [word for word in pseudo_list if word not in chosen_pseudo]
    durations = (300,700)
    standard = 500
    
    comp_list = chosen_words+chosen_pseudo
    stan_list = chosen_stan_pseudo+chosen_stan_words
    
    all_words = chosen_words+chosen_stan_words
    all_pseudo = chosen_pseudo+chosen_stan_pseudo
    
    combo_list = zip(comp_list,stan_list)
    rnd.shuffle(combo_list)
    comp_list,stan_list = zip(*combo_list)
    
    comp_id = list()
    stan_id = list()
    
    for c,d in zip(comp_list,stan_list):
        if c in words_list:
            comp_id.append('word')
        else: comp_id.append('pseudoword')
        if d in words_list:
            stan_id.append('word')
        else: stan_id.append('pseudoword')
        
    check = zip(comp_id,stan_id)
        
    t_order = list(np.repeat(0,len(stan_list)/2))+list(np.repeat(1,len(stan_list)/2))
    rnd.shuffle(t_order)
    
    comp_frames_p = list(np.repeat(durations,5))
    rnd.shuffle(comp_frames_p)
    stan_frames_p = list(np.repeat(standard,10))
    
    comp_frames = [int(d*.06) for d in comp_frames_p]
    stan_frames = [int(d*.06) for d in stan_frames_p]
    
    n_trials = len(comp_list)
#    n_trials = 10
    
    comp_words = [visual.TextStim(win,text=f, color='black', height=40) for f in comp_list]
    stan_words = [visual.TextStim(win,text=f, color='black', height=40) for f in stan_list]
    correct = visual.TextStim(win,text='correct', color='green', height=40)
    incorrect = visual.TextStim(win,text='incorrect', color='red', height=40)
    
    # Define the fixation
    fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((-5, 0), (5, 0)), pos=(0, 0))
    fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((0, -5), (0, 5)), pos=(0, 0))
    
    stim_order = []
    for trial_num, i_stan, i_comp, stan_id, comp_id, stan_frames, comp_frames, t_order in zip(range(len(stan_list)), stan_list, comp_list, stan_id, comp_id, stan_frames, comp_frames, t_order):
        stim_order.append({'trial_num': trial_num, 'stan': i_stan, 'comp': i_comp, 'stan_id': stan_id, 'comp_id': comp_id, 'stan_frames': stan_frames, 'comp_frames': comp_frames, 't_order': t_order})
    
    trials = data.TrialHandler(stim_order, nReps=1, extraInfo=exp_info,
                               method='sequential', originPath=datapath)
    
    
    # Initialize two clocks:
    #   - for image change time
    #   - for response time
    change_clock = core.Clock()
    rt_clock = core.Clock()
    
    # Display trial start text
#    start_message.draw()
#    win.flip()
    
    # Wait for a spacebar press to start the trial, or escape to quit
#    keys = event.waitKeys(keyList=['space', 'escape'])
    fix1.draw()
    fix2.draw()
    win.flip()
    core.wait(1)
    
    p = 0
    
    # Run through the trials
    for trial in trials:
        
    #    pygame.mixer.init(48000, -16, 1, 4096)
        
        # Set the clocks to 0
        change_clock.reset()
        rt_clock.reset()
    
        # Empty the keypresses list
        # Leave an 'escape' press in for immediate exit
        keys = []
        event.clearEvents()
        
        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        while len(keys) == 0 and rt_clock.getTime() < timelimit:
            if trial['t_order'] == 0: #comp -> stan
                for frame in range(trial['comp_frames']):
                    if frame == 0: pygame.mixer.Sound.play(prac_sound, loops = 0, maxtime=comp_frames_p[p]) #play comparison sound
                    fix1.draw()
                    fix2.draw()
                    win.flip()
    #            core.wait(comp_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
                
                for frame in range(blank_time):
                    fix1.draw()
                    fix2.draw()
                    win.flip()
                
                for frame in range(trial['stan_frames']):
                    if frame == 0: pygame.mixer.Sound.play(prac_sound, loops = 0, maxtime=stan_frames_p[p]) #play standard sound
                    fix1.draw()
                    fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
    
            elif trial['t_order'] == 1: #stan -> comp
                for frame in range(trial['stan_frames']):
                    if frame == 0: pygame.mixer.Sound.play(prac_sound, loops = 0, maxtime=stan_frames_p[p]) #play standard sound
                    fix1.draw()
                    fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
                
                for frame in range(blank_time):
                    fix1.draw()
                    fix2.draw()
                    win.flip()
                
                for frame in range(trial['comp_frames']):
                    if frame == 0: pygame.mixer.Sound.play(prac_sound, loops = 0, maxtime=comp_frames_p[p]) #play comparison sound
                    fix1.draw()
                    fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
    
            fix1.draw()
            fix2.draw()
            win.flip()
            rt_clock.reset()
    
    #        print comp_list[p]
    #        print stan_list[p]
    
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
            elif trial['t_order'] == 0:
                if 'left' in keys and trial['comp_frames'] >= trial['stan_frames']:
                    #comparison time first, comparison time longer, first image selected
                    acc = 1
                    cjl = 1
                elif 'right' in keys and trial['stan_frames'] > trial['comp_frames']:
                    #comparison time first, comparison time shorter, second image selected
                    acc = 1
                    cjl = 0
                elif 'left' in keys and trial['stan_frames'] > trial['comp_frames']:
                    #comparison time first, comparison time shorter, first image selected
                    acc = 0
                    cjl = 1
                elif 'right' in keys and trial['comp_frames'] >= trial['stan_frames']:
                    #comparison time first, comparison time longer, second image selected
                    acc = 0
                    cjl = 0
                    
            elif trial['t_order'] == 1:
                if 'left' in keys and trial['stan_frames'] >= trial['comp_frames']:
                    #comparison time second, comparison time shorter, first image selected
                    acc = 1
                    cjl = 0
                elif 'right' in keys and trial['comp_frames'] > trial['stan_frames']:
                    #comparison time second, comparison time longer, second image selected
                    acc = 1
                    cjl = 1
                elif 'left' in keys and trial['comp_frames'] > trial['stan_frames']:
                    #comparison time second, comparison time longer, first image selected
                    acc = 0
                    cjl = 0
                elif 'right' in keys and trial['stan_frames'] >= trial['comp_frames']:
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
        
        if acc == 1:
            correct.draw()
            win.flip()
            core.wait(1)
        elif acc == 0:
            incorrect.draw()
            win.flip()
            core.wait(2)
        fix1.draw()
        fix2.draw()
        win.flip()
        
        p += 1
    #    bs +=1
    #    pygame.mixer.quit()
    
        # Advance to the next trial after brief pause
        core.wait(rnd.uniform(.5,1.5))    
        
        if p == n_trials:
            section_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            win.flip()
            if keys != 0:
#                m.setVisible(True)
#                win.close()
                #core.quit()
                break
    
        elif p%break_time == 0:
    #        bs = 0
    #        pygame.mixer.quit()
    #        pygame.mixer.init(48000, -16, 1, 4096)
    #        comp_sounds = []
    #        stan_sounds = []
    #        comp_sounds = [pygame.mixer.Sound(os.path.join(legit_path,f)) for f in comp_list[p:p+break_time]]
    #        stan_sounds = [pygame.mixer.Sound(os.path.join(pseudo_path,f)) for f in stan_list[p:p+break_time]]
            trials.saveAsWideText(data_fname + '.csv', delim=',', appendFile = False)
            block_num = np.divide(p,break_time)
            block_tot = np.divide(n_trials,break_time)
            block_missive = 'You have completed block ' + str(block_num) + ' out of ' + str(block_tot) + '. ' + 'Please take a short break and press the spacebar when you are ready to continue.'
            block_message = visual.TextStim(win, text=block_missive, color='black', height=20)        
            block_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            fix1.draw()
            fix2.draw()
            win.flip()
            core.wait(1)
            
    
    #======================
    # End of the experiment
    #======================
    
    # Save all data to a file
    trials.saveAsWideText(data_fname + '.csv', delim=',', appendFile = False)