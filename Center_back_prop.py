# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 14:22:14 2018

@author: Evan
"""

import numpy as np
import numpy.random as rnd
from matplotlib import pyplot, figure
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
                 error = 0.0):
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
        
    def add_connection(self, connection):
        """Add connection objects to incoming/outgoing list unit object attributes"""
        self.incoming.append(connection)
        connection.sender.outgoing.append(connection)
        
    def get_input(self):
        # sum inputs over all connections and units
        signals = []
        for i in range(len(self.incoming)):
            self.net_state += (self.incoming[i].sender.excite_output+self.incoming[i].sender.inhibi_output)*self.incoming[i].weight
        #print "net state: ",self.net_state
        
    def update_activation(self):
        # update activations according to sigmoid transfer function
        t0 = self.excite_output
        #if self.net_state != 0:
        self.excite_output = 1.0/(1.0 + np.exp(-self.net_state))
        t1 = self.excite_output
        return t0,t1
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
# # create a network object class comprised of units and their connections
# # *****WARNING***** you'll have to uncomment networks one at a time to avoid
# # newly created ones inheriting all the units and connections of existing ones
# # for some stupid ass reason
# # [unless your version of python isn't as infuriating as mine]
# 
# # I've tried to divide up relevant networks with #------- sandwhiches to help
#==============================================================================

class LayeredNetwork(object):
    def __init__(self, n_inputs = 0, n_hidden = 0, n_outputs = 0, bias_node = 0, layer_i = [], 
                 layer_h = [], layer_o = [], units = [], connections = [], global_error = []):
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.bias_node = bias_node
        self.n_outputs = n_outputs
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
        
        # connect every unit to every unit in the layer above, step 1: create connections
        if n_hidden > 0:
            for unit_h in self.layer_h:
                for unit_i in self.layer_i:
                    self.connections.append(Connection(unit_i,unit_h))
                for unit_o in self.layer_o:
                    self.connections.append(Connection(unit_h,unit_o))
        else:
            for unit_i in self.layer_i:
                for unit_o in self.layer_o:
                    self.connections.append(Connection(unit_i,unit_o))
                    
        # connect units, step 2: add connection Unit method   
        for connect_i in range(len(self.connections)):
            self.connections[connect_i].recipient.add_connection(self.connections[connect_i])
            # assign a random weight to each connection
            self.connections[connect_i].weight = rnd.rand(1)[0]

    # train it
    def train(self, training_set, desired_output, rep_cap = 9000, learning_rate = .3, momentum = .7, display = 0):
        
        reps = 0 # init counter
        # while global error hasn't met criteria OR an impatience limit hasn't been met
        self.global_error.append(10000.0)
        while self.global_error[-1] > .00001:
            
            # add 1 to counter for every loop
            reps += 1
            
            # break the loop if impatience limit exceeded
            if reps > rep_cap:
                print 'rule 1'
                break
            
            # initialize delta weight state first
            for connect in self.connections:
                connect.delta_weight = 0
                
            # for each pattern in the training set
            for pattern in range(len(training_set)):
                
                # do a forward prop run and calculate errors            
                self.run(training_set[pattern],desired_output[pattern])
                
                # add up delta weights based on error for each connection
                for connect in self.connections:
                    connect.delta_weight += learning_rate*connect.recipient.error*connect.sender.excite_output + momentum*connect.delta_weight

            # then actually change the delta weights we've stored      
            for connect in self.connections:        
                connect.weight += connect.delta_weight
                
            # calculate and append global error for each iteration
            error_o,error_h = 0,0
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
        
        print 'n epochs required: ',reps
        print 'global error: ',self.global_error[-1]
        
    def run(self, test_pattern, target_pattern, printy = 0):
        # start each run with fresh nodes
        self.reset_nodes()
        
        # set initial activations to levels of test patterns
        for i in range(len(test_pattern)):
            self.layer_i[i].excite_output = test_pattern[i]
            #self.layer_i[i].net_state = test_pattern[i]
            #self.layer_i[i].update_activation()
        
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
                for unit_o in self.layer_o:
                    for c in range(len(unit_o.incoming)):
                        unit_h.error += (unit_o.error*unit_o.incoming[c].weight)*unit_h.excite_output*(1-unit_h.excite_output)
        
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
        
    def display_activations(self, stim_set = []):
        # method for visualizing final activation states of a given input
        # or set of inputs
    
        # make a new little screen and arrange some node placeholders in a way
        # that hopefully doesn't suck
        scrn_size = [800,600]
        win = visual.Window(scrn_size, color='gray', units='pix')
        pic_nodes = []
        len_o = len(self.layer_o)
        node_size = scrn_size[0]/(len_o*4)
        posx = range(0,scrn_size[0],scrn_size[0]/(len_o))
        posx = list(stats.zscore(posx)*(scrn_size[0]/4))
        
        # make it work for single patterns or sets of patterns
        if len(np.shape(stim_set)) > 1:
            rows = np.shape(stim_set)[0]
        else:
            rows = 1
        
        for i in range(rows):
            slot = self.n_outputs*[0]
            
            if rows > 1:
                self.run(stim_set[i],slot)
            else:
                self.run(stim_set,slot)
            
            # find the output unit with the largest activation
            box = []
            for unit in range(len(self.layer_o)):
                box.append(self.layer_o[unit].excite_output)
            winner = max(box)
            
            # fill the nodes by degree of activation
            # winner will be in green and competitors will be in blue
            # no activation in gray
            # brightness of hue indicates strength of activation
            for unit in range(len(self.layer_o)):
                if self.layer_o[unit].excite_output == winner:
                    pic_nodes.append(visual.Circle(win,node_size,fillColor=[0,self.layer_o[unit].excite_output,0],pos=(posx[unit],0)))
                else:
                    pic_nodes.append(visual.Circle(win,node_size,fillColor=[0,0,self.layer_o[unit].excite_output],pos=(posx[unit],0)))
            
            # draw the nodes
            for unit in range(len(pic_nodes)):
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
        
#==============================================================================
# PART ONE
#==============================================================================

# make John's training sets and assign desired outputs

catA1 = [0.0]*10
catA1[5] = 1.0
catA2 = [0.0]*10
catA2[9] = 1.0
DO_1 = [.98,.02,.02,.02]

catB1 = [0.0]*10
catB1[4] = 1.0
catB1[8] = 1.0
catB2 = [0.0]*10
catB2[3] = 1.0
DO_2 = [.02,.98,.02,.02]

catC1 = [0.0]*10
catC1[7] = 1.0
catC2 = [0.0]*10
catC2[2] = 1.0
DO_3 = [.02,.02,.98,.02]

catD1 = [0.0]*10
catD1[1] = 1.0
catD1[6] = 1.0
catD2 = [0.0]*10
catD2[0] = 1.0
catD2[6] = 1.0
DO_4 = [.02,.02,.02,.98]

training_set1 = [catA1,catA2,catB1,catB2,catC1,catC2,catD1,catD2]
DOs = [DO_1,DO_1,DO_2,DO_2,DO_3,DO_3,DO_4,DO_4]

def create_test_set(training_set, probability = 0.0):
    """Takes a list of lists of 1s and 0s and flips each element with probability = probability"""
    bastardized_set = training_set[:]
    # iterate through every element
    for i in range(len(bastardized_set)):
        for j in range(len(bastardized_set[0])):
            state = bastardized_set[i][j]
            change = 0.0
            if state == 1.0:
                change = 0.0
            elif state == 0.0:
                change = 1.0
            bastardized_set[i][j] = rnd.choice([state,change],p=[1-probability,probability])
    return bastardized_set


#--------------------------------------------------
#categorizer = LayeredNetwork(10,0,4)
#
#categorizer.reset_nodes()
#categorizer.reset_weights()
#categorizer.train(training_set1,DOs,5000,.75,0.05)
##categorizer.display_connections(1)
#categorizer.run(catB2,DO_1,1)
##categorizer.display_activations(training_set1)
#categorizer.display_activations(training_set1)
#
#test_set1 = create_test_set(trainging_set1,.25)
#categorizer.display_activations(test_set1)
#---------------------------------------------------    
    
    
#---------------------------------------------------    
#categorizerHL = LayeredNetwork(10,4,4,1)
#categorizerHL.train(training_set1,DOs,5000,.75,0.05)
#categorizerHL.display_activations(training_set1)
#    
#test_set1 = create_test_set(training_set1, .25)
#
##categorizer.display_connections(1)
##categorizerHL.run(catB2,DO_1,1)
#categorizerHL.display_activations(test_set1)
#-----------------------------------------------------

#==============================================================================
# PART ONE set 2
#==============================================================================

catA1 = [0.0]*10
catA1[0] = 1.0
catA1[1] = 1.0
catA1[3] = 1.0
catA1[9] = 1.0
catA2 = [0.0]*10
catA2[0] = 1.0
catA2[1] = 1.0
catA2[4] = 1.0
catA2[9] = 1.0
DO_1 = [.98,.02,.02,.02]

catB1 = [0.0]*10
catB1[0] = 1.0
catB1[1] = 1.0
catB1[5] = 1.0
catB1[8] = 1.0
catB2 = [0.0]*10
catB2[0] = 1.0
catB2[1] = 1.0
catB2[8] = 1.0
DO_2 = [.02,.98,.02,.02]

catC1 = [0.0]*10
catC1[0] = 1.0
catC1[2] = 1.0
catC1[3] = 1.0
catC1[7] = 1.0
catC2 = [0.0]*10
catC2[0] = 1.0
catC2[2] = 1.0
catC2[4] = 1.0
catC2[7] = 1.0
DO_3 = [.02,.02,.98,.02]

catD1 = [0.0]*10
catD1[0] = 1.0
catD1[2] = 1.0
catD1[5] = 1.0
catD1[6] = 1.0
catD2 = [0.0]*10
catD2[0] = 1.0
catD2[2] = 1.0
catD2[6] = 1.0
DO_4 = [.02,.02,.02,.98]

training_set2 = [catA1,catA2,catB1,catB2,catC1,catC2,catD1,catD2]
DOs2 = [DO_1,DO_1,DO_2,DO_2,DO_3,DO_3,DO_4,DO_4]

#---------------------------------------------------------
#s2categorizer = LayeredNetwork(10,0,4)
#
#s2categorizer.train(training_set2,DOs2,5000,.75,0.05)
##print categorizer.connections[0].weight
##categorizer.display_connections(1)
##s2categorizer.run(catD2,DO_1,1)
#s2categorizer.display_activations(training_set2)
#
#test_set2 = create_test_set(training_set2,.25)
#s2categorizer.display_activations(test_set2)
#---------------------------------------------------------


#---------------------------------------------------------
#s2categorizerHL = LayeredNetwork(10,4,4,1)
#
#s2categorizerHL.train(training_set2,DOs2,5000,.75,0.05)
##print categorizer.connections[0].weight
##categorizer.display_connections(1)
##s2categorizer.run(catD2,DO_1,1)
#s2categorizerHL.display_activations(training_set2)
#
#test_set2 = create_test_set(training_set2,.25)
#s2categorizerHL.display_activations(test_set2)
#----------------------------------------------------------

#==============================================================================
# PART ONE set 3 
#==============================================================================

catA1 = [0.0]*10
catA1[0] = 1.0
catA1[1] = 1.0
catA1[2] = 1.0
catA1[3] = 1.0
catA1[4] = 1.0
catA2 = [0.0]*10
catA2[5] = 1.0
catA2[6] = 1.0
catA2[7] = 1.0
catA2[8] = 1.0
catA2[9] = 1.0
DO_1 = [.98,.02]

catB1 = [0.0]*10
catB1[0] = 1.0
catB1[1] = 1.0
catB1[3] = 1.0
catB1[4] = 1.0
catB1[7] = 1.0
catB2 = [0.0]*10
catB2[2] = 1.0
catB2[5] = 1.0
catB2[6] = 1.0
catB2[8] = 1.0
catB2[9] = 1.0
DO_2 = [.02,.98]

training_set3 = [catA1,catA2,catB1,catB2]
DOs3 = [DO_1,DO_1,DO_2,DO_2]

#--------------------------------------------------------
#s3categorizer = LayeredNetwork(10,0,2)
#
#s3categorizer.reset_nodes()
#s3categorizer.reset_weights()
#s3categorizer.train(training_set3,DOs3,5000,.75,0.05)
##print categorizer.connections[0].weight
##categorizer.display_connections(1)
##s3categorizer.run(catA1,DO_1,1)
#test_set3 = create_test_set(training_set3,.25)
#s3categorizer.display_activations(test_set3)
#---------------------------------------------------------


#---------------------------------------------------------
#s3categorizerHL = LayeredNetwork(10,4,2,1)
#
#s3categorizerHL.train(training_set3,DOs3,5000,.75,0.05)
##print categorizer.connections[0].weight
##categorizer.display_connections(1)
##s2categorizer.run(catD2,DO_1,1)
#s3categorizerHL.display_activations(training_set3)
#
#test_set3 = create_test_set(training_set3,.25)
#s3categorizerHL.display_activations(test_set3)
#---------------------------------------------------------

#==============================================================================
# PART TWO: autoencoder
#==============================================================================

s0 = [0.0]*8
s0[0] = 1.0
o0 = [0.02]*8
o0[0] = .98
s1 = [0.0]*8
s1[1] = 1.0
o1 = [0.02]*8
o1[1] = .98
s2 = [0.0]*8
s2[2] = 1.0
o2 = [0.02]*8
o2[2] = .98
s3 = [0.0]*8
s3[3] = 1.0
o3 = [0.02]*8
o3[3] = .98
s4 = [0.0]*8
s4[4] = 1.0
o4 = [0.02]*8
o4[4] = .98
s5 = [0.0]*8
s5[5] = 1.0
o5 = [0.02]*8
o5[5] = .98
s6 = [0.0]*8
s6[6] = 1.0
o6 = [0.02]*8
o6[6] = .98

training_set_ae = [s0,s1,s2,s3,s4,s5,s6]
DOs_ae = [o0,o1,o2,o3,o4,o5,o6]

#----------------------------------------------------------
#autoencoder = LayeredNetwork(8,3,8,1)
#
#autoencoder.reset_nodes()
#autoencoder.reset_weights()
#autoencoder.train(training_set_ae,DOs_ae,5000,.75,0.1)

#autoencoder.run(s6,o1,1)
#autoencoder.display_activations(training_set_ae)

#==============================================================================
# PART TWO B, generalization
#==============================================================================

ns1 = [0.0]*8
ns1[0] = 1.0
ns1[1] = 1.0
ns1[2] = 1.0

no1 = [0.02]*8
no1[0] = .98
no1[1] = .98
no1[2] = .98

ns2 = [0.0]*8
ns2[3] = 1.0
ns2[4] = 1.0
ns2[5] = 1.0

no2 = [0.02]*8
no2[3] = .98
no2[4] = .98
no2[5] = .98

new_training_set_ae = [ns1,ns2]
new_DOs_ae = [no1,no2]

#autoencoder.train(new_training_set_ae,new_DOs_ae,5000,.75,0.1)
#autoencoder.display_activations(new_training_set_ae)

randy1 = [0.0]*8
randy1[2] = 1.0
randy1[3] = 1.0

randy2 = [0.0]*8
randy2[5] = 1.0
randy2[6] = 1.0

randy3 = [0.0]*8
randy3[1] = 1.0
randy3[4] = 1.0

randy_set = [randy1,randy2,randy3]

#autoencoder.display_activations(randy_set)

#==============================================================================
# PART TWO C, rules
#==============================================================================

odd_man = [0.0]*8
odd_man[-1] = 1.0
odd_man_DO = [.02]*8
odd_man_DO[-1] = .98

#autoencoder.run(odd_man,odd_man_DO,1)
#autoencoder.display_activations(odd_man)
#-----------------------------------------------------------------