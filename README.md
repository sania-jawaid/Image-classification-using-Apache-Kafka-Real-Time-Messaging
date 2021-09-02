### System to classify fashion images. The system will have a single client consuming a single machine learning service. It is robust, scalable and able to process requests asynchronously. - Note that this is not a REST API based system but rather one which can process requests in a non-blocking way and (theoretically) put the results somewhere else (like a database). Here it is mocked this by printing to the console.

### This project is built in three parts:


## Part 1:
1) Built a multi-class image classifier on the fashion MNIST dataset using a Convolutional Neural Network (CNN) based model. 
The notebook can be accessed with the name 'Fashion Mnist Dataset Model training.ipynb' (Model saved as 'final.h5')
2) Built a multi-class image classifier on the MNIST dataset using a Convolutional Neural Network (CNN) based model. 
The notebook can be accessed with the name 'Mnist Dataset Model training.ipynb' (Model saved as 'mnist-model.h5')
3) Built a multi-class image classifier on the Cifar10 dataset using a Convolutional Neural Network (CNN) based model. 
The notebook can be accessed with the name 'Cifar Dataset Model training.ipynb' (Model saved as 'cifar-model.h5')
Other Datasets can be included with minor modifications if required.
NOTE: Getting High Accuracy was not a the main objective of this task.

## Part 
1) Build a unified API in python to send and receive messages to / from Apache Kafka
2) The inputs to the function and the outputs should be as unified as possible.
Setup Kakfa on local machine using this link: https://kafka.apache.org/quickstart
NOTE: Need to make some changes to the configuration to be able to send images over the messaging service.
### You need to override the following properties:

Broker Configs($KAFKA_HOME/config/server.properties)

`message.max.bytes=15728640`
`replica.fetch.max.bytes=15728640`

Consumer Configs($KAFKA_HOME/config/consumer.properties)
`fetch.message.max.bytes=15728640`

#### Restart the server.

Look at this documentation for more info: http://kafka.apache.org/08/configuration.html


## Part 3:
1) Multiple machine learning services that are coordinated via a message broker. The system will have a single client consuming a single
machine learning service.
2) Used the model from Part 1 and the library from Part 2 to build such an application. It is robust, scalable and able to process
requests asynchronously.
3) Note that this is not a REST API based system but rather one which can process requests in a non-blocking way and (theoretically) put the
results somewhere else (like a database). Y Here it is mocked this by printing to the console.
