# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 4
#######################################################################################################################

def get_input():
    stop_cond = False
    timeout = 10
    times = 0
    while not(stop_cond):
        print("choose a Natural number")
        try:
            num = int(input())
            stop_cond = True
        except ValueError:
            print("please choose Natural number, example : 12")
        if times >= timeout:
            print("failed to many times")
            exit(1)
    return num

def find_divisors(num):
    lst = []
    for n in range(2,num):
        if num % n == 0:
            lst.append(n)

    return lst

def is_prime(num):
    divs = find_divisors(num)
    if len(divs) > 0:
        return False
    return True

if __name__ == "__main__":
    num = get_input()
    isprime = is_prime(num)
    print("")
    if isprime:
        print(str(num)+" is a prime number")
    else:
        print(str(num)+" is not a prime number")