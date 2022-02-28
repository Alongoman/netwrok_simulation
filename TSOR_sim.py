'''
Alon Goldamnn Jan 13 2022
TSOR simulation
'''

import matplotlib.pyplot as plt
import time
import json
from utils import *


def GenerateSmallWirelessModel(capacity=1, rate=1, alpha=1):
    '''
    wireless model 6 nodes
    '''
    from net_objects.Net import NetworkModel
    from net_objects.Link import Link
    from net_objects.User import User
    from net_objects.Packet import Packet

    L = 11
    U = 6
    net = NetworkModel(name="TSOR 6 nodes", alpha=alpha)
    disp(f"building model named '{net.name}'")
    disp(f"generating {L} links and {U} users")

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


def Model(size=6):
    '''generate the wirless networks as described in the article'''
    if size == 6:
        net_p = GenerateSmallWirelessModel(capacity=1,rate=1, alpha=GLOB.alpha)

    elif size == 60:
        net_p = GenerateBigWirelessModel(capacity=10,rate=1, alpha=GLOB.alpha)

    net_p.MapNeighboors()

    return net_p


def get_time_remained(time_remained):
    hours = str(time_remained//3600)
    minutes = str((time_remained%3600)//60)
    seconds = str(time_remained%60)
    if len(seconds) == 1:
        seconds = "0"+seconds
    if len(minutes) == 1:
        minutes = "0"+minutes
    if len(hours) == 1:
        hours = "0"+hours

    return hours,minutes,seconds


def DoTSOR(size=6, user_id='1'):
    '''
    this will run the TSOR algorithm for N iterations.
    each iteration, new link probability are generated as described in the TSOR article
    '''

    start = time.time()
    print("################")
    print("nodes:")
    avg_payoff = [0]*len(max_packet_list)
    avg_regret = [GLOB.opt_payoff]*len(max_packet_list)
    packets = max_packet_list

    if load_results:
        with open(load_file, 'r') as f:
            avg_payoff = json.load(f)
    else:
        for l in range(iteration_num):
            net = Model(size=size)
            for k,p in enumerate(max_packet_list):
                done_presentage = round(100*(k + l*len(max_packet_list))/(len(max_packet_list)*iteration_num),1) + 1e-5
                time_remained = int(((time.time()-start)/done_presentage)*(100-done_presentage))
                hours,minutes,seconds = get_time_remained(time_remained)
                done_presentage = round(done_presentage,1)

                payoff = net.TSOR(user_id=user_id, max_packet=p)
                disp_progress(f"_____________ ETA {hours}:{minutes}:{seconds} (h:m:s) | {done_presentage}% _____________",color=COLOR.HEADER,progress=done_presentage)
                avg_payoff[k] += (round(payoff/iteration_num,4))

    for k,p in enumerate(avg_payoff):
        avg_regret[k] -= p

    if save_results:
        f_name = f"net size {size}, iterations {iteration_num}, max packet count {max_packet_list[-1]}, packet samples {len(max_packet_list)}.json"
        with open(f_name, 'w') as f:
            json.dump(avg_payoff, f, indent=2)


    end = time.time()
    print(avg_payoff)
    print(avg_regret)
    minutes = (end-start)//60
    secs = (end-start)%60
    if not minutes:
        time_string = f"{secs} seconds"
    else:
        if len(str(secs)) == 1:
            secs = f"0{secs}"
        time_string = f"{minutes}:{secs} minutes"

    plt_suptitle = f"Average Payoff"
    plt_title = f"Net size={size} iterations={iteration_num}"
    disp(f"time passed: {time_string}",color=COLOR.BLUE)
    plt.figure()
    plt.plot(packets,avg_payoff, label="average payoff", color="orange")
    plt.legend()
    plt.title(plt_title)
    plt.suptitle(plt_suptitle)
    plt.xlabel("Number of Packets")
    plt.ylabel("Average Payoff")
    plt.ylim([0,8])

    plt_suptitle = f"Average Regret"
    plt_title = f"Net size={size} iterations={iteration_num}"
    disp(f"time passed: {time_string}",color=COLOR.BLUE)
    plt.figure()
    plt.plot(packets,avg_regret, label="average regret")
    plt.legend()
    plt.title(plt_title)
    plt.suptitle(plt_suptitle)
    plt.xlabel("Number of Packets")
    plt.ylabel("Average Regret")
    plt.ylim([0,7])
    plt.show()

    plt.show()

    return avg_payoff


if __name__ == "__main__":
    print("choose packet count range")
    start = int(input("start number: "))
    stop = int(input("stop number: "))
    step = int(input("step size: "))
    iteration_num = int(input("iteration number: "))

    load_results = False
    save_results = False
    load_file = "TSOR_results/net size 6, iterations 100, max packet count 1485, packet samples 100.json"
    max_packet_list = [i for i in range(start, stop, step)]
    size = 6

    avg_payoff = DoTSOR(size=size,user_id="1")



