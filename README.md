# Portfolio-Project-
A fun School Project 


# About the project 

In this project i built a thermometer to be able to log the temperature in my home. By using an API from OpenWeatherMap I can also log the temperatures outside. The whole usecase is built around AWS Cloud Services. 


# Flowchart


![AWS_diagram drawio (2)](https://user-images.githubusercontent.com/92151619/206849984-2160fa73-3980-458d-ae68-fd8b034b8bc7.png)

# Components

# 1.
 To build the thermometer I used a DHT11 sensor that I connected to a RaspberryPi 3b+.
 
# 2. 

  I wanted the pi to be able to send up the sensor data to AWS Cloud. To do this I wrote code that published messages to IoT Core through       MQTT. The pi retrieves the sensor data from the sensor and connects to AWS IoT and publishes to the defined topic. 
  
# 3. 
  
  Since I'm using an IoT device I decided to use AWS IoT. In their service IoT Core I created a thing and subscribed to my publisher to be     able to see the messages from my device. 
  
 # 4.
 
  To be able to log the data it had to be saved somewhere. AWS has a database service called dynamoDB. DynamoDB is easy to integrate with the   rest of my project. To be able to send the data to dynamoDB i had to configure some other AWS services, to be specific an IoT rule and an     action. The rule says that every new message coming from the thing and publishing to our topic will trigger an action and that action will   send a message to be stored in dynamoDB.
  
 # 5. 
 
   The dynamoDB table created is used for both of our data sources. I will differentiate them with the help if an id and a timestamp. 
 
 # 6. 
 
 
  

  
