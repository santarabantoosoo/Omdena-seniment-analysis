from tensorflow.keras import regularizers
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot


def word_dictionary(text):
    text = set(list(text))
    dictionary = {}
    for i, word in enumerate(text):
        dictionary[word] = i

    return dictionary

def predict(text, model, tokenize, vocab, maxlen):
    text, _, _ = tokenize(text)
    vector, temp = [], []
    for d in text:
        for i in d:
            temp.extend(one_hot(i, vocab))
        vector.append(temp)
        temp=[]
    vector = pad_sequences(vector, maxlen=maxlen, padding="post")
    return vector

def get_model(X, y, vocab_size, embedding_size, maxlen, method):
    if method == "simpleRNN":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(SimpleRNN(64,return_sequences=True))
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
    
    elif method == "bidRNN":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(Bidirectional(LSTM(64, activation='relu')))
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))

    elif method == "1DConv":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(Conv1D(20, 6, activation='relu',kernel_regularizer=regularizers.l1_l2(l1=2e-3, l2=2e-3),bias_regularizer=regularizers.l2(2e-3)))
        model.add(MaxPooling1D(5))
        model.add(Dropout(0.2))
        model.add(Conv1D(20, 6, activation='relu',kernel_regularizer=regularizers.l1_l2(l1=2e-3, l2=2e-3),bias_regularizer=regularizers.l2(2e-3)))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(1, activation='sigmoid'))

    elif method == "lstm":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(LSTM(64, activation='relu'))
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))

    return model
