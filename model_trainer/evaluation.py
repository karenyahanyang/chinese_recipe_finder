import tensorflow as tf
from dataset import DishDataset
›
with tf.Session() as sess:
    saver = tf.train.import_meta_graph('saved_models/dish_model.ckpt.meta', clear_devices=True)      # Don't have to recreate the entire graph
    saver.restore(sess, 'saved_models/dish_model.ckpt')                          # Restore all graph variables

    model = tf.get_collection('model')[0]
    inputs = tf.get_collection('model_inputs')[0]

    test_inputs = ['data/train/cabbage_stir_fry/1.jpg',
                   'data/train/red_bean_sticky_rice_dumpling/7.jpg',
                   'data/train/mapo_tofu/11.jpg',
                   'data/table.JPG']
    test_inputs = [DishDataset.read_image(input) for input in test_inputs]
    predictions = sess.run(model,
                           feed_dict={inputs: test_inputs})
    print(predictions)››