'''
Alon Goldamnn Nov 25 2021
network net_objects
'''

from home_exercise import *
from TSOR_sim import *
import numpy as np


class Link(object):
    '''
    link object with capacity and users that are using it
    '''
    def __init__(self, id, transmit_prob=1, capacity=0, src=None, dst=None, users={}):

        self.id = id
        self.cap = capacity
        self.load = 0
        self.local_users = {}
        self.users = {}
        self.transmit_prob = transmit_prob
        self.transmit_rand = np.random.binomial(1, transmit_prob)
        for user in users:
            self.Connect(user)
        self.penalty = 0
        self.src = src
        self.dst = dst
        self.cost = 0 # link cost depend on load
        self.lagrange = 1 # link lagrange multiplier

    def __str__(self):
        src_id = " "
        dst_id = " "
        if self.src is not None:
            src_id = self.src.id
        if self.dst is not None:
            dst_id = self.dst.id
        return f"link {self.id} | topology {src_id} <- -> {dst_id} | transmit prob: {round(100*self.transmit_prob)}% "

    def Connect(self,obj):
        from net_objects.User import User
        if isinstance(obj, User):
            self.AddUser(obj)
        elif isinstance(obj, Link):
            self.AddLink(obj)

    def Disconnect(self, obj):
        from net_objects.User import User
        if isinstance(obj, User):
            self.DelUser(obj)
        elif isinstance(obj, Link):
            self.DelLink(obj)

    def AddLink(self, link):
        self.dst = link
        link.src = self

    def DelLink(self, link):
        if self.dst == link:
            self.dst = None
        if self.src == link:
            self.src = None

    def AddUser(self, user):
        self.users[user.id] = user
        self.load += user.rate

    def DelUser(self, user):
        try:
            self.users.pop(user.id)
        except KeyError:
            print("no such user id {} to remove".format(user.id))
            return
        self.load -= user.rate
        user.DelLink()

    def AddLocalUser(self, user):
        self.local_users[user.id] = user

    def DelLocalUser(self, user):
        try:
            self.local_users.pop(user.id)
        except KeyError:
            print("no such user id {} to remove".format(user.id))
            return

    def UpdateLoad(self):
        self.load = 0
        for user in self.users.values():
            self.load += user.rate

    def UpdateCost(self):
        self.cost = 0
        for user in self.users.values():
            self.cost += self.Penalty(user.rate)
        # if self.load > self.cap:
        #     self.cost += ((self.load/self.cap)-1)**2


    def Penalty(self, x):
        if self.load > self.cap:
            return x*(((self.load/self.cap)-1)**4)
        if x < 0.01:
            return 100
        return 1/x

    def Transmit(self, dst, packet):
        if dst.id not in self.local_users:
            print(f"{dst.id} not in reach, dropping packet: {packet}")

        if self.transmit_rand:
            packet.Hop()
            dst.RecivePacket(packet=packet)
            disp(f"PASS: transmit to {dst.id} of packet {packet}")
        else:
            disp(f"FAIL: transmit to {dst.id} of packet {packet}")