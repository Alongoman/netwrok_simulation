# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 7
#######################################################################################################################


def find_max(a,b,c):
    M = a
    if a < b:
        M = b
    if M < c :
        M = c
    return M


if __name__ == "__main__":
    print("choose 1st var")
    a = input()
    print("choose 2nd var")
    b = input()
    print("choose 3rd var")
    c = input()
    print("")
    print("max of these 3 vars is "+find_max(a,b,c))