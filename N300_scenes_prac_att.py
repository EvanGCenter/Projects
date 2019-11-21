# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 12:25:23 2018

@author: Evan
"""
def prac_att():

    rnd.seed()
    
    pracPath = 'C:\\Users\\rift\\Desktop\\Evan\\scenes\\prac_mids\\'
    
    pracList = [os.path.join(pracPath,f) for f in os.listdir(pracPath) if not f.startswith('.')]
    rnd.shuffle(pracList)
    
    prac_message = visual.TextStim(win,
                                    text="This is a practice block. Please keep your eyes on the fixation cross at the center of the screen at all times. Meanwhile, try to pay attention to each scene that appears. If you think the scene is a bad exemplar of its category, press the red 'B' button. Press 'start' to begin.",
                                    color='black', height=20)
    done_message = visual.TextStim(win,
                                    text="You have reached the end of this practice block. Press start to continue.",
                                    color='black', height=20)
    
    fix1 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((-5, 0), (5, 0)), pos=(0, 0))
    fix2 = visual.ShapeStim(win, units='pix', lineWidth=2, lineColor='yellow', fillColor='yellow', vertices=((0, -5), (0, 5)), pos=(0, 0))

    bitmap = visual.ImageStim(win, size=None)
    
    scrsize = (1280,1024)                 # screen size in pixels
    
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
    win.flip()
    core.wait(1)
    
    for bitmap in bitmaps:
            
        for frame in range(im_time):
           
            bitmap.draw()
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
    
    
