import lara
from lara import *
import braid_env
from braid_env import *
import random
from imp import reload
reload(lara)
reload(braid_env)


# strands = 3
# length = 8
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
    for iteration in range(int(len(x_test)/test_denom)):
        braid = x_test[iteration]
        braid_log, done, step = [braid], False, 0
        env = BraidEnv(braid, strands, length)
        while not done:
            action = action_lara(my_lara, braid, 0)
            braid, executed = env.step(action)
            if np.all(braid == root):
                wins += 1 
                done = True
            if braid in braid_log:
                done = True
            if executed:   
                braid_log.append(braid)
            step += 1
        env.close()
        print('UNA,\tProgress:\t{:.3f},\tAccuracy:\t{:.3f}'.format(iteration/int(len(x_test)/test_denom),wins/(iteration+1)))
    return wins/(len(x_test)/test_denom)

epoc = 100
train_l = False

# my_lara, x_test = initialize(epoc)

# save_lara(my_lara, strands, length, depth, epoc)

# my_lara, x_test = initialize(epoc, train_l)

# x_test_out = load_outside_test(strands, length)

# proceed_una(my_lara, x_test_out, 1)





# x_train, y_train, x_test, y_test = get_braids_labels(strands, length, depth)
# m = create_lara(strands, length)
# train_lara(m, x_train, y_train, 10)
# test_lara(m, x_test, y_test)

# braid = [1,-1,0,0,0,0,0,0]
# env = BraidEnv(braid, strands, length)
# env.step(action_lara(m, env.state))

# env.close()

# action_lara(m, env.state) // (strands*2+4)

# action_lara(m, env.state) % (strands*2+4)
