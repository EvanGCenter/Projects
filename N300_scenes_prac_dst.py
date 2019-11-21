# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 12:25:23 2018

@author: Evan
"""
def prac_dst():
    
    rnd.seed()
    
    pracPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\prac_mids\\'
    
    pracList = [os.path.join(pracPath,f) for f in os.listdir(pracPath) if not f.startswith('.')]
    rnd.shuffle(pracList)
    
    prac_message = visual.TextStim(win,
                                    text="This is a practice block. Use the joystick to keep the bug in the bubble. While the bug is green, hold down the green 'A' button to influence him. While the bug is red, hold down the red 'B' button to influence him. Press 'start' to begin.",
                                    color='black', height=20)
    
    done_message = visual.TextStim(win,
                                    text="You have reached the end of this practice block. Press start to continue.",
                                    color='black', height=20)
    
    bitmap = visual.ImageStim(win, size=None)
    
    scrsize = (1280,1024)                 # screen size in pixels
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
    
    ##### start prac - distraction #####
    
    load_message.draw()
    win.flip()
    bitmaps = [visual.ImageStim(win, img, ori=0, pos=[0,0]) for img in pracList]
    
    while buttons == 0:
        prac_message.draw()
        win.flip()
        buttons = joy.get_button(9)
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
    
    for bitmap in bitmaps:
            
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
            
            if 'escape' in keys:
                break
        
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
            
            if 'escape' in keys:
                break
                
    block_button = 0    
    while block_button == 0:     
        done_message.draw()
        win.flip()
        block_button = joy.get_button(9)
        keys = event.getKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            break
    win.flip()
    core.wait(.5)
    
    
