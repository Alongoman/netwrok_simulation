'''
Alon Goldamnn Nov 25 2021
Computer exercise 1 - network net_objects
'''

import matplotlib.pyplot as plt
from enum import IntFlag


'''############################################ functions ############################################'''

def disp(info):
    if GLOB.print_info:
        print(info)

def GetRatesDiff(rates1, rates2):
    diff = [0]*len(rates1)
    for idx,elem in enumerate(rates1):
        diff[idx] = abs(rates1[idx] - rates2[idx])
    return diff

def GenerateSerialModel(L, capacity=1, alpha=1):
    '''
    total L link and L+1 sources, first source transmit to last source and each other source transmit to next source
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User

    net = NetworkModel(name="serial model (from class)", alpha=alpha)
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
        net.links[u].AddLocalUser(net.users[u+1])
        net.Connect(net.users[0], net.links[u]) # user 0 utilize all links
    net.Connect(net.users[0], net.users[L+1])
    net.Connect(net.users[0], net.links[1])

    return net

def GenerateWebModel(capacity=1, alpha=1):
    '''
    web model like what was given in the lecture
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User

    L = 8
    U = 6
    net = NetworkModel(name="web model (from class)", alpha=alpha)
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
    net.links['ab'].AddLocalUser(net.users['a'])
    net.links['ab'].AddLocalUser(net.users['b'])
    net.links['ad'] = Link(id='ad', capacity=capacity)
    net.links['ad'].AddLocalUser(net.users['a'])
    net.links['ad'].AddLocalUser(net.users['d'])
    net.links['db'] = Link(id='db', capacity=capacity)
    net.links['db'].AddLocalUser(net.users['d'])
    net.links['db'].AddLocalUser(net.users['b'])
    net.links['bc'] = Link(id='bc', capacity=capacity)
    net.links['bc'].AddLocalUser(net.users['b'])
    net.links['bc'].AddLocalUser(net.users['c'])
    net.links['de'] = Link(id='de', capacity=capacity)
    net.links['de'].AddLocalUser(net.users['d'])
    net.links['de'].AddLocalUser(net.users['e'])
    net.links['be'] = Link(id='be', capacity=capacity)
    net.links['be'].AddLocalUser(net.users['b'])
    net.links['be'].AddLocalUser(net.users['e'])
    net.links['cf'] = Link(id='cf', capacity=capacity)
    net.links['cf'].AddLocalUser(net.users['c'])
    net.links['cf'].AddLocalUser(net.users['f'])
    net.links['ef'] = Link(id='ef', capacity=capacity)
    net.links['ef'].AddLocalUser(net.users['e'])
    net.links['ef'].AddLocalUser(net.users['f'])

    net.users['a'].AddLocalLink(net.links['ab'])
    net.users['a'].AddLocalLink(net.links['ad'])
    net.users['b'].AddLocalLink(net.links['ab'])
    net.users['b'].AddLocalLink(net.links['bc'])
    net.users['b'].AddLocalLink(net.links['db'])
    net.users['b'].AddLocalLink(net.links['be'])
    net.users['c'].AddLocalLink(net.links['bc'])
    net.users['c'].AddLocalLink(net.links['cf'])
    net.users['d'].AddLocalLink(net.links['ad'])
    net.users['d'].AddLocalLink(net.links['db'])
    net.users['d'].AddLocalLink(net.links['de'])
    net.users['e'].AddLocalLink(net.links['be'])
    net.users['e'].AddLocalLink(net.links['de'])
    net.users['e'].AddLocalLink(net.links['ef'])
    net.users['f'].AddLocalLink(net.links['cf'])
    net.users['f'].AddLocalLink(net.links['ef'])


    # class example
    net.links['ab'].cost = 3
    net.links['ad'].cost = 2
    net.links['db'].cost = 1
    net.links['de'].cost = 4
    net.links['bc'].cost = 2
    net.links['be'].cost = 1
    net.links['cf'].cost = 2
    net.links['ef'].cost = 2

    net.MapNeighboors()

    return net

