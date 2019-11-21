    # -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:00:30 2019

@author: Evan
"""

#==============================================
# Settings that we might want to tweak later on
#==============================================

def PF_TP_visual():
    
    # Create a unique filename for the experiment data
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    data_fname = 'PF_TP_words_visual' + exp_info['participant'] + '_' + exp_info['date']
    data_fname = os.path.join(datapath, data_fname)    
    
    rnd.seed()
    
    words_list = [f for f in os.listdir(legit_path) if not f.startswith('.')]
    pseudo_list = [f for f in os.listdir(pseudo_path) if not f.startswith('.')]
    
    chosen_words = list()
    chosen_pseudo = list()
    chosen_stan_words = list()
    chosen_stan_pseudo = list()
    durations = range(300,701,50)
    standard = 500
    
    for dur in durations:
        chosen_words.extend(rnd.choice([w for w in words_list if w.endswith(str(dur)+'.wav') and w.replace(w[-8:],'') not in [ws.replace(ws[-8:],'') for ws in chosen_words]],9,replace=False))
        chosen_pseudo.extend(rnd.choice([p for p in pseudo_list if p.endswith(str(dur)+'.wav') and p.replace(w[-8:],'') not in [ps.replace(ps[-8:],'') for ps in chosen_pseudo]],9,replace=False))
    
    chosen_stan_words.extend(rnd.choice([w for w in words_list if w.endswith('500.wav') and w.replace(w[-8:],'') not in [ws.replace(ws[-8:],'') for ws in chosen_words]],81,replace=False))
    chosen_stan_pseudo.extend(rnd.choice([p for p in pseudo_list if p.endswith('500.wav') and p.replace(w[-8:],'') not in [ps.replace(ps[-8:],'') for ps in chosen_pseudo]],81,replace=False))
    
    #for word in chosen_words:
    #    for dur in durations:
    #        if word.replace(word[-8:],'')+str(dur)+'.wav' in chosen_stan_words:
    #            print 'word error'
    
    rnd.shuffle(chosen_words)
    rnd.shuffle(chosen_pseudo)
    rnd.shuffle(chosen_stan_words)
    rnd.shuffle(chosen_stan_pseudo)    
    
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
    
    #i=0
    #for snd in comp_sounds[0:10]:
    #    pygame.mixer.Sound.play(snd)
    #    print i,comp_list[i]
    #    i+=1
    #    core.wait(1)
    #    
    #i=0
    #for snd in stan_sounds[0:10]:
    #    pygame.mixer.Sound.play(snd)
    #    print i,stan_list[i]
    #    i+=1
    #    core.wait(1)
    
    comp_frames = [int((int(dur[-7:-4]))*.06) for dur in comp_list]
    stan_frames = [int((int(dur[-7:-4]))*.06) for dur in stan_list]
    
    n_trials = len(comp_list)
#    n_trials = 10
    
    comp_words = [visual.TextStim(win,text=f[0:-8], color='black', height=40) for f in comp_list]
    stan_words = [visual.TextStim(win,text=f[0:-8], color='black', height=40) for f in stan_list]
    
    # Define trial start text
    
    
    # Define bitmap stimulus (contents can still change)
    #bitmap1 = visual.ImageStim(win, size=None)
    #bitmap2 = visual.ImageStim(win, size=None)
    
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
    #bs = 0
    
    #c = 0
    #for word in comp_words:
    #    comp_words[c].draw()
    #    win.flip()
    #    print comp_list[c]
    #    core.wait(.5)
    #    c+=1
    #    
    #s = 0
    #for word in stan_words:
    #    stan_words[s].draw()
    #    win.flip()
    #    print stan_list[s]
    #    core.wait(.5)
    #    s+=1
    
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
                    comp_words[p].draw() #play comparison sound
    #                fix1.draw()
    #                fix2.draw()
                    win.flip()
    #            core.wait(comp_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
                
                for frame in range(blank_time):
                    fix1.draw()
                    fix2.draw()
                    win.flip()
                
                for frame in range(trial['stan_frames']):
                    stan_words[p].draw() #play standard sound
    #                fix1.draw()
    #                fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
    
            elif trial['t_order'] == 1: #stan -> comp
                for frame in range(trial['stan_frames']):
                    stan_words[p].draw() #play standard sound
    #                fix1.draw()
    #                fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
                
                for frame in range(blank_time):
                    fix1.draw()
                    fix2.draw()
                    win.flip()
                
                for frame in range(trial['comp_frames']):
                    comp_words[p].draw() #play comparison sound
    #                fix1.draw()
    #                fix2.draw()
                    win.flip()
    #            core.wait(stan_frames[p])
    #            core.wait(int(trial['comp_id'][-7:-4])/1000.0)
    
            fix1.draw()
            fix2.draw()
            win.flip()
            rt_clock.reset()
    
#            print comp_list[p]
#            print stan_list[p]
    
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