# -*- coding: utf-8 -*-
"""
Created on Thu Feb 08 14:50:34 2018

@author: Evan
"""

class Connection(object):
    def __init__(self, sender = None, recipient = None, weight = 0.0):
        """Class of connection objects with sender, recipient, and weight"""
        self.sender = sender
        self.recipient = recipient
        self.weight = weight
        
class Unit(object):
    def __init__(self, excite_output = 0.0, inhibi_output = 0.0, net_state = 0.0, pos_input = 0.0, neg_input = 0.0, threshold = .5, refract = False, incoming = None, outgoing = None):
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
    def add_connection(self, connection):
        """Add connection objects to incoming/outgoing list unit object attributes"""
        self.incoming.append(connection)
        connection.sender.outgoing.append(connection)
    def get_input(self):
        # sum inputs over all connections and units
        for i in range(len(self.incoming)):
            self.net_state += (self.incoming[i].sender.excite_output+self.incoming[i].sender.inhibi_output)*self.incoming[i].weight
        print "net state: ",self.net_state
    def update_activation(self):
        if self.refract == True: #don't spike if you just spiked
            self.refract = False
            self.excite_output = 0.0
            self.net_state = 0.0
        elif self.net_state > self.threshold: #spike if resting potential exceeds threshold
            self.excite_output = 1.0
            self.refract = True
        elif self.net_state >= .1: #reduce resting potential a bit if no refract and no spike
            self.net_state -= .1
        print "activation: ",self.excite_output
    def reset(self): # handy reset method
        self.net_state = 0.0
        self.excite_output = 0.0
        self.inhibi_output = 0.0
        self.pos_input = 0.0
        self.neg_input = 0.0
        self.refract = False
    def activateF1(self):
        self.excite_output = self.net_state - .5
        print "activation: ",self.excite_output
    def activateF2(self):
        if self.net_state > 1.0:
            self.excite_output = 1.0
        elif self.net_state < .75:
            self.excite_output = 0.0
        else:
            self.excite_output = self.net_state
        print "activation: ",self.excite_output
    def activateFa(self):
        self.excite_output += 0.5*(1-self.excite_output)*self.net_state
        print "activation: ",self.excite_output
    def activateFb(self):
        self.excite_output += 0.5*(1-self.excite_output)*self.net_state - 0.1*self.excite_output
        print "activation: ",self.excite_output
    def activateFc(self):
        self.excite_output += 0.5*((1-self.excite_output)*self.pos_input + (1+self.excite_output)*self.neg_input)
        print "activation: ",self.excite_output

nodes = range(3) # how many units would you like?
units = [] # empty units list
connections = [] # empty connections list

# create the units
for node in nodes:
    units.append(Unit())

# connect every unit to every other unit but itself, step 1: create connections   
for unit_i in units:
    for i in range(len(nodes)):
        if not unit_i is units[i]:
            connections.append(Connection(unit_i,units[i],1.0))

# connect units, step 2: add connection Unit method   
for connect_i in range(len(connections)):
    connections[connect_i].recipient.add_connection(connections[connect_i])
    
# 1.1 a
units[0].excite_output = 1.0
units[1].excite_output = 1.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF1()
        
# they sync up and reach crazy high values because they're all connected
# and each round adds more than activity than it takes away; they just
# volley around like crazy
        
for i in range(len(units)):
    units[i].reset()
    
# 1.1 b
units[0].excite_output = 1.0
units[1].excite_output = 0.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF1()
        
# unit 0 gets negative at first but then they quickly sync up and reach
# high values because they're all connected and each round is still
# adding more activity than it's taking away
        
for i in range(len(units)):
    units[i].reset()
    
# 1.1 c
units[0].excite_output = 0.5
units[1].excite_output = 0.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF1()
        
# same business but now they sync up and get negative because more energy
# is being removed from the system than put into it
        
for i in range(len(units)):
    units[i].reset()
        
# 1.2 a
units[0].excite_output = 1.0
units[1].excite_output = 1.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF2()
        
# These activation functions put some boundaries on the activation levels
# so things don't get quite as crazy. Enough energy is supplied to the 
# system that all the units can activate, and from there they always stay
# active because there are no rules to bring them below the activation
# threshold given these starting values
        
for i in range(len(units)):
    units[i].reset()
        
# 1.2 b
units[0].excite_output = 1.0
units[1].excite_output = 0.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF2()
        
# A little slower but same thing
        
for i in range(len(units)):
    units[i].reset()
        
# 1.2 c
units[0].excite_output = 0.5
units[1].excite_output = 0.0
units[2].excite_output = 0.0

for i in range(10):
    for j in range(len(units)):
        units[j].get_input()
    for k in range(len(units)):
        units[k].activateF2()
        
# Same as 1.1 c but now there is a floor for activation
        
#### PART TWO ####

unit_solo = Unit()

# a1
unit_solo.reset()

