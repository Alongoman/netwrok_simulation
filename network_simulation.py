'''
Alon Goldamnn Nov 25 2021
Computer exercise 1 - network simulation
'''

import random
import numpy as np
import matplotlib.pyplot as plt

'''############## Globals ###############'''
inf = 10**3
print_info = True
alpha = 2
L = 5
max_plot_rate = 5 # will not save rates higher that that to the net plot

'''############## Classes ###############'''

class User(object):
    '''
    user object with rate and link that is being used
    '''
    def __init__(self, id, rate=0, dst=None, links={}):
        self.id = id
        self.rate = rate
        self.dst = dst
        self.cost = 0 # cost to reach destination
        self.lagrange = 0 # lagrange multiplier along route to destination
        self.dst_links = {}
        self.links = {}
        for link in links:
            self.Connect(link)

    def __str__(self):
        dst_id = " "
        if self.dst is not None:
            dst_id = self.dst.id
        return "user {0} | transmission {0} -> {1} | rate {2} ".format(self.id, dst_id, self.rate)

    def Connect(self, obj):
        if isinstance(obj, User):
            self.AddUser(obj)
        elif isinstance(obj, Link):
            self.AddLink(obj)

    def Disconnect(self, obj):
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


    def AddLink(self, link):
        self.links[link.id] = link
        link.AddUser(self)

    def DelLink(self, link):
        self.links.remove(link.id)
        link.DelUser(self)

    def AddDstLink(self, link):
        self.dst_links[link.id] = link

    def DelDstLink(self, link):
        try:
            self.dst_links.pop(link.id)
        except KeyError:
            print("no such link id {} to remove".format(link.id))
            return

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
                if self.dst.id in link_iter.dst_users: # got to destination
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
                if self.dst.id in link_iter.dst_users: # got to destination
                    disp("user {} got to dst {} with lagrangians of {}".format(self.id, self.dst.id, self.lagrange))
                    return self.lagrange
                link_iter = link_iter.dst
        disp("couldn't reach from user {} to user {}, no lagrangians".format(self.id, self.dst.id))
        return 0

class Link(object):
    '''
    link object with capacity and users that are using it
    '''
    def __init__(self, id, capacity=0, src=None, dst=None, users={}):
        self.id = id
        self.cap = capacity
        self.load = 0
        self.dst_users = {}
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
        return "link {0} | topology {1} <- {0} -> {2} | load: {3}% | total {4} users".format(self.id, src_id, dst_id, round(100*self.load/self.cap,2), len(self.users))

    def Connect(self,obj):
        if isinstance(obj, User):
            self.AddUser(obj)
        elif isinstance(obj, Link):
            self.AddLink(obj)

    def Disconnect(self, obj):
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

    def AddDstUser(self, user):
        self.dst_users[user.id] = user

    def DelDstUser(self, user):
        try:
            self.dst_users.pop(user.id)
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
        if self.load > self.cap:
            self.cost += (self.load/self.cap-1)**2


    def Penalty(self, x):
        return x


