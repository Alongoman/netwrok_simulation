# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 10
#######################################################################################################################


def is_sum_in(lst,x):
    for i in range(len(lst)-1):
        n1 = lst[i]
        for j in range(i+1,len(lst)):
            n2 = lst[j]
            if (n1+n2) == x:
                return True
    return False


if __name__ == "__main__":
    print("unsorted list of number :")
    lst = [1,2,3,4,6,8,234,24653]
    print(lst)
    print("num : ",end="")
    x = 3
    print(x)
    print(" is given lst have 2 nums that sum to " +str(x)+" ? : "+str(is_sum_in(lst,x)))
    print("num : ",end="")
    x = 78
    print(x)
    print(" is given lst have 2 nums that sum to " +str(x)+" ? : "+str(is_sum_in(lst,x)))
