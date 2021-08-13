from os import write
import sys
from sklearn import model_selection  
sys.path.insert(0, '../scripts')
import streamlit as st
import numpy as np
import pandas as pd
import modeling
import visualize
import pickle
import librosa
from keras.models import load_model
import tensorflow as tf

# loading the trained model
FEAT_MASK_VALUE = 1e+10
initial_learning_rate = 0.005
momentum = 0.9

model = load_model('../models/RNN.h5')
model.compile(optimizer = tf.keras.optimizers.SGD(initial_learning_rate, momentum))
with open('../data/alphabets_data.json', 'r', encoding='UTF-8') as language_file:
    alphabets = json.load(language_file)

def file_uploader():
    uploaded_file = st.file_uploader("Upload Files",type=['csv'])
    return uploaded_file

def extract_feature(audio,sr):
    input_val = mfcc(audio, samplerate=sr)
    input_val = (input_val - np.mean(input_val)) / np.std(input_val)
    train_input = tf.ragged.constant(input_val, dtype=np.float32)
    train_seq_len = tf.cast(train_input.row_lengths(), tf.int32)
    train_input = train_input.to_tensor(default_value=FEAT_MASK_VALUE)
    return train_input,train_seq_len

@st.cache()  
# defining the function which will make 
# the prediction using data about the users 
def prediction(file):   
    y,sr = librosa.load(file)
    train_input,train_seq_len = extract_feature(y,sr)
    
    decoded, _ = tf.nn.ctc_greedy_decoder(tf.transpose(
        model_predict.predict(train_input), (1, 0, 2)), train_seq_len)

    d = tf.sparse.to_dense(decoded[0], default_value=-1).numpy()
    str_decoded = [''.join([alphabets['num_to_char'][str(x)]
                           for x in np.asarray(row) if x != -1]) for row in d]
    result = ""
    for s in str_decoded:
        s = s.replace(alphabets['num_to_char']['0'], ' ')
        result += s
    return result

    
def main_page():
    st.write('Amharic Speech to Text')
    Store = st.text_input("Upload your audio file")
    file = file_uploader()

    result = ""
    
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(file)
        st.write(result)
        # st.success('The user is {}'.format(result))     
  


     
if __name__=='__main__': 
    main_page()