# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        # set root as id of the switch
        self.root = self.switchID
        # initial distance to 0, thus it will be easy to track and for calculating itself to root difference
        self.distance = 0 
        # store all links, either will be True or False
        self.activeLinks = dict()
        # setting default as None - find the root easily and it could be replace easily. 
        self.switchthrough = None
        # setting default value of all links to "False" whenever need to switch - change to "True"
        for x in self.links:
            self.activeLinks[x] = False




    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for x in self.links:
            msg = Message(self.switchID,0,self.switchID,x,False)
            self.send_message(msg)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        # there are no difference in root. no need to modify
        if self.root < message.root:
            self.activeLinks[message.origin] = message.pathThrough
        # here is to show distance difference
        elif self.root == message.root:
            # when root is no difference, compare distance difference
            # 1. greater than
            if self.distance > message.distance + 1:
                self.distance = message.distance + 1
                self.switchThrough = message.origin
                for x in self.links:
                    if x == self.switchthrough:
                        self.activeLinks[x] = True
                        msg = Message(self.root,self.distance,self.switchID,x,True)
                        self.send_message(msg)
                    else:
                        msg = Message(self.root,self.distance,self.switchID,x,False)
                        self.send_message(msg)
            # 2. equal than
            elif self.distance == message.distance + 1:
                if self.switchthrough > message.origin and self.switchthrough is not None:
                    self.switchthrough = message.origin
                    self.activeLinks[self.switchthrough] = True
                    msg = Message(self.root,self.distance,self.switchID,self.switchthrough,True)
                    self.send_message(msg)
                elif self.switchthrough <= message.origin and self.switchthrough is not None:
                    self.activeLinks[message.origin] = message.pathThrough
                else:
                    self.activeLinks[message.origin] = message.pathThrough
            # 3. less than
            else:
                self.activeLinks[message.origin] = message.pathThrough
        # this is to calculate root difference
        elif self.root > message.root:
            self.root = message.root
            self.switchthrough = message.origin
            self.distance = message.distance + 1
            for x in self.links:
                if x == self.switchthrough:
                    self.activeLinks[x] = True
                    msg = Message(self.root,self.distance,self.switchID,x,True)
                    self.send_message(msg)
                    
                else:
                    msg = Message(self.root,self.distance,self.switchID,x,False)
                    self.send_message(msg)
        # it may also include sth else that may not be considered
        else:
            self.activeLinks[message.origin] = message.pathThrough
        return         

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        logs = []
        separator = ', '
        for key, value in sorted(self.activeLinks.items()):
            if value == True:
                logs.append((f"{self.switchID} - {key}"))
            else:
                pass
        # refer to https://www.programiz.com/python-programming/methods/string/join
        return separator.join(logs)