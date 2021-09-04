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
from keras.utils import to_categorical

producer = KafkaProducer(bootstrap_servers='localhost:9092')

"""
Requirements
1. Numpy
2. Pympler or a recursive sys.getsizeof()
3. PIL
"""

# Lambda function to represent memory in Mb
get_size = lambda x: asizeof(x) / (1024*1024)

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
        msg = encode_and_transmit_numpy_array_in_bytes(np_arr)
        print('Transmitted Image Size: {} Mb'.format(get_size(j_dumps)))
        msg=msg.encode('utf-8')
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
        msg = encode_and_transmit_numpy_array_in_bytes(np_arr)
        print('Transmitted Image Size: {} Mb'.format(get_size(msg)))
        msg=msg.encode('utf-8')
        category = "topic_"+topic
        producer.send(category,msg, label).add_callback(success).add_errback(error)
    producer.flush()

# Encode and transmit Numpy Array in bytes
def encode_and_transmit_numpy_array_in_bytes(numpy_array:np.array) -> str:
    # Create a Byte Stream Pointer
    compressed_file = io.BytesIO()
    
    # Use PIL JPEG reduction to save the image to bytes
    Image.fromarray(numpy_array).save(compressed_file, format="JPEG")
    
    size_in_bytes = compressed_file.tell()
    img_file_size = size_in_bytes/(1024*1024)
    print("Original Image size_in_bytes:",size_in_bytes, "img_file_size in MB:",img_file_size)

    # Set index to start position
    compressed_file.seek(0)
    
    # Convert the byte representation to base 64 representation for Post
    return json.dumps(base64.b64encode(compressed_file.read()).decode())
    #return json.dumps(base64.b64encode(compressed_file.read()))


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

def preprocess_img(image, grayscale=False):
    if grayscale:
        image = cv2.resize(image, (28, 28))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image
    
# load train and test dataset
def load_dataset(dataset, grayscale=False):
    print("grayscale",grayscale)
    # load dataset
    (trainX, trainY), (testX, testY) = dataset.load_data()
    # reshape dataset to have a single channel
    testX = np.array([preprocess_img(x, grayscale) for x in testX])
    print(testX.shape, testY.flatten()[0])
    # one hot encode target values
    # testY = to_categorical(testY)
    return testX, testY#testY.flatten()

def main():
    print("Producing msgs!")	
    option = 3
    if option == 1:
        #load Fashion Mnist Data
        topic = "fashion"
        fashion_mnist = tf.keras.datasets.fashion_mnist
        (test_images, test_labels) = load_dataset(fashion_mnist)
    elif option == 2:
       #load Mnist Data
       topic = "mnist"
       mnist = keras.datasets.mnist
       (test_images, test_labels) = load_dataset(mnist)
    else:
       #load Cifar Data
       topic = "cifar"
       cifar = keras.datasets.cifar10
       (test_images, test_labels) = load_dataset(cifar, grayscale=True)
    kafka_python_producer_async(producer, topic, test_images, test_labels)

if __name__ == "__main__":
    main()