class NetworkModel(object):
    '''
    model of the network, alpha is the fairness parameter >= 0
    '''
    def __init__(self, name, alpha=1, links={}, users={}):
        self.name = name
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

    def __str__(self):
        return "network model name: '{}' with total {} links and {} users".format(self.name, len(self.links), len(self.users))

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
            for user in link.dst_users.values():
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
            self.rates[iter][user.id] = x
            if x>max_plot_rate:
                x = 0
            self.plot_rates[iter][user.id] = x


    def IteratePrimaly(self, step, iter):
        ''' one iteration of the primal algorithm'''
        user = random.choice(list(self.users.values()))
        while user.dst is None:
            user = random.choice(list(self.users.values()))
        x = user.rate
        disp("user {} rate {}".format(user.id, x))
        x_t = x + (step*(utility_tag(x) - user.GetRouteCost()))
        if x_t < 0:
            x_t = 0
        disp("user {} updated rate {}".format(user.id, x_t))
        user.rate = round(x_t,4)
        self.UpdateRates(iter)
        self.UpdateLinksLoad()
        self.UpdateLinksCost()

    def UpdateRatesPrimaly(self, step=0.01, threshold=0.01, iterations=500, iter_thresh=20):
        ''' iterate until grad descent convergence or until timeout'''
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
        x_t = inv_utility_tag(user.GetRouteLagrange())
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
        node_and_cost = {}
        nodes = [user]
        for u in self.users.values():
            node_and_cost[u.id] = (inf,-1)
        node_and_cost[user.id] = (0,user.id)

        while len(nodes) < len(list(self.users.keys())):
            curr_n = nodes[-1]
            cost = inf
            next_link = None
            for l in curr_n.dst_links.values():
                for u in l.dst_users:
                    if node_and_cost[u][0] > l.cost + node_and_cost[curr_n.id][0]:
                        node_and_cost[u] = (l.cost + node_and_cost[curr_n.id][0], curr_n.id)
                tmp_l_dst = l.dst_users.copy()
                tmp_l_dst.pop(curr_n.id)
                tmp_l_dst = set(tmp_l_dst.values())
                if (cost > l.cost) and (tmp_l_dst.isdisjoint(nodes)):
                    cost = l.cost
                    next_link = l

            next_n_dict = next_link.dst_users.copy()
            next_n_dict.pop(curr_n.id)
            next_n = list(next_n_dict.values())[0]
            nodes.append(next_n)
            disp([x.id for x in nodes])

        return node_and_cost

    def UpdateRouteBellmanFord(self):
        node_and_cost = {}


        return node_and_cost


    def PlotRates(self, title=""):
        alpha_str = str(alpha)
        if alpha == inf :
            alpha_str = "inf"
        plt.figure()
        plt.plot(self.plot_rates)
        plt.ylabel("Rate")
        plt.xlabel("Iterations")
        plt.title("L = {} alpha = {}".format(L, alpha_str))
        plt.suptitle(title)
        plt.legend(["user {}".format(i) for i in range(len(self.plot_rates[0]))])
        plt.show(block=False)

'''############################################ functions ############################################'''

def disp(info):
    if print_info:
        print(info)

def utility(x):
    if alpha == 1:
        return np.log(x)
    return (x**(1-alpha))/(1-alpha)

def utility_tag(x):
    if x == 0:
        return inf
    try:
        res = 1/(x**alpha)
    except OverflowError:
        disp("utility tag too large")
        res = inf
    return res

def inv_utility_tag(x):
    if x == 0:
        return inf
    try:
        res = 1/(x**(1/alpha))
    except OverflowError:
        disp("utility tag too large")
        res = inf
    return res

def GetRatesDiff(rates1, rates2):
    diff = [0]*len(rates1)
    for idx,elem in enumerate(rates1):
        diff[idx] = abs(rates1[idx] - rates2[idx])
    return diff

def GenerateSerialModel(L, capacity=1):
    '''
    total L link and L+1 sources, first source transmit to last source and each other source transmit to next source
    '''
    net = NetworkModel("serial model (from class)")
    print("building model named '{}'".format(net.name))
    print("generating {} links and {} users".format(L,L+1))
    net.users[0] = User(id=0, rate=capacity/2)
    for l in range(1, L+1):
        net.links[l] = Link(id=l, capacity=capacity)
        net.users[l] = User(id=l, rate=capacity/2)
    net.users[L+1] = User(id=L+1,rate=0)

    print("connecting links")
    for l in range(1, L): # connect links
        net.Connect(net.links[l],net.links[l+1])

    print("connecting users")
    for u in range(1,L+1): # connect users
        net.Connect(net.users[u], net.users[u+1])
        net.Connect(net.users[u], net.links[u])
        net.links[u].AddDstUser(net.users[u+1])
        net.Connect(net.users[0], net.links[u]) # user 0 utilize all links
    net.Connect(net.users[0], net.users[L+1])
    net.Connect(net.users[0], net.links[1])

    return net

