'''
Alon Goldamnn Nov 25 2021
Computer exercise 1 - network net_objects
'''

import matplotlib.pyplot as plt
from utils import *


def Model_Web(step, threshold, iterations, alpha=1):
    net_p = GenerateWebModel(capacity=10,rate=2, alpha=alpha)
    net_p.UpdateLinksLoad()
    net_p.find_short_path = "Dijkstra"
    net_p.Show()
    DoAlgorithm(net_p, name="Primal", step=step, threshold=threshold, iterations=iterations)

    net_p = GenerateWebModel(capacity=1, alpha=alpha)
    net_p.UpdateLinksLoad()
    net_p.find_short_path = "Dijkstra"
    net_p.Show()
    DoAlgorithm(net_p, name="Dual", step=step, threshold=threshold, iterations=iterations)


    net_d = GenerateWebModel(capacity=1, alpha=alpha)
    net_d.UpdateLinksLoad()
    net_d.find_short_path = "BellmanFord"
    net_d.Show()
    DoAlgorithm(net_d, name="Primal", step=step, threshold=threshold, iterations=iterations)

    net_d = GenerateWebModel(capacity=1, alpha=alpha)
    net_d.UpdateLinksLoad()
    net_d.find_short_path = "BellmanFord"
    net_d.Show()
    DoAlgorithm(net_d, name="Dual", step=step, threshold=threshold, iterations=iterations)


def GenerateSerialModel(L, capacity=1, alpha=1):
    '''
    total L link and L+1 sources, first source transmit to last source and each other source transmit to next source
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User

    net = NetworkModel(name="serial model (from class)", alpha=alpha, topology="serial")
    print("building model named '{}'".format(net.name))
    print("generating {} links and {} users".format(L,L+1))
    net.users[0] = User(id=0, rate=capacity/2)
    for l in range(1, L+1):
        net.links[l] = Link(id=l, capacity=capacity, print_usage=True)
        net.users[l] = User(id=l, rate=capacity/2, num=l)
    net.users[L+1] = User(id=L+1,rate=0, num=L+1)

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


def GenerateWebModel(capacity=1, rate=1, alpha=1):
    '''
    web model like what was given in the lecture
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User
    L = 8
    U = 6
    net = NetworkModel(name="user made", alpha=alpha, topology="web")
    print("building model named '{}'".format(net.name))
    print("generating {} links and {} users".format(L,U))

    net.users['a'] = User(id='a', rate=rate, num=0)
    net.users['b'] = User(id='b', rate=rate, num=1)
    net.users['c'] = User(id='c', rate=rate, num=2)
    net.users['d'] = User(id='d', rate=rate, num=3)
    net.users['e'] = User(id='e', rate=rate, num=4)
    net.users['f'] = User(id='f', rate=rate, num=5)

    net.users['a'].Connect(net.users['f'])
    net.users['b'].Connect(net.users['d'])
    net.users['c'].Connect(net.users['e'])
    net.users['d'].Connect(net.users['c'])
    net.users['e'].Connect(net.users['a'])
    net.users['f'].Connect(net.users['d'])

    net.links['ab'] = Link(id='ab', capacity=capacity, print_usage=True)
    net.links['ab'].AddLocalUser(net.users['a'])
    net.links['ab'].AddLocalUser(net.users['b'])
    net.links['ad'] = Link(id='ad', capacity=capacity, print_usage=True)
    net.links['ad'].AddLocalUser(net.users['a'])
    net.links['ad'].AddLocalUser(net.users['d'])
    net.links['db'] = Link(id='db', capacity=capacity, print_usage=True)
    net.links['db'].AddLocalUser(net.users['d'])
    net.links['db'].AddLocalUser(net.users['b'])
    net.links['bc'] = Link(id='bc', capacity=capacity, print_usage=True)
    net.links['bc'].AddLocalUser(net.users['b'])
    net.links['bc'].AddLocalUser(net.users['c'])
    net.links['de'] = Link(id='de', capacity=capacity, print_usage=True)
    net.links['de'].AddLocalUser(net.users['d'])
    net.links['de'].AddLocalUser(net.users['e'])
    net.links['be'] = Link(id='be', capacity=capacity, print_usage=True)
    net.links['be'].AddLocalUser(net.users['b'])
    net.links['be'].AddLocalUser(net.users['e'])
    net.links['cf'] = Link(id='cf', capacity=capacity, print_usage=True)
    net.links['cf'].AddLocalUser(net.users['c'])
    net.links['cf'].AddLocalUser(net.users['f'])
    net.links['ef'] = Link(id='ef', capacity=capacity, print_usage=True)
    net.links['ef'].AddLocalUser(net.users['e'])
    net.links['ef'].AddLocalUser(net.users['f'])

    # net.users['a'].AddLocalLink(net.links['ab'])
    # net.users['a'].AddLocalLink(net.links['ad'])
    # net.users['b'].AddLocalLink(net.links['ab'])
    # net.users['b'].AddLocalLink(net.links['bc'])
    # net.users['b'].AddLocalLink(net.links['db'])
    # net.users['b'].AddLocalLink(net.links['be'])
    # net.users['c'].AddLocalLink(net.links['bc'])
    # net.users['c'].AddLocalLink(net.links['cf'])
    # net.users['d'].AddLocalLink(net.links['ad'])
    # net.users['d'].AddLocalLink(net.links['db'])
    # net.users['d'].AddLocalLink(net.links['de'])
    # net.users['e'].AddLocalLink(net.links['be'])
    # net.users['e'].AddLocalLink(net.links['de'])
    # net.users['e'].AddLocalLink(net.links['ef'])
    # net.users['f'].AddLocalLink(net.links['cf'])
    # net.users['f'].AddLocalLink(net.links['ef'])


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


