"""
learn the basics of Tensorflow
"""
import tensorflow as tf
import numpy as np

print("TensorFlow version:", tf.__version__)

# Tensors are multi-dimensional arrays with a uniform type (called a dtype). You can see all supported dtypes at tf.dtypes
# If you're familiar with NumPy, tensors are (kind of) like np.arrays.
# All tensors are immutable like Python numbers and strings: you can never update the contents of a tensor, only create a new one.


mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0


model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])
