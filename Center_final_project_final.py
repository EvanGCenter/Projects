# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 14:22:14 2018

@author: Evan
"""

import numpy as np
import numpy.random as rnd
from matplotlib import pyplot
from psychopy import visual, event, core # the visualizations are totally worth it
from scipy import stats

#np.random.seed(1738)

class Connection(object):
    def __init__(self, sender = None, recipient = None, weight = 0.0, delta_weight = 0.0):
        """Class of connection objects with sender, recipient, and weight"""
        self.sender = sender
        self.recipient = recipient
        self.weight = weight
        self.delta_weight = delta_weight
        
class Unit(object):
    def __init__(self, excite_output = 0.0, inhibi_output = 0.0, net_state = 0.0, pos_input = 0.0, 
                 neg_input = 0.0, threshold = 1.0, refract = False, incoming = None, outgoing = None,
                 error = 0.0, sensitivity = 1.0):
        """Class of unit objects"""        
        self.excite_output = excite_output #sending excitatory signal
        self.inhibi_output = inhibi_output #sending inhibitory signal
        self.net_state = net_state #value to calculate net of inputs
        self.pos_input = pos_input #stuff to make part 2 easier with my neurons
        self.neg_input = neg_input
        self.threshold = threshold #activation threshold
        self.refract = refract #boolean for refractory period (one step buffer)
        self.incoming = incoming #list of incoming connections
        self.outgoing = outgoing #list of outgoing connections
        if self.incoming == None: #fuckery to get the empty lists to play nice
            self.incoming = []
        if self.outgoing == None:
            self.outgoing = []
        self.error = error
        self.sensitivity = sensitivity
        
    def add_connection(self, connection):
        """Add connection objects to incoming/outgoing list unit object attributes"""
        self.incoming.append(connection)
        connection.sender.outgoing.append(connection)
        
    def get_input(self):
        for i in range(len(self.incoming)):
            self.net_state += (self.incoming[i].sender.excite_output+self.incoming[i].sender.inhibi_output)*self.incoming[i].weight
        #print "net state: ",self.net_state
        
    def update_activation(self):
        # update activations according to sigmoid transfer function
        t0 = self.excite_output
        if self.net_state != 0:
            self.excite_output = 1.0/(1.0 + np.exp(-self.net_state))
        t1 = self.excite_output
        return t0,t1
#        if t1 > t0:
#            self.sensitivity += self.sensitivity*self.excite_output
#        else:
#            self.sensitivity -= self.sensitivity*self.excite_output
        #print "activation: ",self.excite_output
        
    def reset(self): 
    # handy reset method for units
        self.net_state = 0.0
        self.excite_output = 0.0
        self.inhibi_output = 0.0
        self.pos_input = 0.0
        self.neg_input = 0.0
        self.refract = False
        self.error = 0.0
        

#==============================================================================


class LayeredNetwork(object):
    def __init__(self, n_inputs = 0, n_hidden = 0, n_outputs = 0, bias_node = 0, CM = 0, layer_i = [], 
                 layer_h = [], layer_o = [], units = [], connections = [], global_error = []):
        self.n_inputs = n_inputs**2
        self.n_hidden = n_hidden**2
        self.bias_node = bias_node
        self.n_outputs = n_outputs**2
        self.CM = CM
        self.layer_i = layer_i
        self.layer_h = layer_h
        self.layer_o = layer_o
        self.units = units
        self.connections = connections
        self.global_error = global_error
        
        # create the units
        for node in range(self.n_inputs):
            self.layer_i.append(Unit())
        for node in range(self.n_hidden):
            self.layer_h.append(Unit())
        for node in range(self.n_outputs):
            self.layer_o.append(Unit())
        
        self.units = self.layer_i+self.layer_h+self.layer_o
        
        # if desired, make a bias node that hides in its own secret space,
        # talks to all the output units with activation of 1, listens to no one
        if self.bias_node != 0:
            self.bias_node = Unit(1.0)
            for unit_o in self.layer_o:
                self.connections.append(Connection(self.bias_node,unit_o))
        
        
#       connect input layer neighbors
#        for unit_i in range(len(self.layer_i)):
#                for i in range(len(self.layer_i)):
#                    if abs(unit_i-i) == 1:
#                        if unit_i%int(np.sqrt(self.n_inputs)) == 0 and unit_i-i == 1:
#                            pass
##                            self.connections.append(Connection(self.layer_i[unit_i],self.layer_i[i],-0.5))
#                        elif unit_i%int(np.sqrt(self.n_inputs)) == int(np.sqrt(self.n_inputs))-1 and unit_i-i == -1:
#                            pass
##                            self.connections.append(Connection(self.layer_i[unit_i],self.layer_i[i],-0.5))
#                        else:
#                            self.connections.append(Connection(self.layer_i[unit_i],self.layer_i[i],.5))
#                            
#                    elif abs(unit_i-i) == int(np.sqrt(self.n_inputs)):
#                        self.connections.append(Connection(self.layer_i[unit_i],self.layer_i[i],.5))
##                    else: 
##                        self.connections.append(Connection(self.layer_i[unit_i],self.layer_i[i],-0.5))


#         connect every unit to every unit in the layer above, step 1: create connections
#         all input to all output method
#        if n_hidden > 0:
#            for unit_h in self.layer_h:
#                for unit_i in self.layer_i:
#                    self.connections.append(Connection(unit_i,unit_h,rnd.random()))
#                for unit_o in self.layer_o:
#                    self.connections.append(Connection(unit_h,unit_o,rnd.random()))
#        else:
#            for unit_i in self.layer_i:
#                for unit_o in self.layer_o:
#                    self.connections.append(Connection(unit_i,unit_o,rnd.random()))

#         connect every unit to every unit in the layer above, step 1: create connections
#         nearby neighbor method
        if n_hidden > 0:
            budz = [1,1,1,0,0,1,1,1,0,0,1,1,1] + [0]*12
            for unit_h in range(len(self.layer_h)):
                for unit_i in range(len(self.layer_i)):
                    if budz[unit_i] == 1:
                        self.connections.append(Connection(self.layer_i[unit_i],self.layer_h[unit_h],rnd.random()))
                for unit_o in range(len(self.layer_o)):
                    if budz[unit_o] == 1:
                        self.connections.append(Connection(self.layer_h[unit_h],self.layer_o[unit_o],rnd.random()))
                if  unit_h%int(np.sqrt(self.n_hidden)) == int(np.sqrt(self.n_hidden))-1:
                    budz = [0]*int(np.sqrt(self.n_hidden)) + budz
                else:
                    budz = [0] + budz
        else:
            for i in range(len(self.layer_i)):
                for o in range(len(self.layer_o)):
                    if i == o:
                        self.connections.append(Connection(self.layer_i[i],self.layer_o[o],rnd.random()))
                    
        # connect units, step 2: add connection Unit method   
        for connect_i in range(len(self.connections)):
            self.connections[connect_i].recipient.add_connection(self.connections[connect_i])
            # assign a random weight to each connection
            #self.connections[connect_i].weight = rnd.rand(1)[0]
            #self.connections[connect_i].weight = 1.0
            
    # train it
    def train(self, training_set, desired_output, rep_cap = 9999, learning_rate = .97, momentum = .03, criteria = 5):
        
        reps = 0 # init counter
        # while global error hasn't met criteria OR an impatience limit hasn't been met
        self.global_error.append(1.0)
        while self.global_error[-1] > 10**(-criteria):
            
            # randomize learn order?
            k = range(len(training_set))
            rnd.shuffle(k)
            
            training_set = [training_set[i] for i in k]
            desired_output = [desired_output[i] for i in k]
            
            # add 1 to counter for every loop
            reps += 1
#            print reps
            
            # break the loop if impatience limit exceeded
            if reps > rep_cap:
                print 'impatience limit reached'
                break
            
            # initialize delta weight state first
            for connect in self.connections:
                connect.delta_weight = 0
                
            # for each pattern in the training set
            for pattern in range(len(training_set)):
                
                # do a forward prop run and calculate errors
                self.run(training_set[pattern],desired_output[pattern])
                self.reset_sensitivity()
                
                # add up delta weights based on error for each connection
                for connect in self.connections:
                    connect.delta_weight += learning_rate*connect.recipient.error*connect.sender.excite_output + momentum*connect.delta_weight

            # then actually change the delta weights we've stored      
            for connect in self.connections:
                if connect.recipient in self.layer_i:
                    pass
                else:                
                    connect.weight += connect.delta_weight
                
            # calculate and append global error for each iteration
            error_o,error_h = 0.0,0.0
            if len(self.layer_h) > 0:
                for unit in self.layer_o:
                    error_o += np.square(unit.error)
                for unit in self.layer_h:
                    error_h += np.square(unit.error)
                error_tot = error_o + error_h
                self.global_error.append(error_tot)
            else:
                for unit in self.layer_o:
                    error_o += np.square(unit.error)
                self.global_error.append(error_o)
            print reps,self.global_error[-1]
        
        print 'n epochs required: ',reps
        print 'global error: ',self.global_error[-1]
        
    def run(self, test_pattern, target_pattern, printy = 0):
        # start each run with fresh nodes
        self.reset_nodes()
        
        # set initial activations to levels of test patterns
        for i in range(len(test_pattern)):
            self.layer_i[i].excite_output = test_pattern[i]*self.layer_i[i].sensitivity
        
        # give signal to input layer neighbors
#        for i in range(len(test_pattern)):
#            if test_pattern[i] == 1.0:
#                for c in range(len(self.layer_i[i].outgoing)):
#                    if self.layer_i[i].outgoing[c].recipient in self.layer_i:
#                        self.layer_i[i].outgoing[c].recipient.excite_output = self.layer_i[i].excite_output*self.layer_i[i].outgoing[c].weight
                
                
#            self.layer_i[i].net_state = test_pattern[i]
#            self.layer_i[i].update_activation()
            
#        for i in range(len(test_pattern)):
#            self.layer_i[i].get_input()
#            
#        for i in range(len(test_pattern)):
#            self.layer_i[i].update_activation()
        
        # if there's a hidden layer            
        if len(self.layer_h) > 0:            
            # update the hidden layer and output layer based on input layer activations           
            for unit in self.layer_h:
                unit.get_input()
            for unit in self.layer_h:
                unit.update_activation()
            for unit in self.layer_o:
                unit.get_input()
            for unit in self.layer_o:
                unit.update_activation()
            
            # calculate error at output layer
            for u in range(len(self.layer_o)):
                self.layer_o[u].error = (target_pattern[u]-self.layer_o[u].excite_output)*self.layer_o[u].excite_output*(1-self.layer_o[u].excite_output)
                
            # calculate error/blame assignment at hidden layer
            for unit_h in self.layer_h:
                for connect in unit_h.outgoing:
                    unit_h.error += (connect.recipient.error*connect.weight)*unit_h.excite_output*(1-unit_h.excite_output)
        
            # calculate error/blame assignment at hidden layer, convolution nn method
#            for unit_h in self.layer_h:
#                for connect in unit_h.outgoing:
#                    for unit_hx in self.layer_h:    
#                        unit_hx.error += (connect.recipient.error*connect.weight)*unit_h.excite_output*(1-unit_h.excite_output)
                    
        
        # if no hidden layer    
        else: 
            # update activations for output from input layer
            for unit in self.layer_o:
                unit.get_input()
            for unit in self.layer_o:
                unit.update_activation()
            
            # calculate error at output layer
            for u in range(len(self.layer_o)):
                self.layer_o[u].error = (target_pattern[u]-self.layer_o[u].excite_output)*self.layer_o[u].excite_output*(1-self.layer_o[u].excite_output)
        
        limen = .2
        up_sense = .8
        down_sense = .444        
        
        if self.CM == 1:
            # alter input sensitivity for input neurons corresponding to active outputs, indirect method
            for i in range(len(self.layer_o)):
#                if self.layer_o[i].excite_output > limen:          
                self.layer_i[i].sensitivity = np.exp(self.layer_o[i].excite_output) - 0.45
#                else:
#                    self.layer_i[i].sensitivity = 1-self.layer_i[i].excite_output
        
        else:
            # alter sensitivity direct method
            case = []
            for unit_o in self.layer_o:
                case.append(unit_o.excite_output)
            avg = np.mean(case)
        
            for unit_o in self.layer_o:
                for connect_o in unit_o.incoming:
                    for unit_i in self.layer_i:
                        for connect_i in unit_i.outgoing:
                            if connect_o.sender is connect_i.recipient:
#                                if unit_o.excite_output > limen:
                                unit_i.sensitivity += (np.exp(unit_o.excite_output)-.75)-avg
#                                else:
#                                    unit_i.sensitivity -= unit_i.sensitivity*down_sense
        
        # optional arguement to print activations at end of run        
        if printy != 0:
            for i in range(len(self.layer_o)):
                print self.layer_o[i].excite_output
            
    def reset_nodes(self):
        # method to iterate through units in the network
        # and reset state of each unit
        for i in range(len(self.units)):
            self.units[i].net_state = 0.0
            self.units[i].excite_output = 0.0
            self.units[i].inhibi_output = 0.0
            self.units[i].pos_input = 0.0
            self.units[i].neg_input = 0.0
            self.units[i].refract = False
            self.units[i].error = 0.0
            
    def reset_weights(self):
        # method to reset all network weights
        for i in range(len(self.connections)):
            self.connections[i].weight = rnd.rand(1)[0]
            self.connections[i].delta_weight = 0.0
            
    def reset_sensitivity(self):
        for unit in self.units:
            unit.sensitivity = 1.0
        
    def display_connections(self,option=0):
        # display the connection weights
        #start with a 2-D array of zeros of length n_nodes by n_nodes
        if len(self.layer_h)>0:
            array = np.zeros(len(self.connections))
            #initialize a counter to help retrieve skipped values caused by unit to same unit connections being artificially supplied
            skip = 0
            #iterate through the array
            for i in range(len(self.connections)):
                #get the weight
                array[i] = self.connections[i].weight
            #reshape the 2-D array into an n_nodes by n_nodes array
            web1 = array[0:((self.n_inputs*self.n_hidden))]
            web2 = array[(self.n_inputs*self.n_hidden)-1:-1]
            web1 = np.reshape(web1,(self.n_inputs,self.n_hidden))
            web2 = np.reshape(web2,(self.n_hidden,self.n_outputs))
            
            # plot the weights without interpolation
            # for networks with hidden layer, option to see input by hidden connections
            # or hidden by output connections
            if option == 0:
                return pyplot.imshow(web1, cmap = 'Greys', interpolation = 'none')
            else: 
                return pyplot.imshow(web2, cmap = 'Greys', interpolation = 'none')
                
        else:
            array = np.zeros(len(self.connections))
            #initialize a counter to help retrieve skipped values caused by unit to same unit connections being artificially supplied
            skip = 0
            #iterate through the array
            for i in range(len(self.connections)):
                #get the weight
                array[i] = self.connections[i].weight
            #reshape the 2-D array into an n_nodes by n_nodes array and plot
            web1 = array[0:((self.n_inputs*self.n_outputs))]
            web1 = np.reshape(web1,(self.n_inputs,self.n_outputs))
            return pyplot.imshow(web1, cmap = 'Greys', interpolation = 'none')
        
    def display_activations(self, stim_set = [], clean = 0, reps = 1, sensi = 0):
        # method for visualizing final activation states of a given input
        # or set of inputs
    
        if sensi == 1:
            self.CM = 1
        else:
            self.CM = 0
    
        # make a new little screen and arrange some node placeholders in a way
        # that hopefully doesn't suck
        scrn_size = [800,600]
        win = visual.Window(scrn_size, color='gray', units='pix')
        len_o = int(np.sqrt(self.n_outputs))
        node_size = scrn_size[0]/(len_o*4)
        posx = range(0,scrn_size[0],scrn_size[0]/(len_o))
        posx = list(stats.zscore(posx)*(scrn_size[0]/4))
        posy = range(0,scrn_size[1],scrn_size[1]/(len_o))
        posy = list(stats.zscore(posy)*(scrn_size[1]/4))
        posy = list(reversed(posy))
        
        if reps > 1:
            stim_set = [stim_set for x in xrange(reps)]
            
        # make it work for single patterns or sets of patterns
        if len(np.shape(stim_set)) > 1:
            rows = np.shape(stim_set)[0]
        else:
            rows = 1
    
    
        for i in range(rows):
            slot = self.n_outputs*[0]
            
            if clean != 0:
                self.reset_sensitivity()
            
            if stim_set:
                if rows > 1:
                    self.run(stim_set[i],slot)
                else:
                    self.run(stim_set,slot)
            
            
            # find the output unit with the largest activation
            box = []
            for unit in range(len(self.layer_o)):
                box.append(self.layer_o[unit].excite_output)
#                if self.layer_o[unit].excite_output > .05:
#                    print unit,self.layer_o[unit].excite_output
            winner = max(box)
            print 'winner:',winner
            
            # create and place the nodes
            pic_nodes = []
            for unit in range(len_o):
                for place in range(len_o):
                    pic_nodes.append(visual.Circle(win,node_size,pos=(posx[place],posy[unit])))
            
            # fill the nodes by degree of activation
            # winner will be in green and competitors will be in blue
            # no activation in gray
            # brightness of hue indicates strength of activation        
            # then finally draw the nodes
            for unit in range(len(pic_nodes)):
                if self.layer_o[unit].excite_output == winner:
                    pic_nodes[unit].fillColor=[0,self.layer_o[unit].excite_output,0]
                else:
                    pic_nodes[unit].fillColor=[0,0,self.layer_o[unit].excite_output]
            
                pic_nodes[unit].draw()
            
            # flip the nodes to the screen for each pattern
            if rows < 2:
                win.flip()
                keys = event.waitKeys(keyList=['space', 'enter', 'escape'])
                win.close()            
            
            elif i != len(stim_set)-1:
                win.flip()
                keys = event.waitKeys(keyList=['space', 'enter', 'escape'])
                win.flip()
                core.wait(.3)
            
            else:
                win.flip()
                keys = event.waitKeys(keyList=['space', 'enter', 'escape'])
                win.close()
                

targets = .811
distractors = .405
ignores = .001


area = 25
blank = [0.0]*area
stimz = [[] for x in xrange(area)]

for i in range(area):
    stimz[i][:] = blank

for i in range(area):
    for j in range(area):
        if i == j:
            stimz[i][j] = 1.0
            
goalz = [[] for x in xrange(area)]

for i in range(area):
    goalz[i][:] = blank

for i in range(area):
    for j in range(area):
        if i == j:
            goalz[i][j] = targets
        else:
            goalz[i][j] = ignores
            
for unit_i in range(area):
    for i in range(area):
        if abs(unit_i-i) == 1:
            if unit_i%int(np.sqrt(area)) == 0 and unit_i-i == 1:
                pass
            elif unit_i%int(np.sqrt(area)) == int(np.sqrt(area))-1 and unit_i-i == -1:
                pass
            else:
                goalz[unit_i][i] = distractors
                
        elif abs(unit_i-i) == int(np.sqrt(area)):
            goalz[unit_i][i] = distractors

# what is learned first is learned better so let's bias it towards the center of the display and spiral out
#learn_order = [12,13,17,11,7,8,18,16,6,14,22,10,2,9,19,23,21,15,5,1,3,4,24,20,0]
#propr_order = [24,19,12,20,21,18,8,4,5,13,11,3,0,1,9,17,7,2,6,14,23,16,10,15,22]
#
#stimz = [stimz[i] for i in learn_order]
#goalz = [goalz[i] for i in learn_order]

#squarey_boi = LayeredNetwork(int(np.sqrt(area)),3,int(np.sqrt(area)),1)
#
#squarey_boi.train(stimz,goalz,99999,.1,.2,5)
##squarey_boi.train(stimz,goalz,1800,.7,.3,6)
#
##stimz = [stimz[i] for i in propr_order]
##goalz = [goalz[i] for i in propr_order]
#
## check to make sure it got all the mappings, resetting sensitivity each time
#squarey_boi.display_activations(stimz,1)
#
#squarey_boi.reset_sensitivity()
#
#num = 21 # pick a node between 0 and 25
## repeat for five runs to see the signal grow stronger and the candidates show up
#squarey_boi.display_activations(stimz[num],0,5,1)
#
#squarey_boi.reset_sensitivity()
#
## watch it do better when a candidate is subsequently picked as a target
#squarey_boi.display_activations(stimz[8],0,5,1)
#squarey_boi.display_activations(stimz[3],0,5,1)
#
#squarey_boi.reset_sensitivity()
#
## watch it make a mistake when something far away comes after, then recover
#squarey_boi.display_activations(stimz[24],0,5,1)
#squarey_boi.display_activations(stimz[11],0,5,1)
#
#
## transfer! 
#stimz[6][18] = 1.0
#squarey_boi.display_activations(stimz[6],0,5,1)
#