def GetCostumeUsers():
    '''get users from input'''
    from net_objects.User import User

    users = {}
    users_dst = {}
    print("choose users with this structure:")
    print("ID,destination_ID(use '-' for no destination),rate")
    flag = input("enter new user? [y/n]: ")
    u_num = 0
    while flag == "y":
        in_user = input("new user (ID,destination_ID,rate) : ")
        user = in_user.split(",")
        id = user[0]
        dst = user[1]
        rate = int(user[2])
        if dst == "-":
            dst = None
        if dst:
            users_dst[id] = dst
        users[id] = User(id=id, rate=rate, num=u_num)
        u_num += 1
        print()
        flag = input("enter new user? [y/n]: ")

    return users, users_dst


def GetCostumeLinks():
    '''get links from input'''
    from net_objects.Link import Link

    links = {}
    links_local_users = {}
    print("choose links with this structure:")
    print("ID,capacity,all connected users i.e. [1|4|7|5]")
    flag = input("enter new link? [y/n]: ")
    while flag == "y":
        in_link = input("new link (ID,capacity,[connected users]) : ")
        link = in_link.split(",")
        id = link[0]
        cap = int(link[1])
        links_local_users[id] = link[2][1:-1].split("|")
        links[id] = Link(id=id, capacity=cap, print_usage=True)
        print()
        flag = input("enter new link? [y/n]: ")

    return links, links_local_users


def GenerateCostumeModel():
    '''user made model, users/link are list of tuples with all relevant information'''
    from net_objects.Net import NetworkModel

    alpha = int(input("choose alpha > 0. alpha = ? : "))
    users, users_dst = GetCostumeUsers()
    print()
    print("_____________________________________")
    print()
    links, links_local_users = GetCostumeLinks()
    L = len(links)
    U = len(users)
    net = NetworkModel(name="user made model (from class)", alpha=alpha, topology="costume")
    print("building model named '{}'".format(net.name))
    print("generating {} links and {} users".format(L,U))

    net.users = users
    net.links = links

    for u_id,dst_id in users_dst.items():
        dst = net.users[dst_id]
        user = net.users[u_id]
        if user and dst:
            net.Connect(user,dst)

    for l_id,vals in links_local_users.items():
        for u_id in vals:
            net.links[l_id].AddLocalUser(users[u_id])

    net.MapNeighboors()
    net.find_short_path = "Dijkstra"
    net.UpdateAllPaths()

    print()
    print("the network that generated:")
    net.Show()
    print()
    print("_____________________________________")
    print()
    proceed = input("would you like to proceed with this network? [y/n]: ")
    if proceed != "y":
        exit(1)
    return net


def DoAlgorithm(net, name, step=0.01, threshold=0.001, iterations=10**3):
    if name == "Primal":
        net.UpdateRatesPrimaly(step=step, threshold=threshold, iterations=iterations)
    elif name == "Dual":
        net.UpdateRatesDual(step=step, threshold=threshold, iterations=iterations)
    print("################")
    print("rates are:")
    for user in net.users.values():
        print(user)
    print("new network")
    net.Show()


def Model_PrimalDual(step, threshold, iterations, alpha=1, net=None):
    if not net:
        net_p = GenerateSerialModel(L=GLOB.L, capacity=1, alpha=alpha)
    else:
        net_p = net

    net_p.UpdateLinksLoad()
    DoAlgorithm(net_p, name="Primal", step=step, threshold=threshold, iterations=iterations)
    net_p.model_name += f" - Primal"

    if not net:
        net_d = GenerateSerialModel(L=GLOB.L, capacity=1, alpha=alpha)
    else:
        net_d = net

    net_d.UpdateLinksLoad()
    DoAlgorithm(net_d, name="Dual", step=step, threshold=threshold, iterations=iterations)
    net_d.model_name += f" - Dual"

    return net_p,net_d


