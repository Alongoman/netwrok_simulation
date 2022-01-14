'''
Alon Goldamnn Jan 14 2022
network net_objects
'''

class Packet(object):
    '''
    Packet of information: ACK, NACK, LACK, LCFM
    '''
    def __init__(self, src, dst, type, V=None, last_hop=None, next_hop=None, TTL=100, num=None):
        self.dst = dst
        self.src = src
        if last_hop is None:
            last_hop = src
        self.last_hop = last_hop
        self.next_hop = next_hop
        self.type = type
        if type in ["LACK","LCFM"]:
            TTL = 1
        self.TTL = TTL
        self.num = num
        self.hop = 0
        self.V = V

    def copy(self):
        p = Packet(src=self.src, dst=self.dst, type=self.type, V=self.V, last_hop=self.last_hop, next_hop=self.next_hop, TTL=self.TTL, num=self.num)
        return p

    def __str__(self):
        return f"{self.type}: {self.src} -> {self.dst}"

    def SendTo(self, user):
        assert isinstance(user, User)
        user.buffer.append(self)
        user.buffer_head += 1
        self.last_hop = self.next_hop
        self.next_hop = user
        self.TTL -= 1
        self.hop += 1