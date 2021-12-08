# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 1
#######################################################################################################################
from datetime import datetime

def age100year(age):
    now = datetime.now()
    year = int(now.strftime("%Y"))
    return (year+100-age),year

if __name__ == "__main__":
    stop_cond = False
    timeout = 10
    times = 0
    print("enter your name:")
    name = input()
    while not(stop_cond):
        print(name+", please enter your age")
        try:
            age = int(input())
            stop_cond = True
        except ValueError:
            print("age must be a Natural number, example : 12")
            times += 1
        if times >= timeout:
            print("failed to many times")
            exit(1)
    res, now = age100year(age)
    if res>now:
        print(name+", you will be 100 years old in "+str(res))
    elif res<now:
        print(name+", you were 100 years old in "+str(res))
    else:
        print(name+", you will\were be 100 years old on this year: "+str(res))