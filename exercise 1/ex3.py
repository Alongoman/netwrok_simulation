# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 3
#######################################################################################################################

def get_input():
    stop_cond = False
    timeout = 10
    times = 0
    while not(stop_cond):
        print("player 1 : choose rock/paper/scissors")
        p1 = input()
        if p1 not in possible_outcomes:
            print("you must choose from either ",end="")
            print(possible_outcomes)
            times += 1
        else:
            while not(stop_cond):
                print("player 2 : choose rock/paper/scissors")
                p2 = input()
                if p1 not in possible_outcomes:
                    print("you must choose from either ",end="")
                    print(possible_outcomes)
                    times += 1
                else:
                    stop_cond = True
        if times >= timeout:
            print("failed to many times")
            exit(1)
    return p1,p2

def find_winner(p1,p2):
    # idx = p2_idx - p1_idx
    winner = {0:"even",1:"p2 wins",-1:"p1 wins",2:"p1 wins",-2:"p2 wins"}
    idx1 = outcomes_dict[p1]
    idx2 = outcomes_dict[p2]
    return winner[idx2-idx1]

if __name__ == "__main__":
    possible_outcomes = {"rock","paper","scissors"}
    outcomes_dict = {"rock":0,"paper":1,"scissors":2}
    play_again = True
    while(play_again):
        p1, p2 = get_input()
        res = find_winner(p1,p2)
        print("")
        print("result is: "+res)
        print("")
        print("play again? (y/n)")
        play_again = "y" == input()
