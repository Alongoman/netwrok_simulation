'''
Alon Goldamnn Jan 13 2022
TSOR simulation
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

def GenerateSmallWirelessModel(capacity=1, rate=1, alpha=1):
    '''
    wireless model 6 nodes
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User
    L = 11
    U = 6
    net = NetworkModel(name="TSOR 6 nodes", alpha=alpha)
    print(f"building model named '{net.name}'")
    print(f"generating {L} links and {U} users")

    net.users['1'] = User(id='1', rate=rate, num=1)
    net.users['2'] = User(id='2', rate=rate, num=2)
    net.users['3'] = User(id='3', rate=rate, num=3)
    net.users['4'] = User(id='4', rate=rate, num=4)
    net.users['5'] = User(id='5', rate=rate, num=5)
    net.users['6'] = User(id='6', rate=rate, num=6)

    net.users['1'].Connect(net.users['6'])
    net.users['6'].Connect(net.users['1'])

    net.links['12'] = Link(id='12', capacity=capacity)
    net.links['12'].AddLocalUser(net.users['1'])
    net.links['12'].AddLocalUser(net.users['2'])
    net.links['13'] = Link(id='13', capacity=capacity)
    net.links['13'].AddLocalUser(net.users['1'])
    net.links['13'].AddLocalUser(net.users['3'])
    net.links['14'] = Link(id='14', capacity=capacity)
    net.links['14'].AddLocalUser(net.users['1'])
    net.links['14'].AddLocalUser(net.users['4'])
    net.links['15'] = Link(id='15', capacity=capacity)
    net.links['15'].AddLocalUser(net.users['1'])
    net.links['15'].AddLocalUser(net.users['5'])

    net.links['23'] = Link(id='23', capacity=capacity)
    net.links['23'].AddLocalUser(net.users['2'])
    net.links['23'].AddLocalUser(net.users['3'])
    net.links['24'] = Link(id='24', capacity=capacity)
    net.links['24'].AddLocalUser(net.users['2'])
    net.links['24'].AddLocalUser(net.users['4'])
    net.links['25'] = Link(id='25', capacity=capacity)
    net.links['25'].AddLocalUser(net.users['2'])
    net.links['25'].AddLocalUser(net.users['5'])
    net.links['26'] = Link(id='26', capacity=capacity)
    net.links['26'].AddLocalUser(net.users['2'])
    net.links['26'].AddLocalUser(net.users['6'])

    net.links['34'] = Link(id='34', capacity=capacity)
    net.links['34'].AddLocalUser(net.users['3'])
    net.links['34'].AddLocalUser(net.users['4'])
    net.links['35'] = Link(id='35', capacity=capacity)
    net.links['35'].AddLocalUser(net.users['3'])
    net.links['35'].AddLocalUser(net.users['5'])
    net.links['36'] = Link(id='36', capacity=capacity)
    net.links['36'].AddLocalUser(net.users['3'])
    net.links['36'].AddLocalUser(net.users['6'])

    net.links['45'] = Link(id='45', capacity=capacity)
    net.links['45'].AddLocalUser(net.users['4'])
    net.links['45'].AddLocalUser(net.users['5'])

    net.users['1'].AddLocalLink(net.links['12'])
    net.users['1'].AddLocalLink(net.links['13'])
    net.users['1'].AddLocalLink(net.links['14'])
    net.users['1'].AddLocalLink(net.links['15'])

    net.users['2'].AddLocalLink(net.links['12'])
    net.users['2'].AddLocalLink(net.links['23'])
    net.users['2'].AddLocalLink(net.links['24'])
    net.users['2'].AddLocalLink(net.links['25'])
    net.users['2'].AddLocalLink(net.links['26'])

    net.users['3'].AddLocalLink(net.links['13'])
    net.users['3'].AddLocalLink(net.links['23'])
    net.users['3'].AddLocalLink(net.links['34'])
    net.users['3'].AddLocalLink(net.links['35'])
    net.users['3'].AddLocalLink(net.links['36'])

    net.users['4'].AddLocalLink(net.links['14'])
    net.users['4'].AddLocalLink(net.links['24'])
    net.users['4'].AddLocalLink(net.links['34'])
    net.users['4'].AddLocalLink(net.links['45'])

    net.users['5'].AddLocalLink(net.links['15'])
    net.users['5'].AddLocalLink(net.links['25'])
    net.users['5'].AddLocalLink(net.links['35'])
    net.users['5'].AddLocalLink(net.links['45'])

    net.users['6'].AddLocalLink(net.links['26'])
    net.users['6'].AddLocalLink(net.links['36'])

    for l_id,l in net.links.items():
        l.cost = 1

    net.MapNeighboors()

    return net

def DoTSOR(net, step=0.01, threshold=0.001, iterations=10**3):
    print("network links:")
    net.Show()
    print("################")
    print("rates are:")
    for user in net.users.values():
        print(user)
    net.PlotRates(f"TSOR - {net.GetNumberOfUsers()} nodes")


def Model(step, threshold, iterations, size=6):
    if size == 6:
        net_p = GenerateSmallWirelessModel(capacity=1,rate=1, alpha=GLOB.alpha)
        net_p.Show()
        DoTSOR(net_p, step=step, threshold=threshold, iterations=iterations)
    if size == 60:
        net_p = GenerateBigWirelessModel(capacity=10,rate=1, alpha=GLOB.alpha)
        net_p.UpdateLinksLoad()
        net_p.find_short_path = "Dijkstra"
        net_p.Show()
        DoTSOR(net_p, step=step, threshold=threshold, iterations=iterations)

'''############## Globals ###############'''

class GLOB(IntFlag):
    R = 1
    inf = 10**3
    alpha = 1
    print_info = True
    L = 5
    find_short_path = False
    max_plot_rate = 5 # will not save rates higher that that to the net_objects plot
    zero_th = 0.001 # x < zero_th -> x == 0


if __name__ == "__main__":
    step = 0.001
    threshold = 0.001
    iterations = 2*10**3

    Model(step=step, threshold=threshold, iterations=iterations, size=6)


    plt.show()
