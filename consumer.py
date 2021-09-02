from kafka import KafkaConsumer, TopicPartition
import time
import numpy as np
from pympler.asizeof import asizeof
import json
import io
import base64
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

size = 1000000

# Lambda function to represent memory in Mb
get_size = lambda x: asizeof(x) / 10 ** 6

# Sample array - Represents a HD Image , 3 Channels , 256 bit
np_arr = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)

# Receive and decode bytes to numpy array
def receive_and_decode_bytes_to_numpy_array(j_dumps:str) -> np.array:
    # Convert Base 64 representation to byte representation
    compressed_data = base64.b64decode(j_dumps)
    
    # Read byte array to an Image
    im = Image.open(io.BytesIO(compressed_data))
    
    # Return Image to numpy array format
    return np.array(im)

def get_model(topic):
   model = load_model('final.h5')
   if topic == "topic_mnist":
        model = load_model('mnist-model.h5')
   elif topic == "topic_cifar":
        model = load_model('cifar-model.h5')
   probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
   return model

consumer1 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer1():
    consumer1.subscribe(['topic_fashion', 'topic_cifar', 'topic_mnist'])
    print(consumer1)
    for msg in consumer1:
      print("\n")
      print(msg.topic)
      print(msg.key.decode())
      print(msg.value.decode())
      label=msg.key.decode()
      model = get_model(msg.topic)
      msg=msg.value.decode()
      im = receive_and_decode_bytes_to_numpy_array(msg)
      print('Reloaded Image Size: {} Mb'.format(get_size(im)))
      print(im.shape)
      prediction = model.predict(np.array([im]),  verbose=2)
      print("Results:")
      print("Prediction:", np.argmax(prediction), "Actual:", label)

consumer2 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer2():
    consumer2.assign([TopicPartition('topic1', 1), TopicPartition('topic2', 1)])
    for msg in consumer2:
        print(msg)

consumer3 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer3():
    partition = TopicPartition('topic3', 0)
    consumer3.assign([partition])
    last_offset = consumer3.end_offsets([partition])[partition]
    for msg in consumer3:
        if msg.offset == last_offset - 1:
            break

def main():
    print("Consuming Msgs!")
    kafka_python_consumer1()

if __name__ == "__main__":
    main()
