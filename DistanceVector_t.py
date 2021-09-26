# Project 4 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data    
        self.vector  = dict()
        self.vector[self.name] = 0

    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        
        #neighbor_names is also get from incoming link and it is the name already
        for i in self.neighbor_names:
            msg = dict()
            msg['origin'] = self.name
            msg['nodeweight'] = self.vector
            self.send_msg(msg,i)

    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages       
        is_changed = False #send message or not
        
        for msg in self.messages:            
            for i in msg['nodeweight']: #msg has origin and vector with nodeweight
                if i in self.vector and i != self.name:
                    old_weight = int(self.get_outgoing_neighbor_weight(msg['origin']))
                    msg_weight = int(msg['nodeweight'][i])
                    new_weight = int(old_weight + msg_weight)
                    if (old_weight <= -99 or msg_weight <= -99 or new_weight <= -99) and self.vector[i] != -99: # no update if it is already -99
                        is_changed = True
                        self.vector[i] = -99
                    elif self.vector[i] != -99 and new_weight < self.vector[i]:
                        is_changed = True
                        self.vector[i] = new_weight

                elif i not in self.vector and i != self.name:
                    is_changed = True
                    for out in self.outgoing_links:
                        if i == out:
                            new_weight =  int(self.get_outgoing_neighbor_weight(i)) #fist iteration
                            break
                        else:
                            new_weight = int(self.get_outgoing_neighbor_weight(msg['origin'])) + int(msg['nodeweight'][i]) #get to node + node itself
                    self.vector[i] = new_weight
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if is_changed:
            for i in self.neighbor_names:
                msg = dict()
                msg['origin'] = self.name
                msg['nodeweight'] = self.vector
                self.send_msg(msg,i)

    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        result = ''
        for i in self.vector:
            result += str(i) + str(self.vector[i]) + ','
        if len(result) > 0:
            result = result[:-1]
        add_entry(self.name, result)        
