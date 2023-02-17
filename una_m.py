import sys
sys.path.insert(0, '/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Code')
import lara_l
from lara_l import *
import braid_env_l
from braid_env_l import *
import random
from imp import reload
reload(lara_l)
reload(braid_env_l)


# strands = 3
# length = 10
# depth = 5

def initialize(epoc, train, strands, length, depth):
    x_train, y_train, x_test, y_test = get_braids_labels(strands, length, depth)
    my_lara, exist = load_lara(strands, length, depth, epoc)
    if train or not exist:
        train_lara(my_lara, x_train, y_train, epoc)
    test_lara(my_lara, x_test, y_test)
    save_lara(my_lara, strands, length, depth, epoc)
    x_test_copy = x_test.copy()
    random.shuffle(x_test_copy)
    return my_lara, x_test_copy

def check_legal_actions(aux, strands, length):
    legal_actions = [0 for i in range((strands*2+4)*length)]
    for action in range(1, (strands*2+4)*length+1):
        pos = action // (strands*2+4)
        move = action % (strands*2+4)
        if pos < len(aux)-1 and move > 0:
            if move < strands*2-1 and aux[pos] == -aux[pos+1] and all(item != 0 for item in aux[pos:pos+2]):
                legal_actions[action] = 1
            if move == strands*2-1 and ((aux[pos] == 0 and aux[pos+1] != 0) or (aux[pos] != 0 and aux[pos+1] == 0)):
                legal_actions[action] = 1
            if move >= strands*2 and pos < len(aux)-2 and all(item != 0 for item in aux[pos:pos+3]) and abs(aux[pos]) == abs(aux[pos+2]):
                if move == strands*2 and aux[pos] == aux[pos+2] and (aux[pos] == aux[pos+1]+1 or aux[pos] == aux[pos+1]-1):
                    legal_actions[action] = 1
                else:
                    if move == strands*2+1 and aux[pos] == aux[pos+1]+1: # strands*2+1
                        legal_actions[action] = 1
                    else:
                        if move == strands*2+2 and aux[pos+1] == aux[pos+2]+1: # strands*2+2
                            legal_actions[action] = 1
                        else:
                            if move == strands*2+3 and aux[pos+1]+1 == aux[pos+2]: # strands*2+3
                                legal_actions[action] = 1
                            else:
                                if move == strands*2+4 and aux[pos]+1 == aux[pos+1]: # strands*2+4
                                    legal_actions[action] = 1
    return legal_actions

def load_outside_test(strands, length):
    dir_name = '/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Data/'
    file_name = "braids_"+str(strands)+"s_"+str(length)+"l"
    try:
        data = pd.read_csv(dir_name + file_name).drop('Unnamed: 0',axis=1)
        data = data.values.tolist()
        print('OUTSIDE BRAIDS LOADED')
    except:
        print('ERROR: OUTSIDE BRAIDS NOT FOUND')
    return data

def proceed_una(my_lara, x_test, test_denom, strands, length):
    root, wins = [0 for i in range(length)], 0
    random.shuffle(x_test)
    not_untangled = []
    for iteration in range(int(len(x_test)/test_denom)):
        braid = x_test[iteration]
        braid_log, done, step = [braid], False, 0
        env = BraidEnv(braid, strands, length)
        while not done:
            legal_actions = check_legal_actions(braid, strands, length)
            softmax_probabilities = action_lara(my_lara, braid, 0)
            max_action = np.argmax(softmax_probabilities)
            # legal_probabilities = np.multiply(legal_actions, softmax_probabilities)  
            index_legal_actions = list(np.where(np.array(legal_actions) == 1)[0])
            if max_action in index_legal_actions:
                action = max_action
            else:
                random.shuffle(index_legal_actions)
                if len(index_legal_actions) > 0:
                    action = index_legal_actions[0]
                else: 
                    print('ILEGAL ACTION')
                    done = True
            braid, executed = env.step(action)
            if np.all(braid == root):
                wins += 1 
                done = True
            if braid in braid_log:
                not_untangled.append(x_test[iteration])
                done = True
            if executed:   
                braid_log.append(braid)
            step += 1
        env.close()
        print('UNA_M,\tProgress:\t{:.3f},\tAccuracy:\t{:.3f}'.format(iteration/int(len(x_test)/test_denom),wins/(iteration+1)))
    return wins/(len(x_test)/test_denom), not_untangled

# epoc = 100
# train_l = False

# my_lara, x_test = initialize(epoc)

# save_lara(my_lara, strands, length, depth, epoc)

# my_lara, x_test = initialize(epoc, train_l)

# x_test_out = load_outside_test(strands, length)

# proceed_una(my_lara, x_test_out, 1, 25)






# x_train, y_train, x_test, y_test = get_braids_labels(strands, length, depth)
# m = create_lara(strands, length)
# train_lara(m, x_train, y_train, 100)
# test_lara(m, x_test, y_test)

# braid = [1,0,0,0,0,0,0,-1]
# env = BraidEnv(braid, strands, length)
# legal = check_legal_actions(env.state)
# np.where(np.array(legal) == 1)[0]
# output = action_lara(m, env.state, 0)
# len(list(output[0]))
# np.argmax(output)
# action = np.argmax(np.multiply(legal,output))
# env.step(action)

# env.close()

# action_lara(m, env.state) // (strands*2+4)

# action_lara(m, env.state) % (strands*2+4)
