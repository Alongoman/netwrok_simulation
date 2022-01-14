'''
Alon Goldamnn Jan 14 2022
network net_objects
'''
from home_exercise import *
from TSOR_sim import *

class Packet(object):
    '''
    Packet of information: ACK, NACK, LACK, LCFM
    '''
    def __init__(self, src, dst, type, location=None, TTL=100, num=None):
        self.dst = dst
        self.src = src
        if location is None:
            location = src
        self.location = location
        self.type = type
        self.TTL = TTL
        self.num = num
        self.hop = 0

    def __str__(self):
        return f"{self.type}: {self.src} -> {self.dst}"

    def SendTo(self, user):
        assert isinstance(user, User)
        user.packet_queue.append(self)
        user.queue_head += 1