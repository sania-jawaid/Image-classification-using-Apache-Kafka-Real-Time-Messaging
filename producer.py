import time
from kafka import KafkaProducer
import numpy as np
from pympler.asizeof import asizeof
import json
import io
import base64
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
producer = KafkaProducer(bootstrap_servers='localhost:9092')

"""
Requirements
1. Numpy
2. Pympler or a recursive sys.getsizeof()
3. PIL
"""

# Lambda function to represent memory in Mb
get_size = lambda x: asizeof(x) / 10 ** 6

# Sample array - Represents a HD Image , 3 Channels , 256 bit
np_arr = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)

def kafka_python_producer_sync(producer, topic, test_images, test_labels):
    size = len(test_images)
    print("Total number of Test images:", size)
    for i in range(size):
        print(i, topic, size)
        np_arr = test_images[i]
        label = "{}".format(test_labels[i]).encode('utf-8')
        print(np_arr.shape)
        print('Original Image Size: {} Mb'.format(get_size(np_arr)))
        j_dumps = encode_and_transmit_numpy_array_in_bytes(np_arr)
        print('Transmitted Image Size: {} Mb'.format(get_size(j_dumps)))
        msg=j_dumps.encode('utf-8')
        category = "topic_"+topic
        producer.send(category,msg, label).add_callback(success).add_errback(error)
    producer.flush()

def success(metadata):
    print(metadata.topic)

def error(exception):
    print(exception)

def kafka_python_producer_async(producer, topic, test_images, test_labels):
    size = len(test_images)
    print("Total number of Test images:", size)
    for i in range(size):
        print(i, topic, size)
        np_arr = test_images[i]
        label = "{}".format(test_labels[i]).encode('utf-8')
        print(np_arr.shape)
        print('Original Image Size: {} Mb'.format(get_size(np_arr)))
        j_dumps = encode_and_transmit_numpy_array_in_bytes(np_arr)
        print('Transmitted Image Size: {} Mb'.format(get_size(j_dumps)))
        msg=j_dumps.encode('utf-8')
        category = "topic_"+topic
        producer.send(category,msg, label).add_callback(success).add_errback(error)
    producer.flush()

# Encode and transmit Numpy Array in bytes
def encode_and_transmit_numpy_array_in_bytes(numpy_array:np.array) -> str:
    # Create a Byte Stream Pointer
    compressed_file = io.BytesIO()
    
    # Use PIL JPEG reduction to save the image to bytes
    Image.fromarray(numpy_array).save(compressed_file, format="JPEG")
    
    # Set index to start position
    compressed_file.seek(0)
    
    # Convert the byte representation to base 64 representation for REST Post
    return json.dumps(base64.b64encode(compressed_file.read()).decode())


# Receive and decode bytes to numpy array
def receive_and_decode_bytes_to_numpy_array(j_dumps:str) -> np.array:
    # Convert Base 64 representation to byte representation
    compressed_data = base64.b64decode(j_dumps)
    
    # Read byte array to an Image
    im = Image.open(io.BytesIO(compressed_data))
    
    # Return Image to numpy array format
    return np.array(im)

def error_callback(exc):
    raise Exception('Error while sendig data to kafka: {0}'.format(str(exc)))

def convert_to_grayscale(images):
    print("[INFO] loading and resizing training images...", len(images))
    data = []
    # loop over the image paths
    for img in images:
        image = cv2.resize(img, (28, 28))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        data.append(gray)
    t_images = np.array(data)
    return t_images

def main():
    print("Producing msgs!")	
    option = 3
    if option == 1:
        #load Fashion Mnist Data
        topic = "fashion"
        fashion_mnist = keras.datasets.fashion_mnist
        (_, _), (test_images, test_labels) = fashion_mnist.load_data()
    elif option == 2:
       #load Mnist Data
       topic = "mnist"
       mnist = keras.datasets.mnist
       (_, _), (test_images, test_labels) = mnist.load_data()
    else:
       #load Cifar Data
       topic = "cifar"
       data = keras.datasets.cifar10
       (_, _), (test_images, test_labels) = data.load_data()
       test_images = convert_to_grayscale(test_images)
    kafka_python_producer_async(producer, topic, test_images, test_labels)

if __name__ == "__main__":
    main()
