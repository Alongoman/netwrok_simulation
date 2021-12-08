# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 9
#######################################################################################################################


def is_in(lst,x):
    res = False
    for elem in lst:
        if elem == x:
            res = True
        if elem > x:
            return res
    return res


if __name__ == "__main__":
    print("sorted list of number :")
    lst = [1,2,3,4,6,8,234,24653]
    print(lst)
    print("num : ",end="")
    x = 3
    print(x)
    print("is "+str(x)+" in given lst ? : "+str(is_in(lst,x)))
    print("num : ",end="")
    x = 7
    print(x)
    print("is "+str(x)+" in given lst ? : "+str(is_in(lst,x)))
