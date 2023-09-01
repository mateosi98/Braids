import numpy as np
import tensorflow as tf
import sys
import pandas as pd
from ast import literal_eval



def get_braids_labels(strands, length, depth):
    dir_name = "/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Data/"
    file_name = "braid_tree_l"+str(length)+"_s"+str(strands)+"_d"+str(depth)+".csv"
    data = pd.read_csv(dir_name+file_name, converters={'braid':literal_eval,'labels':literal_eval}).drop("Unnamed: 0", axis=1)
    msk = np.random.rand(len(data)) < 0.8
    training_data = data[msk]
    training_braids = training_data['braid'].values.tolist()
    training_labels = [item for sublist in training_data['labels'].values.tolist() for item in sublist]
    testing_data = data[~msk]
    testing_braids = testing_data['braid'].values.tolist()
    testing_labels = [item for sublist in testing_data['labels'].values.tolist() for item in sublist]
    return training_braids, training_labels, testing_braids, testing_labels, data['braid'].values.tolist()

def create_lara(strands, length):
    tf.keras.backend.clear_session()
    lara = tf.keras.models.Sequential([tf.keras.layers.Flatten(), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense((strands*2+4)*length, activation=tf.nn.softmax)])
    lara.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    print('LARA CREATED')
    return lara

def train_lara(lara, train_braids, train_labels, ep=25):
    lara.fit(train_braids, train_labels, epochs=ep)

def test_lara(lara, test_braids, test_labels):
    lara.evaluate(test_braids,test_labels)

def save_lara(lara, strands, length, depth, epoc):
    dir_name = "/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Models/"
    file_name = "lara_l"+str(length)+"_s"+str(strands)+"_d"+str(depth)+"_e"+str(epoc)+".csv"
    lara.save(dir_name+file_name)
    print('LARA SAVED')

def load_lara(strands, length, depth, epoc):
    dir_name = "/Users/mateosallesize/Google Drive/SRO/Braids/Supervised/Models/"
    file_name = "lara_l"+str(length)+"_s"+str(strands)+"_d"+str(depth)+"_e"+str(epoc)+".csv"
    exist = False
    try:
        lara = tf.keras.models.load_model(dir_name+file_name)
        print('LARA LOADED')
        exist = True
    except:
        print('ERROR: LARA NOT LOADED')
        lara = create_lara(strands, length)
    return lara, exist

def action_lara(lara, braid, ver):
    # a = np.argmax(lara.predict([braid], verbose=ver))
    return lara.predict([braid], verbose=ver)


