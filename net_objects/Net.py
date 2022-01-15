'''
Alon Goldamnn Nov 25 2021
network net_objects
'''

import random
from net_objects.User import User
from net_objects.Link import Link
from net_objects.Packet import Packet
from home_exercise import *
from TSOR_sim import *
import numpy as np

class NetworkModel(object):
    '''
    model of the network, alpha is the fairness parameter >= 0
    '''
    def __init__(self, name, alpha=1, links={}, users={}):
        self.name = name
        self.model_name = ""
        self.alpha = alpha
        self.links = {}
        self.users = {}
        self.rates = [0]*len(users)
        self.plot_rates = [0]*len(users)
        for link in links:
            self.links[link.id] = link
        for user in users:
            self.users[user.id] = user
            self.rates[user.id] = user.rate
        self.MapNeighboors()
        self.find_short_path = False

    def __str__(self):
        return "network model name: '{}' with total {} links and {} users".format(self.name, len(self.links), len(self.users))

    def GetNumberOfUsers(self):
        return len(self.users)

    def Show(self):
        print(self)
        for link in self.links.values():
            print(link)
            print("link users: ",end="")
            for user in link.users.values():
                print("{",end="")
                print(user,end="} ")
            print("")
            print("link dests: ",end="")
            for user in link.local_users.values():
                print("{",end="")
                print(user,end="} ")
            print("\n")

    def Connect(self, obj1, obj2):
        obj1.Connect(obj2)
        self.AddElement(obj1)
        self.AddElement(obj2)

    def AddElement(self, obj):
        if isinstance(obj, User):
            if obj not in self.users:
                self.users[obj.id] = obj
        elif isinstance(obj, Link):
            if obj not in self.links:
                self.links[obj.id] = obj

    def MapNeighboors(self):
        self.neigboors = {}
        for u1 in self.users.values():
            u1.UpdateNeighbors()
            self.neigboors[u1.id] = {}
            for u2 in self.users.values():
                link = u1.GetLink(u2)
                if link and u2 != u1:
                    self.neigboors[u1.id][u2.id] = u2

    def UpdateLinksLoad(self):
        for link in self.links.values():
            link.UpdateLoad()

    def UpdateLinksCost(self):
        for link in self.links.values():
            link.UpdateCost()

    def UpdateRates(self, iter):
        while len(self.rates) <= iter:
            self.rates.append([0]*len(self.users))
            self.plot_rates.append([0]*len(self.users))
        for user in self.users.values():
            x = user.rate
            self.rates[iter][user.num] = x
            if x>GLOB.max_plot_rate:
                x = 0
            self.plot_rates[iter][user.num] = x

    def IteratePrimaly(self, step, iter):
        ''' one iteration of the primal algorithm'''
        user = random.choice(list(self.users.values()))
        while user.dst is None:
            user = random.choice(list(self.users.values()))
        x = user.rate
        disp("user {} rate {}".format(user.id, x))
        if self.find_short_path:
            self.model_name = f"Primal-{self.find_short_path}"
            disp(f"finding 'shortest' path first, algorithm: {self.find_short_path}")
            self.UpdatePath(user)

        x_t = x + (step*(self.utility_tag(x) - user.GetRouteCost()))
        if x_t < 0:
            x_t = 0
        disp("user {} updated rate {}".format(user.id, x_t))
        user.rate = round(x_t,4)
        self.UpdateRates(iter)
        self.UpdateLinksLoad()
        self.UpdateLinksCost()

    def UpdateRatesPrimaly(self, step=0.01, threshold=0.01, iterations=500, iter_thresh=20):
        ''' iterate until grad descent convergence or until timeout'''
        self.model_name = "Primal"
        count = 0
        self.UpdateRates(iter=0)
        self.UpdateLinksLoad()
        self.UpdateLinksCost()
        for i in range(1,iterations):
            disp("###### iter {} ######".format(i))
            self.IteratePrimaly(step=step, iter=i)
            rates_diff = GetRatesDiff(self.rates[i], self.rates[i-1])
            disp("max rate diff {}".format(max(rates_diff)))
            if max(rates_diff) < threshold:
                count += 1
            else:
                count = 0
            if count > iter_thresh: # stop after iter_thresh iterations with no low change
                print("converged after {} iterations".format(i))
                return
        print("timed out after {} iterations".format(iterations))

    def IterateDual(self, step, iter):
        ''' one iteration of the dual algorithm'''
        user = random.choice(list(self.users.values()))
        while user.dst is None:
            user = random.choice(list(self.users.values()))
        disp("user {} rate {}".format(user.id, user.rate))
        if self.find_short_path:
            self.model_name = f"Dual-{self.find_short_path}"
            disp(f"finding 'shortest' path first, algorithm: {self.find_short_path}")
            self.UpdatePath(user)

        x_t = self.inv_utility_tag(user.GetRouteLagrange())
        if x_t < 0:
            x_t = 0
        disp("user {} updated rate {}".format(user.id, x_t))
        user.rate = round(x_t,4)
        self.UpdateRates(iter)
        self.UpdateLinksLoad()
        # update lagrangians for link
        for link in self.links.values():
            lag = link.lagrange
            F = link.load - link.cap
            if lag <= 0:
                F = max(F,0)
            lag_t = lag + step*F
            if lag_t < 0:
                lag_t = 0
            link.lagrange = lag_t

    def UpdateRatesDual(self, step=0.01, threshold=0.01, iterations=500, iter_thresh=20):
        ''' iterate until grad descent convergence or until timeout'''
        self.model_name = "Primal"
        count = 0
        self.UpdateRates(iter=0)
        self.UpdateLinksLoad()
        for i in range(1,iterations):
            disp("###### iter {} ######".format(i))
            self.IterateDual(step=step, iter=i)
            rates_diff = GetRatesDiff(self.rates[i], self.rates[i-1])
            disp("max rate diff {}".format(max(rates_diff)))
            if max(rates_diff) < threshold:
                count += 1
            else:
                count = 0
            if count > iter_thresh: # stop after iter_thresh iterations with no low change
                print("converged after {} iterations".format(i))
                return
        print("timed out after {} iterations".format(iterations))

    def UpdateRouteDijkstra(self, user):
        ''' find min cost and path TO each net_objects node FROM user'''
        node_and_cost = {}
        nodes = [user]
        for u in self.users.values():
            wij = (GLOB.inf,-1, None)
            neighbor_link = user.GetLink(u)
            if neighbor_link:
                wij = (neighbor_link.cost, user.id, neighbor_link.id)
            node_and_cost[u.id] = wij
        node_and_cost[user.id] = (0,user.id,None)
        i=0

        while len(nodes) < len(list(self.users.keys())):
            i+=1
            curr_n = nodes[-1]
            cost = GLOB.inf
            next_link = None
            for l in curr_n.local_links.values():
                for u in l.local_users:
                    if node_and_cost[u][0] > l.cost + node_and_cost[curr_n.id][0]:
                        node_and_cost[u] = (l.cost + node_and_cost[curr_n.id][0], curr_n.id, l.id)
                tmp_l_dst = l.local_users.copy()
                tmp_l_dst.pop(curr_n.id)
                tmp_l_dst = set(tmp_l_dst.values())
                if (cost > l.cost) and (tmp_l_dst.isdisjoint(nodes)):
                    cost = l.cost
                    next_link = l
            if next_link is None:
                for u in self.users.values():
                    if u not in nodes:
                        next_n = u
            else:
                next_n_dict = next_link.local_users.copy()
                next_n_dict.pop(curr_n.id)
                next_n = list(next_n_dict.values())[0]
            nodes.append(next_n)
            disp([x.id for x in nodes])
        return node_and_cost

    def UpdateRouteBellmanFord(self, user):
        ''' find min cost and path FROM each net_objects node TO user'''
        node_and_cost = {}
        curr_nodes = []
        next_nodes = []
        for u in self.users.values():
            wij = (GLOB.inf, -1, None)
            neighbor_link = user.GetLink(u)
            if neighbor_link:
                wij = (neighbor_link.cost, user.id, neighbor_link.id)
                curr_nodes.append(u)
            node_and_cost[u.id] = wij
        node_and_cost[user.id] = (0, user.id, None)

        t = 1
        while t > 0:
            t = 0 # stop condition
            for u in curr_nodes:
                for n in self.neigboors[u.id].values():
                    l = u.GetLink(n)
                    c = node_and_cost[u.id][0] + l.cost
                    if c < node_and_cost[n.id][0]:
                        node_and_cost[n.id] = (c, u.id, l.id)
                        t += 1
                        next_nodes.append(n)
            curr_nodes = next_nodes.copy()
            next_nodes = []

        return node_and_cost

    def UpdatePath(self, user, type=None):
        ''' update shortest path - dijkstra / bellman-ford'''
        if type is None:
            type = self.find_short_path
        dst = user.dst
        if type == "Dijkstra":
            node_and_cost = self.UpdateRouteDijkstra(user)
            self.UpdatePathFromTo(user, dst, node_and_cost)
        elif type == "BellmanFord":
            node_and_cost = self.UpdateRouteBellmanFord(dst)
            self.UpdatePathFromTo(dst, user, node_and_cost)

    def UpdatePathFromTo(self, user, dst, node_and_cost):
        user.ClearLinks()
        u_id = node_and_cost[dst.id][1]
        link = node_and_cost[dst.id][2]
        user.Connect(self.links[link])
        while u_id != user.id:
            link = node_and_cost[u_id][2]
            user.Connect(self.links[link])
            u_id = node_and_cost[u_id][1]

    def utility(self, x):
        if self.alpha == 1:
            return np.log(x)
        return (x**(1-self.alpha))/(1-self.alpha)

    def utility_tag(self, x):
        if x == 0:
            return GLOB.inf
        try:
            res = 1/(x**self.alpha)
        except OverflowError:
            disp("utility tag too large")
            res = GLOB.inf
        return res

    def inv_utility_tag(self, x):
        if x == 0:
            return GLOB.inf
        try:
            res = 1/(x**(1/self.alpha))
        except OverflowError:
            disp("utility tag too large")
            res = GLOB.inf
        return res

    def PlotRates(self, title=""):
        alpha_str = str(self.alpha)
        if self.alpha == GLOB.inf :
            alpha_str = "inf"
        if not(title):
            title = f"Links={len(self.links)}, users={len(self.users)}, alpha={alpha_str}"
        plt.figure()
        plt.plot(self.plot_rates)
        plt.ylabel("Rate")
        plt.xlabel("Iterations")
        plt.title(title)
        plt.suptitle(self.model_name)
        plt.legend(["user {}".format(id) for u,id in enumerate(self.users)])
        plt.show(block=False)

    def TSOR(self, user_id, packet_num=0):
        ''' iterate TSOR from start from user_id until no more packets to route'''

        for u_id,u in self.users.items():
            u.TSOR0()

        src = self.users[user_id]
        dst = src.dst
        packet = Packet(src=src, dst=dst, next_hop=src, origin=src, type="LCFM", V=-GLOB.R, num=packet_num, TTL=10)
        src.RecivePacket(packet)

        lst = [1]*len(self.users)
        while sum(lst) > 0: # still handling packets
            for i, u in enumerate(self.users.values()):
                x = u.HandlePacket()
                if x:
                    lst[i] = 1
                else:
                    lst[i] = 0

        disp(f"done with packet num {packet_num}")