def Model_Dijkstra(step, threshold, iterations, alpha=1, net=None):
    '''model network rates update but find shortest path with dijkstra first'''
    if not net:
        net_d1 = GenerateWebModel(rate=0.1, capacity=2, alpha=alpha)
    else:
        net_d1 = net

    net_d1.UpdateLinksLoad()

    net_d1.find_short_path = "Dijkstra"
    net_d1.UpdateAllPaths()

    DoAlgorithm(net_d1, name="Primal", step=step, threshold=threshold, iterations=iterations)
    net_d1.model_name = f"Dijkstra - Primal"

    if not net:
        net_d2 = GenerateWebModel(rate=0.1, capacity=2, alpha=alpha)
    else:
        net_d2 = net

    net_d2.UpdateLinksLoad()

    net_d2.find_short_path = "Dijkstra"
    net_d2.UpdateAllPaths()

    DoAlgorithm(net_d2, name="Dual", step=step, threshold=threshold, iterations=iterations)
    net_d2.model_name = f"Dijkstra - Dual"

    return net_d1,net_d2


def Model_BellmanFord(step, threshold, iterations, alpha=1, net=None):
    '''model network rates update but find shortest path with bellman-ford first'''
    if not net:
        net_b1 = GenerateWebModel(rate=0.1, capacity=5, alpha=alpha)
    else:
        net_b1 = net
    net_b1.UpdateLinksLoad()

    net_b1.find_short_path = "BellmanFord"
    net_b1.UpdateAllPaths()

    DoAlgorithm(net_b1, name="Primal", step=step, threshold=threshold, iterations=iterations)
    net_b1.model_name = f"BellmanFord - Primal"


    if not net:
        net_b2 = GenerateWebModel(rate=0.1, capacity=5, alpha=alpha)
    else:
        net_b2 = net
    net_b2.UpdateLinksLoad()

    net_b2.find_short_path = "BellmanFord"
    net_b2.UpdateAllPaths()

    DoAlgorithm(net_b2, name="Dual", step=step, threshold=threshold, iterations=iterations)
    net_b2.model_name = f"BellmanFord - Dual"

    return net_b1,net_b2


if __name__ == "__main__":
    step = 0.001
    threshold = 0.000
    iterations = 10*10**3

    costume_net = None
    costume_topo = input("generate costume topology [y/n] ?: ")
    if costume_topo == "y":
        costume_net = GenerateCostumeModel()


    print("enter question number to solve from {4,5,6}. if you want more than 1 then you can enter: '4,6'")
    print("question 4: Primal and Dual algorithm")
    print("question 5: find shortest path using Dijkstra then do 4")
    print("question 6: find shortest path using Bellman-Ford then do 4")
    question = input("solve question number: ")
    questions = set()
    q_tmp = question.split(',')
    for q in q_tmp:
        questions.add(int(q))

    print(f"solving questions: {questions}")

    if 4 in questions:
        net_p1,net_d1 = Model_PrimalDual(step=step, threshold=threshold, iterations=iterations, alpha=1, net=costume_net)
        net_p1.Show()
        net_p1.PlotRates()
        net_d1.Show()
        net_d1.PlotRates()

        net_p2,net_d2 = Model_PrimalDual(step=step, threshold=threshold, iterations=iterations, alpha=2, net=costume_net)
        net_p2.Show()
        net_p2.PlotRates()
        net_d2.Show()
        net_d2.PlotRates()

        net_p_inf,net_d_inf = Model_PrimalDual(step=step, threshold=threshold, iterations=iterations, alpha=GLOB.inf, net=costume_net)
        net_p_inf.Show()
        net_p_inf.PlotRates()
        net_d_inf.Show()
        net_d_inf.PlotRates()

    if 5 in questions:
        net_p_dijkstra,net_d_dijkstra = Model_Dijkstra(step=step, threshold=threshold, iterations=iterations, alpha=1, net=costume_net)
        net_p_dijkstra.Show()
        net_p_dijkstra.PlotRates()
        net_d_dijkstra.Show()
        net_d_dijkstra.PlotRates()

    if 6 in questions:
        net_p_BF,net_d_BF = Model_BellmanFord(step=step, threshold=threshold, iterations=iterations, alpha=4, net=costume_net)
        net_p_BF.Show()
        net_p_BF.PlotRates()
        net_d_BF.Show()
        net_d_BF.PlotRates()

    plt.show()


