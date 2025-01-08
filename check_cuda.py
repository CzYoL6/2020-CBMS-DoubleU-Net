import tensorflow as tf

print("TensorFlow version:", tf.__version__)
print("Is CUDA available:", tf.test.is_built_with_cuda())
print("Available GPUs:", tf.config.list_physical_devices('GPU'))