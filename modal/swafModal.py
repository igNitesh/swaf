import re
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Read the data from the file
with open('modal/dataset/normalTrafficTest.txt', 'r') as file:
    data = file.read()
    test_data = data.split('\n')

with open('modal/dataset/normalTrafficTraining.txt', 'r') as file:
    data = file.read()
    train_data = data.split('\n')

# # Split the data into training and testing sets
# data_lines = test_data.split('\n')
# train_data = data_lines[:len(data_lines) // 2]
# test_data = data_lines[len(data_lines) // 2:]

# Preprocess the data
def preprocess_data(data):
    processed_data = []
    for line in data:
        # Use regular expressions to extract relevant information
        match = re.search(r'(GET|POST) (.+?) HTTP/1\.\d', line)
        if match:
            processed_data.append(match.group(2))
    return processed_data

# Process training and testing data
train_processed = preprocess_data(train_data)
test_processed = preprocess_data(test_data)

# Tokenize the data
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(train_processed)

# Convert text to sequences
train_sequences = tokenizer.texts_to_sequences(train_processed)
test_sequences = tokenizer.texts_to_sequences(test_processed)

# Pad sequences to the same length
max_length = max(len(seq) for seq in train_sequences)
train_padded = tf.keras.preprocessing.sequence.pad_sequences(train_sequences, maxlen=max_length, padding='post')
test_padded = tf.keras.preprocessing.sequence.pad_sequences(test_sequences, maxlen=max_length, padding='post')

# Build the CNN model
model = models.Sequential()
model.add(layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16, input_length=max_length))
model.add(layers.Conv1D(32, kernel_size=3, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=2))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
labels = np.zeros(len(train_data))  # Assuming all data is normal for simplicity
model.fit(train_padded, labels, epochs=5, batch_size=32, validation_split=0.2)

# Evaluate on test data
test_labels = np.zeros(len(test_data))  # Assuming all test data is normal
test_loss, test_accuracy = model.evaluate(test_padded, test_labels)
print(f'Test Accuracy: {test_accuracy * 100:.2f}%')
