'''
Alon Goldamnn Nov 25 2021
network net_objects
'''
from home_exercise import *
from TSOR_sim import *
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
        self.V = {}
        self.a = {}
        self.b = {}
        self.packet_queue = []
        self.queue_head = -1

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
        for l in self.local_links.values():
            for u in l.local_users.values():
                if u is user:
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
                self.AddNeighbor(user)

    def AddNeighbor(self, user):
        self.neighbors[user.id] = user

    def DelNeighbor(self, user):
        if user.id in self.neighbors:
            self.neighbors.pop(user.id)
        else:
            print(f"user {user.id} is not part of user {user.id} neighbors")

    def InitV(self):
        if not self.neighbors:
            self.UpdateNeighbors()
        for u_id, user in self.neighbors.items():
            self.V[u_id] = 0
        self.V[self.id] = -GLOB.R

    def GetPacket(self):
        if self.queue_head == len(self.packet_queue)
            print(f"no more packets on queue of user {self.id}")
            self.packet_queue = []
            self.queue_head = -1
            return None

        packet = self.packet_queue[self.queue_head]
        self.queue_head += 1
        packet.TTL -= 1

        if packet.dst == self.id:
            return Packet(src=self.id, dst=packet.src, type="ACK")