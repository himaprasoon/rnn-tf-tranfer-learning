# -*- coding: utf-8 -*-
"""
@created on: 9/28/18,
@author: Himaprasoon,
@version: v0.0.1

Description:

Sphinx Documentation Status:

"""
from rnn_tranfer_learning.BasicRNN import save_path
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.ERROR)
tf.set_random_seed(0)
# hyperparameters
n_neurons = 128
learning_rate = 0.001
batch_size = 128
n_epochs = 1
# parameters
n_steps = 28  # 28 rows
n_inputs = 28  # 28 cols
n_outputs = 10  # 10 classes
# build a rnn model
X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.int32, [None])
cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_neurons, name="myrnn")
outputs, state = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
output_transposed = tf.transpose(outputs, [1, 0, 2])
logits = tf.matmul(output_transposed[-1],
                   tf.Variable(name="output", initial_value=tf.random_uniform(shape=(n_neurons, n_outputs))))
# logits = tf.layers.dense(state, n_outputs)

cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
loss = tf.reduce_mean(cross_entropy)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
prediction = tf.nn.in_top_k(logits, y, 1)
accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))

# input data
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/mnsit")
X_test = mnist.test.images  # X_test shape: [num_test, 28*28]
X_test = X_test.reshape([-1, n_steps, n_inputs])
y_test = mnist.test.labels

init = tf.global_variables_initializer()
# train the model
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    n_batches = mnist.train.num_examples // batch_size
    for epoch in range(n_epochs):
        for batch in range(n_batches):
            X_train, y_train = mnist.train.next_batch(batch_size)
            X_train = X_train.reshape([-1, n_steps, n_inputs])
            sess.run(optimizer, feed_dict={X: X_train, y: y_train})
        loss_train, acc_train = sess.run(
            [loss, accuracy], feed_dict={X: X_train, y: y_train})
        print('Epoch: {}, Train Loss: {:.3f}, Train Acc: {:.3f}'.format(
            epoch + 1, loss_train, acc_train))
    loss_test, acc_test = sess.run(
        [loss, accuracy], feed_dict={X: X_test, y: y_test})
    print('Test Loss: {:.3f}, Test Acc: {:.3f}'.format(loss_test, acc_test))
    print(sess.run(logits, feed_dict={X: X_train, y: y_train}))
    save_path = saver.save(sess, save_path + 'model.ckpt')
