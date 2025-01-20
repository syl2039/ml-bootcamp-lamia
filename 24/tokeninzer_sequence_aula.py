# Importações necessárias
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = [ # Frases
    'I love my dog',
    'I love my cat',
    'You love my dog!',
    'Do you think my dog is amazing?'
]

test_data = [
    'I really love my dog',
    'My dog loves my manatee'
]
tokenizer = Tokenizer(num_words = 100, oov_token='<OOV>') # Instanciando o tokenizer 
tokenizer.fit_on_texts(sentences) # Processamento das frases
word_index = tokenizer.word_index # Indexação das palavras
sequences = tokenizer.texts_to_sequences(sentences)
test_sequence = tokenizer.texts_to_sequences(test_data)
padded = pad_sequences(sequences) # adiciona zeros a esqueda para as frases menores que a maior
print(word_index) # saída: {'<OOV>': 1, 'my': 2, 'love': 3, 'dog': 4, 'i': 5, 'you': 6, 'cat': 7, 'do': 8, 'think': 9, 'is': 10, 'amazing': 11}
print(test_sequence) # saída: [[5, 1, 3, 2, 4], [2, 4, 1, 2, 1]]
print(sequences) # saída: [[4, 2, 1, 3], [4, 2, 1, 6], [5, 2, 1, 3], [7, 5, 8, 1, 3, 9, 10]]
print(padded) # saída [[ 0  0  0  5  3  2  4]
#                      [ 0  0  0  5  3  2  7]
#                      [ 0  0  0  6  3  2  4]
#                      [ 8  6  9  2  4 10 11]]                     