# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:04:03 2018

@author: Evan
"""

import numpy as np
import numpy.random as rnd
from matplotlib import pyplot, figure

np.random.seed(1738)

class Connection(object):
    def __init__(self, sender = None, recipient = None, weight = 0.0):
        """Class of connection objects with sender, recipient, and weight"""
        self.sender = sender
        self.recipient = recipient
        self.weight = weight
        
class Unit(object):
    def __init__(self, excite_output = 0.0, inhibi_output = 0.0, net_state = 0.0, pos_input = 0.0, neg_input = 0.0, threshold = 0.0, refract = False, incoming = None, outgoing = None):
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
        signals = []
        for i in range(len(self.incoming)):
            signals.append((self.incoming[i].sender.excite_output+self.incoming[i].sender.inhibi_output)*self.incoming[i].weight)
        self.net_state = sum(signals)
        #print "net state: ",self.net_state
    def update_activation(self):
        t0 = self.excite_output
        if self.net_state > self.threshold: #spike if resting potential exceeds threshold
            self.excite_output = 1.0
        t1 = self.excite_output
        return t0,t1
        #print "activation: ",self.excite_output
    def reset(self): # handy reset method
        self.net_state = 0.0
        self.excite_output = 0.0
        self.inhibi_output = 0.0
        self.pos_input = 0.0
        self.neg_input = 0.0
        self.refract = False
        

#### PART ONE ####

# create a network object class comprised of units and their connections
class Network(object):
    def __init__(self, n_nodes = 0, units = [], connections = [], energy = []):
        self.n_nodes = n_nodes
        self.units = units
        self.connections = connections
        self.energy = energy
        
    # create the units
        for node in range(self.n_nodes):
            self.units.append(Unit())

    # connect every unit to every other unit but itself, step 1: create connections   
        for unit_i in self.units:
            for i in range(self.n_nodes):
                if not unit_i is self.units[i]:
                    self.connections.append(Connection(unit_i,self.units[i]))

    # connect units, step 2: add connection Unit method   
        for connect_i in range(len(self.connections)):
            self.connections[connect_i].recipient.add_connection(self.connections[connect_i]) 
        
    def train(self, training_set):
    # input a list of training sets for training and end up changing some connection weights
        # iterate through each training pattern in the set
        for i in range(len(training_set)):
            # iterate through each unit
            for j in range(len(self.units)):
                # and make each unit's activation equal to its corresponding node in the pattern
                if len(np.shape(training_set)) > 1:
                    self.units[j].excite_output = training_set[i][j]
                else:
                    self.units[j].excite_output = training_set[j]
            # now iterate through all of the connections
            for k in range(len(self.connections)):
                # if the sender and recipeint are doing the same thing
                if self.connections[k].recipient.excite_output == self.connections[k].sender.excite_output:
                    # increase the connection weight by one
                    self.connections[k].weight += 1.0
                # if they're doing something different    
                else:
                    # decrease the connection weight by one
                    self.connections[k].weight -= 1.0
                
    def run(self, test_pattern, target_pattern):
    # chew on a test pattern
        settled = False # settled criterion boolean
        settle_crit = 30 # number of no change states defined as proper settling
        stable_it = 0 # start the stability counter at 0
        iterations = 0 # start the iterations counter at 0
        max_it = 5000
        energies = []
        
        for i in range(len(self.units)):
            # set each unit to its corresponding test pattern activation level
            self.units[i].excite_output = test_pattern[i]
        
        while not settled:
        # while settle criteria has not been met
            # pick a random integer within the range of our number of units in the network
            i = rnd.randint(len(self.units))

            # update this unit's inputs and activations
            self.units[i].get_input()            
            t0,t1 = self.units[i].update_activation()
            current_energy = self.get_energy()
            energies.append(float(current_energy))
                
            # check if the activation state at time 0 and time 1 are different
            if t0 == t1:
                # if same, count this as a stable iteration
                stable_it += 1
                # if different, reset the stability counter
            else:
                stable_it = 0
            
            # add to our iteration count
            iterations += 1
            
            # if no change in activations for enough iterations to meet our criteria, call it settled
            if stable_it >= settle_crit:
                settled = True
                
            if iterations > max_it:
                settled = True
            
        # get hamming distance
        hamming_distance = 0
        for i in range(len(target_pattern)):
            if self.units[i].excite_output != target_pattern[i]:
                hamming_distance += 1
        # return count of different activations and # iterations to settle
        return hamming_distance,iterations,energies
        
    def run_all(self, test_pattern, target_pattern, n_cycles = 1):
        # chew on a test pattern
        settled = False # settled criterion boolean
        settle_crit = 30 # number of no change states defined as proper settling
        stable_it = 0 # start the stability counter at 0
        iterations = 0 # start the iterations counter at 0
        max_it = 5000
        energies = []
        
        for i in range(len(self.units)):
            # set each unit to its corresponding test pattern activation level
            self.units[i].excite_output = test_pattern[i]
        
        while not settled:
        # while settle criteria has not been met
        
            for i in range(len(self.units)):
                self.units[i].get_input()
            t0s = []
            t1s = []            
            for i in range(len(self.units)):
                t0,t1 = self.units[i].update_activation()
                t0s.append(t0)
                t1s.append(t1)
            current_energy = self.get_energy()
            energies.append(float(current_energy))
                
            # check if the activation state at time 0 and time 1 are different
            if t0s == t1s:
                # if same, count this as a stable iteration
                stable_it += 1
                # if different, reset the stability counter
            else:
                stable_it = 0
            
            # add to our iteration count
            iterations += 1
            
            # if no change in activations for enough iterations to meet our criteria, call it settled
            if stable_it >= settle_crit:
                settled = True
                
            if iterations > max_it:
                settled = True
            
        # get hamming distance
        hamming_distance = 0
        for i in range(len(target_pattern)):
            if self.units[i].excite_output != target_pattern[i]:
                hamming_distance += 1
        # return count of different activations and # iterations to settle
        return hamming_distance,iterations,energies
        
    def run_8(self, test_pattern, target_pattern):
    # chew on a test pattern
        settled = False # settled criterion boolean
        settle_crit = 30 # number of no change states defined as proper settling
        stable_it = 0 # start the stability counter at 0
        iterations = 0 # start the iterations counter at 0
        max_it = 5000
        energies = []
        
        for i in range(len(self.units)):
            # set each unit to its corresponding test pattern activation level
            self.units[i].excite_output = test_pattern[i]
        
        while not settled:
        # while settle criteria has not been met
            # pick a random integer within the range of our number of units in the network
            chosen_units = rnd.choice(range(len(self.units)), size = (1,8), replace = False)
            chosen_units = list(chosen_units[0])

            # update this unit's inputs and activations
            for i in chosen_units:
                self.units[i].get_input()
            t0s = []
            t1s = []            
            for i in chosen_units:
                t0,t1 = self.units[i].update_activation()
                t0s.append(t0)
                t1s.append(t1)
            current_energy = self.get_energy()
            energies.append(float(current_energy))
                
            # check if the activation state at time 0 and time 1 are different
            if t0 == t1:
                # if same, count this as a stable iteration
                stable_it += 1
                # if different, reset the stability counter
            else:
                stable_it = 0
            
            # add to our iteration count
            iterations += 1
            
            # if no change in activations for enough iterations to meet our criteria, call it settled
            if stable_it >= settle_crit:
                settled = True
                
            if iterations > max_it:
                settled = True
            
        # get hamming distance
        hamming_distance = 0
        for i in range(len(target_pattern)):
            if self.units[i].excite_output != target_pattern[i]:
                hamming_distance += 1
        # return count of different activations and # iterations to settle
        return hamming_distance,iterations,energies        
    
    def run_4(self, test_pattern, target_pattern):
    # chew on a test pattern
        settled = False # settled criterion boolean
        settle_crit = 30 # number of no change states defined as proper settling
        stable_it = 0 # start the stability counter at 0
        iterations = 0 # start the iterations counter at 0
        max_it = 5000
        energies = []
        
        for i in range(len(self.units)):
            # set each unit to its corresponding test pattern activation level
            self.units[i].excite_output = test_pattern[i]
        
        while not settled:
        # while settle criteria has not been met
            # pick a random integer within the range of our number of units in the network
            chosen_units = rnd.choice(range(len(self.units)), size = (1,4), replace = False)
            chosen_units = list(chosen_units[0])

            # update this unit's inputs and activations
            for i in chosen_units:
                self.units[i].get_input()
            t0s = []
            t1s = []            
            for i in chosen_units:
                t0,t1 = self.units[i].update_activation()
                t0s.append(t0)
                t1s.append(t1)
            current_energy = self.get_energy()
            energies.append(float(current_energy))
                
            # check if the activation state at time 0 and time 1 are different
            if t0 == t1:
                # if same, count this as a stable iteration
                stable_it += 1
                # if different, reset the stability counter
            else:
                stable_it = 0
            
            # add to our iteration count
            iterations += 1
            
            # if no change in activations for enough iterations to meet our criteria, call it settled
            if stable_it >= settle_crit:
                settled = True
                
            if iterations > max_it:
                settled = True
            
        # get hamming distance
        hamming_distance = 0
        for i in range(len(target_pattern)):
            if self.units[i].excite_output != target_pattern[i]:
                hamming_distance += 1
        # return count of different activations and # iterations to settle
        return hamming_distance,iterations,energies    
    
    def reset_nodes(self):
        # iterate through units in the network
        # reset state of each unit
        for i in range(len(self.units)):
            self.units[i].net_state = 0.0
            self.units[i].excite_output = 0.0
            self.units[i].inhibi_output = 0.0
            self.units[i].pos_input = 0.0
            self.units[i].neg_input = 0.0
            self.units[i].refract = False
            
    def reset_weights(self):
        for i in range(len(self.connections)):
            self.connections[i].weight = 0.0
        
    def get_energy(self):
        fin_states = []
        for i in range(len(self.connections)):
            fin_states.append(self.connections[i].sender.excite_output*self.connections[i].recipient.excite_output*self.connections[i].weight)
        
        self.energy = -.5*sum(fin_states)
        return float(self.energy)
        
    def display_connections(self):
    # display the connection weights
        #start with a 2-D array of zeros of length n_nodes by n_nodes
        array = np.zeros((self.n_nodes*self.n_nodes))
        #initialize a counter to help retrieve skipped values caused by unit to same unit connections being artificially supplied
        skip = 0
        #iterate through the array
        for i in xrange(self.n_nodes*self.n_nodes):
            #if the node falls on the diagonal
            if i%(self.n_nodes+1) == 0:
                #show its weight as 0
                array[i] = 0.0
                #and note that we have skipped a connection by artificially supplying a value here
                skip += 1
            #otherwise its a true connection with a true weight
            else:
                #get the weight
                array[i] = self.connections[i-skip].weight
        #reshape the 2-D array into an n_nodes by n_nodes array
        array = np.reshape(array,(self.n_nodes,self.n_nodes))
        #plot the weights without interpolation
        pyplot.imshow(array, cmap = 'Greys', interpolation = 'none')
        
    def display_activations(self):
        array = np.zeros((2,self.n_nodes))
        for i in xrange(self.n_nodes):
            array[1,i] = self.units[i].excite_output
        pyplot.imshow(array, cmap = 'Greys', interpolation = 'none')
        
Hoppy_mayne = Network(16)

# (A)

pattern1 = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
pattern2 = [1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0]
pattern3 = [1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0]
pattern4 = [1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0]

training_set1 = [pattern1[:],pattern2[:],pattern3[:],pattern4[:]]

Hoppy_mayne.train(training_set1)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

# (B)

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

num_bastards = 3
bastards = []
probs = [0.0,.1,.2,.3,.4,.5]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        bastards.append(create_test_set(training_set1,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        training_set1 = [pattern1[:],pattern2[:],pattern3[:],pattern4[:]]
        
# (B.1)
hamming_distances_out = []
iterations_out = []
energies_out = []
p = []

for i in range(len(training_set1)):
# for each trained pattern
    for j in range(len(bastards)):
    # for each bastardized training set
        for k in range(len(bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(bastards[j][k],training_set1[i])
                hamming_distances_out.append(H)
                iterations_out.append(I)
                energies_out.append(E)
                Hoppy_mayne.reset_nodes()
                if j < 3:
                    p.append(0)
                elif j < 6:
                    p.append(1)
                elif j < 9:
                    p.append(2)
                elif j < 12:
                    p.append(3)
                elif j < 15:
                    p.append(4)
                else:
                    p.append(5)
            else:
                Hoppy_mayne.reset_nodes()

# pack up the outputs nice and neat
p1_B_outputs = zip(hamming_distances_out,iterations_out,energies_out)

# doing a bunch of annoying as fuck sorting to clump the outputs into the
# correct probability clusters
# I'm sure there's a better way to do this but I gave up looking
# I'm guessing it involves converting to something other than lists
i0 = [i for i in range(len(p)) if p[i]==0]
i1 = [i for i in range(len(p)) if p[i]==1]
i2 = [i for i in range(len(p)) if p[i]==2]
i3 = [i for i in range(len(p)) if p[i]==3]
i4 = [i for i in range(len(p)) if p[i]==4]
i5 = [i for i in range(len(p)) if p[i]==5]
ham0 = []
ham1 = []
ham2 = []
ham3 = []
ham4 = []
ham5 = []
iter0 = []
iter1 = []
iter2 = []
iter3 = []
iter4 = []
iter5 = []

for i in i0:
    ham0.append(hamming_distances_out[i])
    iter0.append(iterations_out[i])
mean_iter0 = np.mean(iter0)
mean_ham0 = np.mean(ham0)
for i in i1:
    ham1.append(hamming_distances_out[i])
    iter1.append(iterations_out[i])
mean_iter1 = np.mean(iter1)
mean_ham1 = np.mean(ham1)
for i in i2:
    ham2.append(hamming_distances_out[i])
    iter2.append(iterations_out[i])
mean_iter2 = np.mean(iter2)
mean_ham2 = np.mean(ham2)    
for i in i3:
    ham3.append(hamming_distances_out[i])
    iter3.append(iterations_out[i])
mean_iter3 = np.mean(iter3)
mean_ham3 = np.mean(ham3)
for i in i4:
    ham4.append(hamming_distances_out[i])
    iter4.append(iterations_out[i])
mean_iter4 = np.mean(iter4)
mean_ham4 = np.mean(ham4)
for i in i5:
    ham5.append(hamming_distances_out[i])
    iter5.append(iterations_out[i])
mean_iter5 = np.mean(iter5)
mean_ham5 = np.mean(ham5)

#==============================================================================
# PART TWO
#==============================================================================


def create_random_set(n_patterns, pattern_length):
    random_set = []
    for i in range(n_patterns):
        row = []
        for j in range(pattern_length):
            integer = rnd.randint(2)   
            row.append(float(integer))
        if n_patterns > 1:
            random_set.append(row)
    if n_patterns == 1:
        return row
    else:
        return random_set

rnd_training_set = create_random_set(3,16)

rnd_pattern1 = rnd_training_set[0][:]
rnd_pattern2 = rnd_training_set[1][:]
rnd_pattern3 = rnd_training_set[2][:]

Hoppy_mayne.reset_nodes()
Hoppy_mayne.reset_weights()

Hoppy_mayne.train(rnd_training_set)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

num_bastards = 3
rnd_bastards = []
probs = [0.0,.1,.2,.3,.4,.5]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        rnd_bastards.append(create_test_set(rnd_training_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        rnd_training_set = [rnd_pattern1[:],rnd_pattern2[:],rnd_pattern3[:]]
        
# (B.1)
rnd_hamming_distances_out = []
rnd_iterations_out = []
rnd_energies_out = []
p = []

for i in range(len(rnd_training_set)):
# for each trained pattern
    for j in range(len(rnd_bastards)):
    # for each bastardized training set
        for k in range(len(rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(rnd_bastards[j][k],rnd_training_set[i])
                rnd_hamming_distances_out.append(H)
                rnd_iterations_out.append(I)
                rnd_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
                if j < 3:
                    p.append(0)
                elif j < 6:
                    p.append(1)
                elif j < 9:
                    p.append(2)
                elif j < 12:
                    p.append(3)
                elif j < 15:
                    p.append(4)
                else:
                    p.append(5)
            else:
                Hoppy_mayne.reset_nodes()

# pack up the outputs nice and neat
p2_A_outputs = zip(rnd_hamming_distances_out,rnd_iterations_out,rnd_energies_out)

i0 = [i for i in range(len(p)) if p[i]==0]
i1 = [i for i in range(len(p)) if p[i]==1]
i2 = [i for i in range(len(p)) if p[i]==2]
i3 = [i for i in range(len(p)) if p[i]==3]
i4 = [i for i in range(len(p)) if p[i]==4]
i5 = [i for i in range(len(p)) if p[i]==5]
ham0 = []
ham1 = []
ham2 = []
ham3 = []
ham4 = []
ham5 = []
iter0 = []
iter1 = []
iter2 = []
iter3 = []
iter4 = []
iter5 = []

for i in i0:
    ham0.append(hamming_distances_out[i])
    iter0.append(iterations_out[i])
rnd_mean_iter0 = np.mean(iter0)
rnd_mean_ham0 = np.mean(ham0)
for i in i1:
    ham1.append(hamming_distances_out[i])
    iter1.append(iterations_out[i])
rnd_mean_iter1 = np.mean(iter1)
rnd_mean_ham1 = np.mean(ham1)
for i in i2:
    ham2.append(hamming_distances_out[i])
    iter2.append(iterations_out[i])
rnd_mean_iter2 = np.mean(iter2)
rnd_mean_ham2 = np.mean(ham2)    
for i in i3:
    ham3.append(hamming_distances_out[i])
    iter3.append(iterations_out[i])
rnd_mean_iter3 = np.mean(iter3)
rnd_mean_ham3 = np.mean(ham3)
for i in i4:
    ham4.append(hamming_distances_out[i])
    iter4.append(iterations_out[i])
rnd_mean_iter4 = np.mean(iter4)
rnd_mean_ham4 = np.mean(ham4)
for i in i5:
    ham5.append(hamming_distances_out[i])
    iter5.append(iterations_out[i])
rnd_mean_iter5 = np.mean(iter5)
rnd_mean_ham5 = np.mean(ham5)


# (B)
#==============================================================================
# adding pattern 4
#==============================================================================
rnd_pattern4 = create_random_set(1,16)

Hoppy_mayne.train(rnd_pattern4)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

rnd_training_set.append(rnd_pattern4)

num_bastards = 3
rnd_bastards = []
probs = [.2]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        rnd_bastards.append(create_test_set(rnd_training_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        rnd_training_set = [rnd_pattern1[:],rnd_pattern2[:],rnd_pattern3[:],rnd_pattern4[:]]
        
rnd4_hamming_distances_out = []
rnd4_iterations_out = []
rnd4_energies_out = []

for i in range(len(rnd_training_set)):
# for each trained pattern
    for j in range(len(rnd_bastards)):
    # for each bastardized training set
        for k in range(len(rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(rnd_bastards[j][k],rnd_training_set[i])
                rnd4_hamming_distances_out.append(H)
                rnd4_iterations_out.append(I)
                rnd4_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
            else:
                Hoppy_mayne.reset_nodes()
                
# pack up the outputs nice and neat
p2_B4_outputs = zip(rnd4_hamming_distances_out,rnd4_iterations_out,rnd4_energies_out)

# mean hamming distances for each probability set
rnd4_mean_ham = np.mean(rnd4_hamming_distances_out)

# mean iterations for each probability set
rnd4_mean_it = np.mean(rnd4_iterations_out)

#==============================================================================
# adding pattern 5
#==============================================================================
rnd_pattern5 = create_random_set(1,16)

Hoppy_mayne.train(rnd_pattern5)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

rnd_training_set.append(rnd_pattern5)

num_bastards = 3
rnd_bastards = []
probs = [.2]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        rnd_bastards.append(create_test_set(rnd_training_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        rnd_training_set = [rnd_pattern1[:],rnd_pattern2[:],rnd_pattern3[:],rnd_pattern4[:],rnd_pattern5[:]]
        
rnd5_hamming_distances_out = []
rnd5_iterations_out = []
rnd5_energies_out = []

for i in range(len(rnd_training_set)):
# for each trained pattern
    for j in range(len(rnd_bastards)):
    # for each bastardized training set
        for k in range(len(rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(rnd_bastards[j][k],rnd_training_set[i])
                rnd5_hamming_distances_out.append(H)
                rnd5_iterations_out.append(I)
                rnd5_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
            else:
                Hoppy_mayne.reset_nodes()
                
# pack up the outputs nice and neat
p2_B5_outputs = zip(rnd5_hamming_distances_out,rnd5_iterations_out,rnd5_energies_out)

# mean hamming distances for each probability set
rnd5_mean_ham = np.mean(rnd5_hamming_distances_out)

# mean iterations for each probability set
rnd5_mean_it = np.mean(rnd5_iterations_out)

#==============================================================================
# adding pattern 6
#==============================================================================
rnd_pattern6 = create_random_set(1,16)

Hoppy_mayne.train(rnd_pattern6)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

rnd_training_set.append(rnd_pattern6)

num_bastards = 3
rnd_bastards = []
probs = [.2]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        rnd_bastards.append(create_test_set(rnd_training_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        rnd_training_set = [rnd_pattern1[:],rnd_pattern2[:],rnd_pattern3[:],rnd_pattern4[:],rnd_pattern5[:],rnd_pattern6[:]]
        
rnd6_hamming_distances_out = []
rnd6_iterations_out = []
rnd6_energies_out = []

for i in range(len(rnd_training_set)):
# for each trained pattern
    for j in range(len(rnd_bastards)):
    # for each bastardized training set
        for k in range(len(rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(rnd_bastards[j][k],rnd_training_set[i])
                rnd6_hamming_distances_out.append(H)
                rnd6_iterations_out.append(I)
                rnd6_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
            else:
                Hoppy_mayne.reset_nodes()
                
# pack up the outputs nice and neat
p2_B6_outputs = zip(rnd6_hamming_distances_out,rnd6_iterations_out,rnd6_energies_out)

# mean hamming distances for each probability set
rnd6_mean_ham = np.mean(rnd6_hamming_distances_out)

# mean iterations for each probability set
rnd6_mean_it = np.mean(rnd6_iterations_out)

#==============================================================================
# adding pattern 7
#==============================================================================
rnd_pattern7 = create_random_set(1,16)

Hoppy_mayne.train(rnd_pattern7)
Hoppy_mayne.display_connections()
Hoppy_mayne.reset_nodes()

rnd_training_set.append(rnd_pattern7)

num_bastards = 3
rnd_bastards = []
probs = [.2]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        rnd_bastards.append(create_test_set(rnd_training_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        rnd_training_set = [rnd_pattern1[:],rnd_pattern2[:],rnd_pattern3[:],rnd_pattern4[:],rnd_pattern5[:],rnd_pattern6[:],rnd_pattern7[:]]
        
rnd7_hamming_distances_out = []
rnd7_iterations_out = []
rnd7_energies_out = []

for i in range(len(rnd_training_set)):
# for each trained pattern
    for j in range(len(rnd_bastards)):
    # for each bastardized training set
        for k in range(len(rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run(rnd_bastards[j][k],rnd_training_set[i])
                rnd7_hamming_distances_out.append(H)
                rnd7_iterations_out.append(I)
                rnd7_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
            else:
                Hoppy_mayne.reset_nodes()
                
# pack up the outputs nice and neat
p2_B7_outputs = zip(rnd7_hamming_distances_out,rnd7_iterations_out,rnd7_energies_out)

# mean hamming distances for each probability set
rnd7_mean_ham = np.mean(rnd7_hamming_distances_out)

# mean iterations for each probability set
rnd7_mean_it = np.mean(rnd7_iterations_out)


#==============================================================================
#  PART THREE
#==============================================================================

base_pattern = pattern1[:]

# making sure to not accidentally train on the base pattern
different = False
while different == False:
    init_training_set3 = [base_pattern[:],base_pattern[:],base_pattern[:],
                          base_pattern[:],base_pattern[:],base_pattern[:]]
    training_set3 = create_test_set(init_training_set3,.125)
    
    for i in range(len(training_set3)):
        if training_set3[i] == base_pattern:
            different = False
        else:
            different = True
        
Hoppy_mayne.reset_nodes()
Hoppy_mayne.reset_weights()

Hoppy_mayne.train(training_set3)
Hoppy_mayne.display_connections()

sym_hamming_distances_out = []
sym_iterations_out = []
sym_energies_out = []

for i in range(100):
    H,I,E = Hoppy_mayne.run(base_pattern,base_pattern)
    sym_hamming_distances_out.append(H)
    sym_iterations_out.append(I)
    sym_energies_out.append(E)
    Hoppy_mayne.reset_nodes()
    
mean_sym_ham = np.mean(sym_hamming_distances_out)
mean_sym_its = np.mean(sym_iterations_out)
    
#==============================================================================
#  PART FOUR
#==============================================================================

new_rnd_train_set = create_random_set(4,16)
p4_pattern1 = new_rnd_train_set[0][:]
p4_pattern2 = new_rnd_train_set[1][:]
p4_pattern3 = new_rnd_train_set[2][:]
p4_pattern4 = new_rnd_train_set[3][:]

Hoppy_mayne.reset_nodes()
Hoppy_mayne.reset_weights()

Hoppy_mayne.train(new_rnd_train_set)
Hoppy_mayne.display_connections()

num_bastards = 10
p4_rnd_bastards = []
probs = [.2]

for i in probs:
# iterate through the probabilities
    for j in range(num_bastards):
    # create three bastards based on each probability
        p4_rnd_bastards.append(create_test_set(new_rnd_train_set,i))
        # reset the goddamn training set who retains a divine bond to anything that touches it
        new_rnd_train_set = [p4_pattern1[:],p4_pattern2[:],p4_pattern3[:],p4_pattern4[:]]
        
p4_hamming_distances_out = []
p4_iterations_out = []
p4_energies_out = []

p48_hamming_distances_out = []
p48_iterations_out = []
p48_energies_out = []

p44_hamming_distances_out = []
p44_iterations_out = []
p44_energies_out = []


for i in range(len(new_rnd_train_set)):
# for each trained pattern
    for j in range(len(p4_rnd_bastards)):
    # for each bastardized training set
        for k in range(len(p4_rnd_bastards[0])):
        # for each pattern within each bastardized training set
            if i == k:
            # only test the bastards on the training patterns on which they are based
            # [their desperate attempts to find their long lost fathers]
                # get all this shit that Hummel wants
                H,I,E = Hoppy_mayne.run_all(p4_rnd_bastards[j][k],new_rnd_train_set[i])
                p4_hamming_distances_out.append(H)
                p4_iterations_out.append(I)
                p4_energies_out.append(E)
                Hoppy_mayne.reset_nodes()
                
                H8,I8,E8 = Hoppy_mayne.run_8(p4_rnd_bastards[j][k],new_rnd_train_set[i])
                p48_hamming_distances_out.append(H8)
                p48_iterations_out.append(I8)
                p48_energies_out.append(E8)
                Hoppy_mayne.reset_nodes()

                H4,I4,E4 = Hoppy_mayne.run_4(p4_rnd_bastards[j][k],new_rnd_train_set[i])
                p44_hamming_distances_out.append(H4)
                p44_iterations_out.append(I4)
                p44_energies_out.append(E4)
                Hoppy_mayne.reset_nodes()                
                
            else:
                Hoppy_mayne.reset_nodes()
                
# pack up the outputs nice and neat
p4_B_outputs = zip(p4_hamming_distances_out,p4_iterations_out,p4_energies_out)
p48_B_outputs = zip(p48_hamming_distances_out,p48_iterations_out,p48_energies_out)
p44_B_outputs = zip(p44_hamming_distances_out,p44_iterations_out,p44_energies_out)

# mean hamming distances for each probability set
p4_mean_ham = np.mean(p4_hamming_distances_out)
p48_mean_ham = np.mean(p48_hamming_distances_out)
p44_mean_ham = np.mean(p44_hamming_distances_out)

# mean iterations for each probability set
p4_mean_it = np.mean(p4_iterations_out)
p48_mean_it = np.mean(p48_iterations_out)
p44_mean_it = np.mean(p44_iterations_out)