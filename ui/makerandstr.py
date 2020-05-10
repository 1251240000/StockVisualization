from random import randint
def make_rand_str(l):
    res = chr(randint(65,90))
    for i in range(l-1):
        t = randint(0,2)
        if t == 0:
            res += chr(randint(48,57))
        elif t == 1:
            res += chr(randint(65,90))
        elif t == 2:
            res += chr(randint(97,122))
            
    return res