def DoAlgorithm(net, name, step=0.01, threshold=0.001, iterations=10**3):
    if name == "Primal":
        net.UpdateRatesPrimaly(step=step, threshold=threshold, iterations=iterations)
    elif name == "Dual":
        net.UpdateRatesDual(step=step, threshold=threshold, iterations=iterations)
    elif name == "Dijkstra":
        net.UpdateRouteDijkstra(step=step, threshold=threshold, iterations=iterations)
    elif name == "BellmanFord":
        net.UpdateRouteBellmanFord(step=step, threshold=threshold, iterations=iterations)
    print("################")
    print("rates are:")
    for user in net.users.values():
        print(user)
    print("new network")
    net.Show()
    net.PlotRates(f"algorithm: {name}")

#
# def DoPrimal(net_objects, step=0.01, threshold=0.001, iterations=10**3):
#     net_objects.UpdateRatesPrimaly(step=step, threshold=threshold, iterations=iterations)
#     print("################")
#     print("rates are:")
#     for user in net_objects.users.values():
#         print(user)
#     print("new network")
#     net_objects.Show()
#     net_objects.PlotRates("algorithm: primal")
#
# def DoDual(net_objects, step=0.01, threshold=0.001, iterations=10**3):
#     net_objects.UpdateRatesDual(step=step, threshold=threshold, iterations=iterations)
#     print("################")
#     print("rates are:")
#     for user in net_objects.users.values():
#         print(user)
#     print("new network")
#     net_objects.Show()
#     net_objects.PlotRates("algorithm: dual")
#
# def DoDijkstra(net_objects, step=0.01, threshold=0.001, iterations=10**3):
#     net_objects.UpdateRouteDijkstra(step=step, threshold=threshold, iterations=iterations)
#     print("################")
#     print("rates are:")
#     for user in net_objects.users.values():
#         print(user)
#     print("new network")
#     net_objects.Show()
#     net_objects.PlotRates("algorithm: dual")
#
#
# def DoBellmanFord(net_objects, step=0.01, threshold=0.001, iterations=10**3):
#     net_objects.UpdateRouteBellmanFord(step=step, threshold=threshold, iterations=iterations)
#     print("################")
#     print("rates are:")
#     for user in net_objects.users.values():
#         print(user)
#     print("new network")
#     net_objects.Show()
#     net_objects.PlotRates("algorithm: dual")

def Model_Serial(step, threshold, iterations, alpha=1):
    net_p = GenerateSerialModel(L=GLOB.L, capacity=1, alpha=alpha)
    net_p.UpdateLinksLoad()
    net_p.Show()
    DoAlgorithm(net_p, name="Primal", step=step, threshold=threshold, iterations=iterations)
    net_d = GenerateSerialModel(L=GLOB.L, capacity=1, alpha=alpha)
    net_d.UpdateLinksLoad()
    DoAlgorithm(net_d, name="Dual", step=step, threshold=threshold, iterations=iterations)
    net_p.Show()

def Model_Web(step, threshold, iterations, alpha=1):
    net_p = GenerateWebModel(capacity=1, alpha=alpha)
    net_p.UpdateLinksLoad()
    net_p.find_short_path = "Dijkstra"
    net_p.Show()
    DoAlgorithm(net_p, name="Dijkstra", step=step, threshold=threshold, iterations=iterations)


    net_d = GenerateWebModel(capacity=1, alpha=alpha)
    net_d.UpdateLinksLoad()
    net_d.find_short_path = "BellmanFord"
    net_d.Show()
    DoAlgorithm(net_d, name="BellmanFord", step=step, threshold=threshold, iterations=iterations)

'''############## Globals ###############'''

class GLOB(IntFlag):
    inf = 10**3
    print_info = True
    L = 5
    find_short_path = False
    max_plot_rate = 5 # will not save rates higher that that to the net_objects plot


if __name__ == "__main__":
    step = 0.01
    threshold = 0.0001
    iterations = 10**3

    Model_Serial(step=step, threshold=threshold, iterations=iterations, alpha=1)
    Model_Serial(step=step, threshold=threshold, iterations=iterations, alpha=2)
    Model_Serial(step=step*10, threshold=threshold*10, iterations=iterations, alpha=3)

    plt.show()

    # net_web = GenerateWebModel(capacity=1)
    #
    # path = net_web.UpdateRouteDijkstra(net_web.users['a'])
    # print(path)
    #
    # path = net_web.UpdateRouteBellmanFord(net_web.users['c'])
    # print(path)