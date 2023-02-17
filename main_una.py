import sys
sys.path.insert(0, '/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Code')
import una
import una_l
import una_b
import una_m
import una_s
from imp import reload
reload(una)
reload(una_l)
reload(una_m)
reload(una_b)
reload(una_s)

strands = 3
length = 8
depths = [3,5]
# depth = 6

epoc = 100
test_denom = 1
train_l = True

accuracy_una = {}

x_test_out = una.load_outside_test(strands, length)

################# UNA #####################

# my_lara, x_test = una.initialize(epoc, train_l, strands, length, depth)

# accuracy_una['una'] = una.proceed_una(my_lara, x_test_out, test_denom, strands, length)

for depth in depths:

    ################# UNA BENCHMARK #####################

    my_lara, x_test = una_b.initialize(epoc, train_l, strands, length, depth)

    accuracy_una['una_b_'+str(depth)] = una_b.proceed_una(my_lara, x_test_out, test_denom, strands, length)

    ################# UNA MIDDLE #####################

    my_lara, x_test = una_m.initialize(epoc, train_l, strands, length, depth)

    accuracy_una['una_m_'+str(depth)], not_untangled = una_m.proceed_una(my_lara, x_test_out, test_denom, strands, length)

    ################# UNA LEGAL #####################

    my_lara, x_test = una_l.initialize(epoc, train_l, strands, length, depth)

    accuracy_una['una_l_'+str(depth)] = una_l.proceed_una(my_lara, x_test_out, test_denom, strands, length)

    ################# UNA SEARCCH #####################

    my_lara, x_test, x_all = una_s.initialize(epoc, train_l, strands, length, depth)

    accuracy_una['una_s_'+str(depth)], not_untangled = una_s.proceed_una(my_lara, x_test_out, x_all, test_denom, strands, length)


# untangled = []
# for i in x_test_out:
#     if i not in not_untangled:
#         untangled.append(i)

# trm = []
# for u in untangled:
#     if u[:3] == [1,2,1]:
#         trm.append(u)

# trm


