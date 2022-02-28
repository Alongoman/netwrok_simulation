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


def combs(xs, i=0):
    if i==len(xs):
        yield ()
        return
    for c in combs(xs,i+1):
        yield c
        yield c+(xs[i],)


def get_combs(iters):
    '''used to get all permotations of elements in list'''
    x = list(combs(iters))
    lst = sorted(x)
    res = set()
    for elem in lst:
        s = fix_str(elem)
        if s:
            res.add(s)
    return res


def fix_str2(lst):
    elem = sorted(lst)
    s = ""
    q = str(elem)[1:-1]
    q = q.replace(" ","")
    q = q.split(",")
    for el in q:
        s += str(el)
    return s


def fix_str(lst):
    q = sorted(lst)
    s = ""
    for el in q:
        s += str(el)
    return s


def GetRatesDiff(rates1, rates2):
    diff = [0]*len(rates1)
    for idx,elem in enumerate(rates1):
        diff[idx] = abs(rates1[idx] - rates2[idx])
    return diff


def disp_warn(info,end="\n"):
    endc = COLOR.ENDC
    print(f"{COLOR.YELLOW}{info}{endc}",end=end)


def disp_progress(info, end="\n", color="",progress=0):
    endc = COLOR.ENDC
    if not color:
        endc = ""
    if GLOB.print_progress:
        passed = "#"*int(progress)
        gap = " "*(100-int(progress))
        progress_bar = "["+passed+gap+"]"
        print ("\033[A                             \033[A")
        print(f"{color}{info}{' '*(60-len(info))}  {progress_bar}{endc}",end=end)


def disp_func(info, end="\n", color=""):
    endc = COLOR.ENDC
    if not color:
        endc = ""
    if GLOB.print_func:
        print(f"{color}{info}{endc}",end=end)


def disp(info,end="\n", color=""):
    endc = COLOR.ENDC
    if not color:
        endc = ""
    if GLOB.print_info:
        print(f"{color}{info}{endc}",end=end)