for i in range(10):
    unit_solo.net_state = 1.5
    unit_solo.activateFa()
    
# a2
unit_solo.reset()

for i in range(10):
    unit_solo.net_state = 5.0
    unit_solo.activateFa()
    
# a3
unit_solo.reset()

for i in range(10):
    unit_solo.net_state = 3.0
    unit_solo.activateFa()
    
# a4
unit_solo.reset()    
    
for i in range(2):
    unit_solo.net_state = 1.0
    unit_solo.activateFa()
    
for i in range(5):
    unit_solo.net_state = -1.0
    unit_solo.activateFa()
    
# a5
unit_solo.reset()    
    
for i in range(50):
    unit_solo.net_state = 1.0
    unit_solo.activateFa()
    
for i in range(5):
    unit_solo.net_state = -1.0
    unit_solo.activateFa()
    
# b1
unit_solo.reset()    
    
for i in range(10):
    unit_solo.net_state = 1.0
    unit_solo.activateFb()
    
for i in range(5):
    unit_solo.net_state = -1.0
    unit_solo.activateFb()
    
# c1
unit_solo.reset()    
    
for i in range(10):
    unit_solo.pos_input = 1.0
    unit_solo.neg_input = 0.0
    unit_solo.activateFc()
    
for i in range(5):
    unit_solo.pos_input = 0.0
    unit_solo.neg_input = -1.0
    unit_solo.activateFc()
    
# 2.1
    # In a1 the activation asymptoted towards 1.0, while in a2 it jumped
    # back and forth from positive to negative with increasing magnitude
    # on each iteration. a1 kept getting closer to 1.0 because the way the
    # equation is set up, it always adds 75% of 1-the current activity state.
    # a2 is different because it adds 250% of 1-the current activity state,
    # and the initial output becomes more than one so it jumps back and forth
    # from positive to negative. 
    
# 2.2 
    # a3 is kind of like a blend of a1 and a2, which makes sense because the
    # amount of activity being added falls between them (150% as opposed to
    # 50% or 250%). So it ends up honing in on 1.0 due to its outputs 
    # being slightly more or slightly less than one each time with
    # decreasing magnitude. 
    
# 2.3
    # a5 got so close to 1.0 that the system decided IT WAS 1.0, then 
    # when we change the formula to reduce energy nothing changes because
    # the delta_activity output is -0.0. This didn't happen in a4 because
    # we only run the first activation function for 2 iterations rather
    # than 50, so it never gets so close to 1.0 that the system decides
    # to call it a day and round 'er out resulting in the no change outcome
    # present in a5. 
    
# 2.4
    # The activation function of b1 subtracts an additional 10% of its 
    # activation state compared to that of a5. This causes b1 to accumulate
    # activity more slowly, and it doesn't reach the 1.0 value that breaks
    # the neuron. 
    
# 2.5
    # They both will go towards negative infinity. They keep subtracting 50%
    # of the activity so it builds continously towards greater negative
    # values. 
    
# 2.6
    # Again we're working with different activation functions. c1 is like the
    # a type activation functions except that it differentiates between 
    # excitatory and inhibitory inputs. b1 is like the a type activations
    # but it removes 10% more activity per iteration than the a's. So b1 grows
    # slower in activity then subsequently gets negative faster, while c1
    # grows more quickly and subsequently gets negative slower. 
    
    
#### PART THREE ####

nodez = range(10) # how many units would you like?
unitz = [] # empty units list
connectionz = [] # empty connections list

# create the units
for node in nodez:
    unitz.append(Unit())

# connect every unit to every other unit but itself, step 1: create connections   
for unit_i in unitz:
    for i in range(len(nodez)):
        if not unit_i is unitz[i]:
            connectionz.append(Connection(unit_i,unitz[i],1.0))

# connect units, step 2: add connection Unit method   
for connect_i in range(len(connectionz)):
    connectionz[connect_i].recipient.add_connection(connectionz[connect_i])
    
unitz[0].excite_output = 1.0
unitz[1].excite_output = 1.0
unitz[2].excite_output = 1.0

for i in range(3):
    for j in range(len(unitz)):
        unitz[j].get_input()
    for k in range(len(unitz)):
        unitz[k].update_activation()
        
# adding an absolute refractory period in a totally interconnected network
        # leads to everyone becoming active on the first iteration and then
        # everything is kill afterwards and nothing else can happen. At least
        # when we're simulating synchronous updating. Let's try with 
        # asynchronous updating. 
        
for i in range(len(unitz)):
    unitz[i].reset()
    
unitz[0].excite_output = 1.0
unitz[1].excite_output = 1.0
unitz[2].excite_output = 1.0

for i in range(3):
    for j in range(len(unitz)):
        unitz[j].get_input()
        unitz[j].update_activation()
        
# Same thing! The next step would probably be a Hopfield net so we'll save
        # that for next time.