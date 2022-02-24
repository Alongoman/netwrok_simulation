'''
Alon Goldamnn Jan 13 2022
'''

from enum import IntFlag

class GLOB(IntFlag):
    R = 10
    opt_payoff = 6.2
    c = 1
    N = 6
    TTL = 6
    inf = 10**3
    alpha = 1
    L = 5
    find_short_path = False
    max_plot_rate = 5 # will not save rates higher that that to the net_objects plot
    zero_th = 0.001 # x < zero_th -> x == 0

    print_func = False
    print_progress = True

    ''' Change this field to see the Packet path '''
    print_info = False


class COLOR:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'