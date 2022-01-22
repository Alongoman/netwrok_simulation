'''
Alon Goldamnn Nov 25 2021
Computer exercise 1 - network net_objects
'''

from network_sim import *

class Link(object):
    '''
    link object with capacity and users that are using it
    '''
    def __init__(self, id, capacity=0, src=None, dst=None, users={}):

        self.id = id
        self.cap = capacity
        self.load = 0
        self.local_users = {}
        self.users = {}
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
        return "link {0} | topology {1} <- {0} -> {2} | capacity: {5} , load: {3}% | total {4} users".format(self.id, src_id, dst_id, round(100*self.load/self.cap,2), len(self.users),self.cap)

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
        # if self.load > self.cap:
            # return x*(((self.load/self.cap)-1)**4)
            # return x*(1 + (self.load/self.cap)-1)
        # if x < 0.01:
        #     return 100
        # return 1/x
        return x
