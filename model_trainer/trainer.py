import tensorflow as tf
from convolutional_model import ConvModel
from dataset import DishDataset

epochs = 30
batch_size = 100  # 100 photos per time

data = DishDataset('data/train')
train_set = data.train_data
test_set = data.test_data
n_batches = len(train_set) // batch_size
n_batches_test = len(test_set) // batch_size

with tf.device('/gpu:0'):
    # model = BasicModel(resolution=[28, 28], channels=1)
    model = ConvModel(resolution=[128, 128], channels=3)

    saver = tf.train.Saver()  # We use this to save the model. Instantiate it after all Variables have been created

    label_placeholder = tf.placeholder(tf.float32, shape=[batch_size, 10])
    loss = tf.losses.softmax_cross_entropy(label_placeholder, model.predictions)
    update = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)

    top_predictions = tf.argmax(model.predictions, axis=1)      # probabilities -> top prediction
    top_labels = tf.argmax(label_placeholder, axis=1)           # one_hot -> number
    correct = tf.equal(top_predictions, top_labels)             # bool Tensor
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))     # Average correct guesses

with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(1, epochs + 1):
        print('Starting epoch %d' % epoch)
        total_epoch_loss = 0

        for i in range(n_batches):
            images, labels = data.sample(batch_size)

            _, l, a = sess.run([update, loss, accuracy],
                               feed_dict={model.input_placeholder: images,
                                          label_placeholder: labels})
            total_epoch_loss += l

            if i % 100 == 0:
                print('[%d / %d] Accuracy: %.2f%%     Loss: %f' % (i+1, n_batches, a*100, l))

        print('Average epoch loss: %f\n' % (total_epoch_loss / n_batches))

    dish_probabilities = tf.nn.softmax(model.predictions, name='prediction')
    tf.add_to_collection('model', dish_probabilities)          # Specify the graph nodes that we want to use later
    tf.add_to_collection('model_inputs', model.input_placeholder)
    saver.save(sess, './saved_models/dish_model.ckpt')               # Save the entire graph and all Variables

    total_epoch_loss = 0
    sum_a = 0
    for i in range(n_batches_test):
        images, labels = data.test_sample(batch_size)

        _, l, a = sess.run([update, loss, accuracy],
                           feed_dict={model.input_placeholder: images,
                                      label_placeholder: labels})
        total_epoch_loss += l

        sum_a += a
        if i == n_batches_test - 1:
            avg_a = sum_a/n_batches_test
            print('Average Test Accuracy: %.2f%%' % (avg_a*100))


