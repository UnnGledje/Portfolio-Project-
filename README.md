# Portfolio-Project-
A fun School Project 


# About the project 

In this project i built a thermometer to be able to log the temperature in my home. By using an API from OpenWeatherMap I can also log the temperatures outside. The whole usecase is built around AWS Cloud Services. 


# Flowchart

 file:///home/unn/Downloads/AWS_diagram.drawio%20(2).png

# Components

# 1.
 To build the thermometer I used a DHT11 sensor that I connected to a RaspberryPi 3b+.
 
# 2. 

  I wanted the pi to be able to send up the sensor data to AWS Cloud. To do this I wrote code that published messages to IoT Core through       MQTT. The pi retrieves the sensor data from the sensor and connects to AWS IoT and publishes to the defined topic. 
  
# 3. 
  
  Since I'm using an IoT device I decided to use AWS IoT. In their service IoT Core I created a thing and subscribed to my publisher to be     able to see the messages from my device. 
  
 # 4.
 
  To be able to log the data it had to be saved somewhere. AWS has a database service called dynamoDB. DynamoDB is easy to integrate with the   rest of my project. To be able to send the data to dynamoDB I had to configure some other AWS services, to be specific an IoT rule and an     action. The rule says that every new message coming from the thing and publishing to our topic will trigger an action and that action will   send a message to be stored in dynamoDB.
  
 # 5. 
 
   The dynamoDB table created is used for both of our data sources. I will differentiate them with the help of an id and a timestamp. 
 
 # 6. 
 
  For this project I used an API from OpenWeatherMap. I choose an API that updates every ten minutes and with the help of my coordinates,
  my longtitude and latitude I was able to get measurements from my city. 
 
 # 7. 
 
  Firstly, I had to set up an API gateway to be able to use my API in AWS Cloud services. Secondly I created a lambda function in Node.js       16.x that makes an https request and sends the data to my dynamoDB table. Thirdly I created a schedule in AWS eventbridge that updates the   function call every ten minutes.
  
 # 8. 
 
  To visualize and analyze the data I choose another Amazon Quicksight. It's a tool that makes it very easy to display and sort your data. 
 
 
  

  
