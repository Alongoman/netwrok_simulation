# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 5
#######################################################################################################################
import random

class Ascii_Table:
    def __init__(self):
        self.nums = list(range(48,58))
        self.lower = list(range(97,123))
        self.upper = list(range(65,91))
        self.symbols = list(range(33,48))+list(range(58,65))+list(range(91,97))+list(range(123,127))
        self.values = [self.nums,self.lower,self.upper,self.symbols]

    def get_index(self,num):
        if num in self.nums:
            return 0
        if num in self.lower:
            return 1
        if num in self.upper:
            return 2
        if num in self.symbols:
            return 3
        return -1


def gen_password(password_length):
    length_whole = password_length - password_length % 4
    max_possibility = length_whole/4
    password=""
    possibilities = [0]*4
    for i in range(password_length):
        times = 0
        seed = random.randint(0,3)
        while (times < timeout_gen) and (possibilities[seed] >= max_possibility) and (sum(possibilities) < length_whole):
            seed = random.randint(0,3)
            times += 1
        password += chr(random.choice(ascii_table.values[seed]))
        possibilities[seed] += 1

    return password

if __name__ == "__main__":
    ascii_table = Ascii_Table()
    timeout_gen = 100
    timeout = 10
    times = 0
    print("generate password? (y/n)")
    generate_again = "y" == input()
    while(generate_again):
        print("choose password length")
        try:
            password_length = int(input())
        except ValueError:
            print("password length must be Natural number")
            times += 1
        if times > timeout:
            print("failed to many times")
            exit(1)
        password = gen_password(password_length)
        print("")
        print("password is: "+password)
        print("")
        print("generate password? (y/n)")
        generate_again = "y" == input()