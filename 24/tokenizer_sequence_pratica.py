# Importações necessárias
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = [ # Frases
    'I i asdf . $ #',
    '34 54 31234 64',
    '!',
    ''
]

test_data = [
    'test test Test tes',
    'T3st te5t tess te'
]
tokenizer = Tokenizer(num_words = 100, oov_token='<OOV>') # Instanciando o tokenizer 
tokenizer.fit_on_texts(sentences) # Processamento das frases
word_index = tokenizer.word_index # Indexação das palavras
sequences = tokenizer.texts_to_sequences(sentences)
test_sequence = tokenizer.texts_to_sequences(test_data)
padded = pad_sequences(sequences) # adiciona zeros a esqueda para as frases menores que a maior
print(word_index) # saída: {'<OOV>': 1, 'i': 2, 'asdf': 3, '34': 4, '54': 5, '31234': 6, '64': 7}
print(test_sequence) # saída: [[1, 1, 1, 1], [1, 1, 1, 1]]
print(sequences) # saída: [[2, 2, 3], [4, 5, 6, 7], [], []] 
print(padded) # saída [[0 2 2 3]
#                      [4 5 6 7]
#                      [0 0 0 0]
#                      [0 0 0 0]]                 