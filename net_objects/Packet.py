'''
Alon Goldamnn Jan 14 2022
network net_objects
'''
from TSOR_sim import *

class Packet(object):
    '''
    Packet of information: ACK, NACK, LACK, LCFM, EXPLORE
    '''
    def __init__(self, src, dst, type, V, origin=None, next_hop=None, TTL=100, num=None):
        self.dst = dst
        self.src = src
        if origin is None:
            origin = src
        self.origin = origin
        self.type = type
        if type is "LACK":
            TTL = 1
        if type is not "LCFM":
            next_hop = None
        self.next_hop = next_hop
        self.TTL = TTL
        self.num = num
        self.hop = 0
        self.cost = 0
        self.V = V

    def copy(self):
        p = Packet(src=self.src, dst=self.dst, type=self.type, origin=self.origin, next_hop=self.next_hop, V=self.V, TTL=self.TTL, num=self.num)
        return p

    def __str__(self):
        return f"{self.type}: {self.src.id} -> {self.dst.id} | origin {self.origin}"

    def Hop(self):
        self.hop += 1
        self.TTL -= 1
        self.cost = GLOB.c*self.hop

    # def SendTo(self, user):
    #     from net_objects.User import User
    #     assert isinstance(user, User)
    #     self.last_hop = self.next_hop
    #     self.next_hop = user
    #     self.TTL -= 1
    #     self.hop += 1
    #     self.cost = GLOB.c*self.hop
    #     if self.type == "LACK":
    #         user.LACK.append(self)
    #     else:
    #         user.buffer.append(self)
    #
    # def SendLack(self, user):
    #     p = self.copy()
    #     p.TTL = 1
    #     p.last_hop = self.next_hop
    #     p.next_hop = user
    #     p.dst = user
    #     user.LACK.append(p)
