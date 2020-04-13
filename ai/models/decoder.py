import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, features, hidden):
        hidden_with_time_axis = tf.expand_dims(hidden, 1)
        score = tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis))
        attention_weights = tf.nn.softmax(self.V(score), axis=1)

        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class RNN_Decoder(tf.keras.Model):
    def __init__(self, embedding_dim, units, vocab_size):
        super(RNN_Decoder, self).__init__()
        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(self.units,
                                    return_sequences=True,
                                    return_state=True,
                                    recurrent_initializer='glorot_uniform')
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(vocab_size)

        self.attention = BahdanauAttention(self.units)

    def call(self, x, features, hidden):
        context_vector, attention_weights = self.attention(features, hidden)

        x = self.embedding(x)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        output, state = self.gru(x)
        x = self.fc1(output)
        x = tf.reshape(x, (-1, x.shape[2]))
        x = self.fc2(x)

        return x, state, attention_weights

    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))




# # 임베딩 레이어 구현
# model = Sequential()
# model.add(tf.keras.layers.Embedding(input_dim=50, output_dim=64, input_length=10))

# input_array = np.random.randint(50, size=(32, 10))

# model.compile('rmsprop', 'mse')
# output_array = model.predict(input_array)
# assert output_array.shape == (32, 10, 64)
# # print(output_array)

# # The LSTM algorithm will be used here
# VOCAB_SIZE = 0
# WORD_EMBEDDING_DIM = 64
# model = Sequential([
#     tf.keras.layers.Embedding(VOCAB_SIZE, WORD_EMBEDDING_DIM),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dropout(rate=0.2),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# model.compile(
#     loss='binary_crossentropy',
#     optimizer='adam',
#     metrics=['accuracy']
# )

# # Training model
# history = model.fit(
#     training_set,
#     epochs=10,
#     validation_data=validation_set
# )


# # 역 임베딩 레이어 구현; embedding to vocab
# # tf.keras.layers.Dense()
# model = Sequential()
# model.add(tf.keras.layers.Dense(32, input_shape=(16,)))

# model.add(tf.keras.layers.Dense(32))
