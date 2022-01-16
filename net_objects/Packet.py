'''
Alon Goldamnn Jan 14 2022
network net_objects
'''
from TSOR_sim import *
from datetime import datetime

class Packet(object):
    '''
    Packet of information: ACK, NACK, LACK, LCFM, EXPLORE
    '''
    def __init__(self, src, dst, type, V, origin=None, next_hop=None, TTL=1, num=None):
        self.dst = dst
        self.src = src
        if origin is None:
            origin = src
        self.origin = origin
        self.type = type
        if type is "LACK":
            TTL = 1
        if type is "LCFM":
            TTL = GLOB.TTL
        if type in ["ACK","NACK"]:
            TTL = GLOB.TTL

        if type is not "LCFM":
            next_hop = None

        self.next_hop = next_hop
        self.TTL = TTL
        if num is None:
            now = datetime.now()
            num = now.strftime("%H:%M:%S")

        self.num = num
        self.hop = 0
        self.cost = 0
        self.V = V

    def copy(self):
        now = datetime.now()
        num = now.strftime("%H:%M:%S")
        p = Packet(src=self.src, dst=self.dst, type=self.type, origin=self.origin, next_hop=self.next_hop, V=self.V, num=num)
        p.TTL = self.TTL
        return p

    def __str__(self):
        string = f"{self.type} | {self.src.id} -> {self.dst.id} | origin {self.origin.id} | TTL {self.TTL} | id {self.num}"
        if self.type is "LCFM":
            string = f"{string} | next hop {self.next_hop.id}"
        return string

    def Hop(self):
        self.hop += 1
        self.TTL -= 1
        self.cost = GLOB.c*self.hop
