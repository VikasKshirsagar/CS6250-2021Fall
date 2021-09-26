# Distance Vector project for CS 6250: Computer Networks
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
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        self.dist_vector= {self.name: 0} # create a dictionary to store distance(vector). init as 0

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py

        for neighbor in self.neighbor_names: 
            # since Node.py requests node format, dictionary of name and vector will be stored in msg
            msg = {'sender': self.name, 'dist':self.dist_vector} 
            # update send_msg with new dictionary and its neighbor
            self.send_msg(msg,neighbor)

    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages       

        updated_status = False  # whether status is getting updated or not
        
        for msg in self.messages:
            for name, value in msg.items():
                if name == 'dist':
                    for i in value:
                        if i in self.dist_vector:
                            if i != self.name:
                                new_distance = int(self.get_outgoing_neighbor_weight(msg['sender'])) + int(msg[name][i])
                                if (int(self.get_outgoing_neighbor_weight(msg['sender'])) <= -99 and self.dist_vector[i] != -99) or (int(msg[name][i]) <= -99 and self.dist_vector[i] != -99) or (new_distance <= -99 and self.dist_vector[i] != -99):
                                    updated_status = True
                                    self.dist_vector[i] = -99
                                if self.dist_vector[i] != -99:
                                    if new_distance < self.dist_vector[i]:
                                        updated_status = True
                                        self.dist_vector[i] = new_distance
                        if i not in self.dist_vector:
                            if i != self.name:
                                updated_status = True
                                for outgoing in self.outgoing_links:
                                    if i != outgoing:
                                    	new_distance = int(self.get_outgoing_neighbor_weight(msg['sender'])) + int(msg[name][i])
                                    else:
                                        new_distance =  int(self.get_outgoing_neighbor_weight(i))
                                        break
                                self.dist_vector[i] = new_distance

        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances               
        if updated_status == True:
            for neighbor in self.neighbor_names:
                msg = {'sender': self.name, 'dist':self.dist_vector}
                self.send_msg(msg,neighbor)
    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided. 
               
        result_str = '' # init result as str
        for node_nms in sorted(self.dist_vector):   # in order to pass 1130 cases from student, then sorted() was needed.
            result_str = result_str + node_nms + str(self.dist_vector[node_nms]) + ','
        result_str = result_str[:-1]
        add_entry(self.name, result_str) 
