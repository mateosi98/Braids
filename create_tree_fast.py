import pandas as pd

dir_name = "Your dir"
strands = 3
length = 10
depth = 3
df_braid_moves = pd.DataFrame(columns=['braid','moves','labels'])

def unique_tuples(list_of_tuples):
    new_list = []
    for tup in list_of_tuples:
        if tup not in new_list:
            new_list.append(tup)
    return new_list

def new_level(son, position, move, df_braid_moves):
    braid_list = df_braid_moves['braid'].values.tolist()
    new_tuple =  (position,move)
    new_label =  (position*(strands*2+4)+move)
    added = True
    if son in braid_list:
        added = False
    else:
        df_braid_moves.loc[len(braid_list)] = [son, [new_tuple], [new_label]]
    return df_braid_moves, added

def create_tree(length, strands, depth, father, df_braid_moves):
    if depth == 0:
        return 
    else:
        for position in range(length-1):
            if father[position] == 0 and father[position+1] == 0:
                for move in range(1,strands):
                    strand = move
                    son = father.copy()
                    son[position], son[position+1] = strand, -strand
                    strand += 1
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                        create_tree(length, strands, depth-1, son, df_braid_moves)
                for move in range(strands,strands*2-1):
                    strand = move + 1 - strands
                    son = father.copy()
                    son[position], son[position+1] = -strand, strand
                    strand += 1
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                        create_tree(length, strands, depth-1, son, df_braid_moves)
            if (father[position] == 0 and father[position+1] != 0) or (father[position] != 0 and father[position+1] == 0):
                move = strands*2-1
                son = father.copy()
                son[position], son[position+1] = son[position+1], son[position]
                df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                if added:
                    create_tree(length, strands, depth-1, son, df_braid_moves)
            if position < length-2 and all(item != 0 for item in father[position:position+3]) and abs(father[position]) == abs(father[position+2]):
                if father[position] == father[position+2] and (father[position] == father[position+1]+1 or father[position] == father[position+1]-1):
                    move = strands*2
                    son = father.copy()
                    son[position], son[position+1], son[position+2] = son[position+1], son[position], son[position+1]
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                        create_tree(length, strands, depth-1, son, df_braid_moves)
                elif father[position] == father[position+1]+1:
                    move = strands*2+1
                    son = father.copy()
                    son[position], son[position+1], son[position+2] = son[position+2]+1, son[position], son[position+1]
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                        create_tree(length, strands, depth-1, son, df_braid_moves)
                elif father[position+1] == father[position+2]+1:
                    move = strands*2+2
                    son = father.copy()
                    son[position], son[position+1], son[position+2] = son[position+1], son[position+2], son[position]-1
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                      create_tree(length, strands, depth-1, son, df_braid_moves)
                elif father[position+1]+1 == father[position+2]:
                    move = strands*2+3
                    son = father.copy()
                    son[position], son[position+1], son[position+2] = son[position+1], son[position+2], son[position]+1
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                      create_tree(length, strands, depth-1, son, df_braid_moves)
                elif father[position]+1 == father[position+1]:
                    move = strands*2+4
                    son = father.copy()
                    son[position], son[position+1], son[position+2] = son[position+2]-1, son[position], son[position+1]
                    df_braid_moves, added = new_level(son, position, move, df_braid_moves)
                    if added:
                        create_tree(length, strands, depth-1, son, df_braid_moves)

def reduce_word_in_kei_group(w):
    reduced = True
    while(reduced):
        reduced = False
        for i in range(len(w)-1):
            if w[i] == w[i+1]:
                w.pop(i)
                w.pop(i)
                reduced = True
                break

def apply_sigma_negative(i, words):
    (words[i], words[i+1]) = (words[i] + words[i+1] + words[i], words[i])

def apply_sigma_positive(i, words):
    (words[i], words[i+1]) = (words[i+1], words[i+1] + words[i] + words[i+1])

def braid_to_automorphisms(braid, words):
    for s in braid:
        if s > 0:
            apply_sigma_positive(s-1, words)
        elif s < 0:
            apply_sigma_negative(-s-1, words)
    for i in range(len(words)):
        reduce_word_in_kei_group(words[i])

def is_braid_trivial(braid, braid_strands):
    words = [[i] for i in range(1, braid_strands+1)]
    braid_to_automorphisms(braid, words)
    is_trivial = True
    for i in range(braid_strands):
        if words[i] == [i+1]:
            continue
        is_trivial = False
    return is_trivial

create_tree(length, strands, depth, [0 for i in range(length)], df_braid_moves)

df_braid_moves          

braids = df_braid_moves['braid'].values.tolist()
n_t, cont = 0, 0
index_nt = []
for braid in braids:
    try:
        if not is_braid_trivial(braid,4):
            index_nt.append(braids.index(braid))
            cont += 1
            n_t += 1
    except:
        index_nt.append(braids.index(braid))


index_nt
df_braid_moves.loc[index_nt]
print(n_t)

file_name = "braid_tree_l"+str(length)+"_s"+str(strands)+"_d"+str(depth)+".csv"
df_braid_moves.to_csv(dir_name+file_name)


# df_braid_moves = pd.read_csv(dir_name+file_name).drop("Unnamed: 0", axis = 1)

# df_braid_moves

is_braid_trivial([1, 2, 1, -2, -1, 2, -1, 1, -2, -2], 3)
