import sys
from gym import Env


class BraidEnv(Env):

    def __init__(self, initial_braid, strands, length):
        self.initial_braid = initial_braid
        self.state = initial_braid
        self.strands = strands
        self.length = length
        self.trivial_braid = [0 for i in range(length)]
        self.executed = False
        self.time = 0
    
    def step(self, action):
        aux = self.state.copy()
        pos = action // (self.strands*2+4)
        move = action % (self.strands*2+4)
        executed = False
        if move < self.strands*2-1 and aux[pos] == -aux[pos+1]:
            aux[pos], aux[pos+1] = 0, 0
        if move == self.strands*2-1 and ((aux[pos] == 0 and aux[pos+1] != 0) or (aux[pos] != 0 and aux[pos+1] == 0)):
            aux[pos], aux[pos+1] = aux[pos+1], aux[pos]
        if move >= self.strands*2 and pos < len(aux)-2 and all(item != 0 for item in aux[pos:pos+3]) and abs(aux[pos]) == abs(aux[pos+2]):
            if move == self.strands*2 and aux[pos] == aux[pos+2] and (aux[pos] == aux[pos+1]+1 or aux[pos] == aux[pos+1]-1):
                aux[pos], aux[pos+1], aux[pos+2] = aux[pos+1], aux[pos], aux[pos+1]
            else:
                if move == self.strands*2+2 and aux[pos] == aux[pos+1]+1: # strands*2+1
                    aux[pos], aux[pos+1], aux[pos+2] = aux[pos+2]+1, aux[pos], aux[pos+1]
                else:
                    if move == self.strands*2+1 and aux[pos+1] == aux[pos+2]+1: # strands*2+2
                        aux[pos], aux[pos+1], aux[pos+2] = aux[pos+1], aux[pos+2], aux[pos]-1
                    else:
                        if move == self.strands*2+4 and aux[pos+1]+1 == aux[pos+2]: # strands*2+3
                            aux[pos], aux[pos+1], aux[pos+2] = aux[pos+1], aux[pos+2], aux[pos]+1
                        else:
                            if move == self.strands*2+3 and aux[pos]+1 == aux[pos+1]: # strands*2+4
                                aux[pos], aux[pos+1], aux[pos+2] = aux[pos+2]+1, aux[pos], aux[pos+1]
        if aux != self.state:
            executed = True
        self.state = aux.copy()
        return self.state, executed



