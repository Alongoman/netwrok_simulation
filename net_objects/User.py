'''
Alon Goldamnn Nov 25 2021
network net_objects
'''
from home_exercise import *
from TSOR_sim import *
import numpy as np
from net_objects.Packet import Packet


class User(object):
    '''
    user object with rate and link that is being used
    '''
    def __init__(self, id, num=None, rate=0, dst=None, links={}):
        self.id = id
        if num is None:
            num = int(id)
        self.num = num
        self.rate = rate
        self.dst = dst
        self.cost = 0 # cost to reach destination
        self.lagrange = 0 # lagrange multiplier along route to destination
        self.local_links = {}
        self.links = {}
        for link in links:
            self.Connect(link)
        self.neighbors = {}
        self.link2user = {}
        self.V_dict = {}
        self.V = None
        self.a = {}
        self.b = {}
        self.buffer = []
        self.LACK = set()
        self.buffer_head = 0
        self.Beta = np.random.beta
        self.S = {}
        self.payoff = 0

    def __str__(self):
        dst_id = " "
        if self.dst is not None:
            dst_id = self.dst.id
        return "user {0} | transmission {0} -> {1} | rate {2} ".format(self.id, dst_id, self.rate)

    def Connect(self, obj):
        from net_objects.Link import Link
        if isinstance(obj, User):
            self.AddUser(obj)
        elif isinstance(obj, Link):
            self.AddLink(obj)

    def Disconnect(self, obj):
        from net_objects.Link import Link
        if isinstance(obj, User):
            self.DelUser(obj)
        elif isinstance(obj, Link):
            self.DelLink(obj)

    def AddUser(self, user):
        self.dst = user

    def DelUser(self, user):
        try:
            self.dst.remove(user)
        except KeyError:
            print(f'No such user: "{user.id}"')

    def ClearLinks(self):
        for link in self.links:
            self.Disconnect(link)

    def AddLink(self, link):
        ''' links user is using to transmit with'''
        self.links[link.id] = link
        link.AddUser(self)

    def DelLink(self, link):
        self.links.remove(link.id)
        link.DelUser(self)

    def AddLocalLink(self, link):

        self.local_links[link.id] = link

    def DelLocalLink(self, link):
        try:
            self.local_links.pop(link.id)
        except KeyError:
            print("no such link id {} to remove".format(link.id))
            return

    def GetLink(self, user):
        ''' check wheter or not user is 1 link away from self, if so return the link to it'''
        if user in self.link2user:
            return self.link2user[user]
        for l in self.local_links.values():
            for u in l.local_users.values():
                if u is user:
                    self.link2user[u] = l
                    return l
        return None

    def GetRouteCost(self):
        if not self.links or self.dst is None:
            disp("user {} has no links/dst, no cost".format(self.id))
            return 0
        timeout = 100
        times = 0
        for link in self.links.values():
            self.cost = 0
            link_iter = link
            while(link_iter != None and times < timeout):
                self.cost += link_iter.cost
                if self.dst.id in link_iter.local_users: # got to destination
                    disp("user {} got to dst {} with cost of {}".format(self.id, self.dst.id, self.cost))
                    return self.cost
                link_iter = link_iter.dst
        disp("couldn't reach from user {} to user {}, no link cost".format(self.id, self.dst.id))
        return 0

    def GetRouteLagrange(self):
        if not self.links or self.dst is None:
            disp("user {} has no links/dst, no lagrangians".format(self.id))
            return 0
        timeout = 100
        times = 0
        for link in self.links.values():
            self.lagrange = 0
            link_iter = link
            while(link_iter != None and times < timeout):
                self.lagrange += link_iter.lagrange
                if self.dst.id in link_iter.local_users: # got to destination
                    disp("user {} got to dst {} with lagrangians of {}".format(self.id, self.dst.id, self.lagrange))
                    return self.lagrange
                link_iter = link_iter.dst
        disp("couldn't reach from user {} to user {}, no lagrangians".format(self.id, self.dst.id))
        return 0

    def UpdateNeighbors(self):
        for l_id,link in self.local_links.items():
            for u_id, user in link.local_users.items():
                if user != self:
                    self.AddNeighbor(user)

    def AddNeighbor(self, user):
        self.neighbors[user.id] = user

    def DelNeighbor(self, user):
        if user.id in self.neighbors:
            self.neighbors.pop(user.id)
        else:
            print(f"user {user.id} is not part of user {user.id} neighbors")

    def RecivePacket(self, packet):
        ''' handle inbound packet'''
        if packet.type == "LACK":
            self.LACK.add(packet)
        else:
            self.buffer.append(packet)

    def HandleRecentPacket(self):
        ''' like handle packet but from the most recent one '''
        disp_func(f"func {'HandleRecentPacket'} | user {self.id}")
        if self.buffer_head >= len(self.buffer):
            print(f"no more packets on queue of user {self.id}")
            self.buffer = []
            self.buffer_head = 0
            return False
        packet = self.buffer.pop(-1)
        self.HandlePacket(packet)

    def HandlePacket(self, packet=None):
        '''if return false then there are no more packets in buffer'''
        disp_func(f"func {'HandlePacket'} | user {self.id}")

        if self.LACK:
            disp(f"handling LACKS")
            dict = self.HandleLack()
            return True

        if self.buffer_head >= len(self.buffer) and (not packet):
                disp(f"no more packets on queue of user {self.id}")
                self.buffer = []
                self.buffer_head = 0
                return False

        if not packet:
            packet = self.buffer[self.buffer_head]
            self.buffer_head += 1 # next in queue

        disp(f"user {self.id} handle {packet.type}",color=COLOR.UNDERLINE)

        if (packet.TTL <= 0):
            if packet.type != "LCFM":
                return False
            if packet.TTL < 0:
                return False

        if (packet.type == "LCFM"):
            if (packet.TTL == 0) or ((packet.dst == self) and (packet.next_hop == self)):
                p2 = Packet(src=self, dst=packet.origin, type="ACK", origin=self, V=self.V)
                if ((packet.dst == self) and (packet.next_hop == self)):
                    self.payoff = GLOB.R - packet.cost
                    disp(f"________________ user: {self.id} sending ACK through {packet.src.id} , payoff: {GLOB.R - packet.cost}",color=COLOR.BLUE)
                    if self.payoff > GLOB.R:
                        debug = 0
                else:
                    p2.type = "NACK"
                    disp(f" user: {self.id} sending NACK through {packet.src.id} ")
                self.SendPacket(dst=packet.src, packet=p2)
                return True

        if packet.type in ["ACK","NACK"]:
            self.TSOR2(packet)
        elif packet.type is "LCFM":
            self.TSOR1(packet)

        return True


    def TSOR0(self):
        ''' TSOR init stage '''
        self.InitS()
        self.InitV()

    def TSOR1(self, packet):
        ''' handle first part of TSOR algorithm'''
        disp_func(f"func {'TSOR1'} | user {self.id}")
        # if packet.type != "LACK":
        #     p_lack = self.GenLack(packet)
        #     self.SendPacket(dst=p_lack.dst, packet=p_lack)

        if (packet.type == "LCFM") and ((packet.src in self.neighbors.values()) or (packet.src == self)): # got LCFM from neighbor
            if self == packet.next_hop:
                disp(f" user: {self.id} got LCFM for self from: {packet.src.id}")
                # self.Broadcast(packet=packet,skip=[packet.origin,packet.src])
                for u in self.neighbors.values():
                    # u.HandleRecentPacket()
                    link = self.GetLink(u)
                    if link.transmit_rand: # transmited successfully the LCFM
                        if link.transmit_rand: # successfully got LACK:
                            self.RecivePacket(Packet(src=u,dst=self,origin=u,TTL=0,type="LACK",V=u.V))
                if self.LACK:
                    V_dict = self.HandleLack()
                    packet.V = self.V
                    if (len(V_dict) > 1) and (packet.src in V_dict):
                        V_dict.pop(packet.src) # if got equals LACK dont send packet back from where is came from
                    if (len(V_dict) > 1) and (packet.origin in V_dict):
                        V_dict.pop(packet.origin) # if got equals LACK dont send packet back from where is came from
                    packet.next_hop = self.GetNextHop(V_dict)
                    self.SendPacket(dst=packet.next_hop, packet=packet)

    def HandleLack(self):
        disp_func(f"func {'HandleLack'} | user {self.id}")
        disp(f"user {self.id} handle LACKS",color=COLOR.UNDERLINE)
        lst = []
        V_dict = {}
        while self.LACK:
            packet = self.LACK.pop()
            V_dict[packet.src] = packet.V
            lst.append(str(packet.src.id))
        s = fix_str(lst)
        self.UpdateBetaParams(s)
        return V_dict


    def TSOR2(self, packet):
        ''' handle second part of TSOR algorithm'''
        disp_func(f"func {'TSOR2'} | user {self.id}")
        p_lack = self.GenLack(packet) # lines 4-6 | redundant in simulation?
        self.SendPacket(dst=p_lack.dst, packet=p_lack)

        if (packet.V == self.V_dict[packet.src]):
            return

        if self.id != str(GLOB.N.value):
            self.V_dict[packet.src] = packet.V
            self.UpdateV()

        if packet.dst == self:
            return # got to destination

        p = packet.copy()
        self.Broadcast(packet=p, skip=p.src)



    def GenLack(self, packet):
        ''' generate locak ACK packet '''
        p = Packet(src=self, dst=packet.src, origin=self, type="LACK", V=self.V, TTL=1)
        return p

    def SendPacket(self, dst, packet):
        ''' send p through link to dst '''
        if self != dst:
            packet.V = self.V
            packet.src = self
            link = self.GetLink(dst)
            link.Transmit(dst=dst, packet=packet)

    def Broadcast(self, packet, skip=None):
        ''' will send packet to all neighbors'''
        disp_func(f"func {'Broadcast'} | user {self.id}")
        if not isinstance(skip, list):
            skip = [skip]
        for u_id,u in self.neighbors.items(): # broadcast locally confirmation
            if (u in skip) or (u == self):
                disp(f"user {self.id} not sending packet to {u_id}")
                continue
            p = packet.copy()
            self.SendPacket(dst=u, packet=p)

    def GetNextHop(self, V_dict={}):
        ''' find next hope base on min distance V(n) '''
        disp_func(f"func {'GetNextHop'} | user {self.id}")
        if not V_dict:
            V_dict = self.V_dict
        next = ""
        val = GLOB.inf
        for n,v in V_dict.items():
            if v < val:
                next = n
                val = v
        return next

    def UpdateV(self):
        ''' equation number 6 in article '''
        disp_func(f"func {'UpdateV'} | user {self.id}")
        V = GLOB.c.value
        for s,u_dict in self.S.items():
            V_dict = {}
            for u_id,u in u_dict.items():
                V_dict[u] = u.V
            next = self.GetNextHop(V_dict)
            t = self.Beta(self.a[s], self.b[s])
            V += t*next.V
        self.V = min(0, V)
        self.V = max((-GLOB.R+GLOB.c),self.V)

    def UpdateBetaParams(self, s):
        ''' equation number 5 in article '''
        disp_func(f"func {'UpdateBetaParams'} | user {self.id}")
        for i in self.a:
            if i == s:
                self.a[i] += 1
            else:
                self.b[i] += 1

    def InitS(self):
        ''' initialize all subsets of neighbors '''
        disp_func(f"func {'InitS'} | user {self.id}")
        neighbors = list(self.neighbors.keys())
        for i,n in enumerate(neighbors):
            neighbors[i] = int(n)

        self.S = {}
        S = get_combs(neighbors)
        for el in S:
            self.a[el] = 1
            self.b[el] = 1
            self.S[el] = {}
            for char in el:
                self.S[el][char] = self.neighbors[char]

    def InitV(self):
        ''' init the distance dictionary V(n,n') '''
        disp_func(f"func {'InitV'} | user {self.id}")
        N = str(GLOB.N.value)
        if not self.neighbors:
            self.UpdateNeighbors()
        for u_id, user in self.neighbors.items():
            if u_id == N:
                self.V_dict[user] = -GLOB.R/2
            else:
                self.V_dict[user] = 0
        if self.id == N:
            self.V = -GLOB.R
        else:
            self.V = 0
