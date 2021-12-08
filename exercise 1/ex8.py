# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 8
#######################################################################################################################
import os
cwd = os.getcwd()+"/"

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

def sum_exp_digit(num,base):
    s = 0
    str_num = str(num)
    for digit in str_num:
        s += (int(digit))**base
    return s

def is_happy(num,base,times=500):
    time = 0
    res = num
    while res >= 10:
        time += 1
        res = sum_exp_digit(res,base)
        if (time > times):
            print("couldn't converge")
            return False
    return res == 1

def list_primes(n):
    primes_list = []
    for p in range(1,n+1):
        if is_prime(p):
            primes_list.append(p)
    return primes_list

def list_happy(n):
    happy_list = []
    for i in range(n+1):
        if is_happy(i,2):
            happy_list.append(i)
    return happy_list

def generate_file(path,lst):
    f = open(path,"w")
    i = 0
    while i < (len(lst) - 1):
        f.write(str(lst[i]))
        f.write(",")
        i += 1
    f.write(str(lst[i]))
    f.close()

def find_overlap_nums(path1,path2):
    f1 = open(path1,"r")
    f2 = open(path2,"r")
    overlap_nums = []
    nums_dict = {}
    nums1 = ""
    nums2 = ""
    for line in f1.readlines():
        nums1 += line.replace(' ','').replace('\n','')
    for line in f2.readlines():
        nums2 += line.replace(' ','').replace('\n','')
    f1.close()
    f2.close()
    nums1 = nums1.split(',')
    nums2 = nums2.split(',')
    for num in nums1:
        nums_dict[num] = 1
    for num in nums2:
        if num in nums_dict.keys():
            overlap_nums.append(num)
    return overlap_nums

if __name__ == "__main__":
    file_name1 = "nums_list1.txt"
    file_name2 = "nums_list2.txt"
    file_name_primes = "primes.txt"
    file_name_happy = "happy.txt"
    overlaps_nums = find_overlap_nums(cwd+file_name1,cwd+file_name2)
    print("overlaps :")
    print(overlaps_nums)
    generate_file(cwd+file_name_primes,list_primes(1000))
    generate_file(cwd+file_name_happy,list_happy(1000))


