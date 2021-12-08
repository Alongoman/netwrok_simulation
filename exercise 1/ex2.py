# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 2
#######################################################################################################################

def find_divisors(num):
    lst = []
    for n in range(1,num+1):
        if num % n == 0:
            lst.append(n)

    return lst

if __name__ == "__main__":
    stop_cond = False
    timeout = 10
    times = 0
    while not(stop_cond):
        print("please enter a Natural number")
        try:
            num = int(input())
            stop_cond = True
        except ValueError:
            print("number must be Natural , example : 12")
            times += 1
        if times >= timeout:
            print("failed to many times")
            exit(1)

    res = find_divisors(num)
    print("divisors list:")
    print(res)