def GenerateWebModel(capacity=1):
    '''
    web model like what was given in the lecture
    '''
    L = 8
    U = 6
    net = NetworkModel("web model (from class)")
    print("building model named '{}'".format(net.name))
    print("generating {} links and {} users".format(L,U))

    net.users['a'] = User(id='a', rate=capacity/2)
    net.users['b'] = User(id='b', rate=capacity/2)
    net.users['c'] = User(id='c', rate=capacity/2)
    net.users['d'] = User(id='d', rate=capacity/2)
    net.users['e'] = User(id='e', rate=capacity/2)
    net.users['f'] = User(id='f', rate=capacity/2)

    net.users['a'].Connect(net.users['f'])
    net.users['b'].Connect(net.users['d'])
    net.users['c'].Connect(net.users['e'])
    net.users['d'].Connect(net.users['c'])
    net.users['e'].Connect(net.users['a'])
    net.users['f'].Connect(net.users['d'])

    net.links['ab'] = Link(id='ab', capacity=capacity)
    net.links['ab'].AddDstUser(net.users['a'])
    net.links['ab'].AddDstUser(net.users['b'])
    net.links['ad'] = Link(id='ad', capacity=capacity)
    net.links['ad'].AddDstUser(net.users['a'])
    net.links['ad'].AddDstUser(net.users['d'])
    net.links['db'] = Link(id='db', capacity=capacity)
    net.links['db'].AddDstUser(net.users['d'])
    net.links['db'].AddDstUser(net.users['b'])
    net.links['bc'] = Link(id='bc', capacity=capacity)
    net.links['bc'].AddDstUser(net.users['b'])
    net.links['bc'].AddDstUser(net.users['c'])
    net.links['de'] = Link(id='de', capacity=capacity)
    net.links['de'].AddDstUser(net.users['d'])
    net.links['de'].AddDstUser(net.users['e'])
    net.links['be'] = Link(id='be', capacity=capacity)
    net.links['be'].AddDstUser(net.users['b'])
    net.links['be'].AddDstUser(net.users['e'])
    net.links['cf'] = Link(id='cf', capacity=capacity)
    net.links['cf'].AddDstUser(net.users['c'])
    net.links['cf'].AddDstUser(net.users['f'])
    net.links['ef'] = Link(id='ef', capacity=capacity)
    net.links['ef'].AddDstUser(net.users['e'])
    net.links['ef'].AddDstUser(net.users['f'])

    net.users['a'].AddDstLink(net.links['ab'])
    net.users['a'].AddDstLink(net.links['ad'])
    net.users['b'].AddDstLink(net.links['ab'])
    net.users['b'].AddDstLink(net.links['bc'])
    net.users['b'].AddDstLink(net.links['db'])
    net.users['b'].AddDstLink(net.links['be'])
    net.users['c'].AddDstLink(net.links['bc'])
    net.users['c'].AddDstLink(net.links['cf'])
    net.users['d'].AddDstLink(net.links['ad'])
    net.users['d'].AddDstLink(net.links['db'])
    net.users['d'].AddDstLink(net.links['de'])
    net.users['e'].AddDstLink(net.links['be'])
    net.users['e'].AddDstLink(net.links['de'])
    net.users['e'].AddDstLink(net.links['ef'])
    net.users['f'].AddDstLink(net.links['cf'])
    net.users['f'].AddDstLink(net.links['ef'])


    # class example
    net.links['ab'].cost = 3
    net.links['ad'].cost = 2
    net.links['db'].cost = 1
    net.links['de'].cost = 4
    net.links['bc'].cost = 2
    net.links['be'].cost = 1
    net.links['cf'].cost = 2
    net.links['ef'].cost = 2

    return net

def DoPrimal(net, step=0.01, threshold=0.001, iterations=10**3):
    net.UpdateRatesPrimaly(step=step, threshold=threshold, iterations=iterations)
    print("################")
    print("rates are:")
    for user in net.users.values():
        print(user)
    print("new network")
    net.Show()
    net.PlotRates("algorithm: primal")

def DoDual(net, step=0.01, threshold=0.001, iterations=10**3):
    net.UpdateRatesDual(step=step, threshold=threshold, iterations=iterations)
    print("################")
    print("rates are:")
    for user in net.users.values():
        print(user)
    print("new network")
    net.Show()
    net.PlotRates("algorithm: dual")

def Model(step, threshold, iterations, alp):
    global alpha
    alpha = alp
    net_p = GenerateSerialModel(L=L, capacity=1)
    net_p.UpdateLinksLoad()
    net_p.Show()
    DoPrimal(net_p, step=step, threshold=threshold, iterations=iterations)
    net_d = GenerateSerialModel(L=L, capacity=1)
    net_d.UpdateLinksLoad()
    DoDual(net_d, step=step, threshold=threshold, iterations=iterations)
    net_p.Show()


if __name__ == "__main__":
    step = 0.01
    threshold = 0.0001
    iterations = 10**3

    # Model(step=step, threshold=threshold, iterations=iterations, alp=1)
    # Model(step=step, threshold=threshold, iterations=iterations, alp=2)
    # Model(step=step*10, threshold=threshold*10, iterations=iterations, alp=inf)

    plt.show()

    net_web = GenerateWebModel(capacity=1)
    path = net_web.UpdateRouteDijkstra(net_web.users['a'])
    print(path)