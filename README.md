# Portfolio-Project-
A fun School Project 


# About the project 

In this project i built a thermometer to be able to log the temperature in my home. By using an API from OpenWeatherMap I can also log the temperatures outside. The whole usecase is built around AWS Cloud Services. 


# Flowchart

![AWS_diagram drawio (2)](https://user-images.githubusercontent.com/92151619/206851988-18a50908-2368-4805-b181-4832bb97d403.png)


# Components

# 1.
 To build the thermometer I used a DHT11 sensor that I connected to a RaspberryPi 3b+.
 A DHT11 is a commonly used digital temperature and humidity sensor.
 
# 2. 

  I wanted the pi to be able to send up the sensor data to AWS Cloud. To do this I wrote code that published messages to IoT Core through       MQTT. The pi retrieves the sensor data from the sensor and connects to AWS IoT and publishes to the defined topic. 
  
  # Publishing message to topic 'rpidht': Temperature : 22.0C Humidity : 28.0%
  
              rpidht
              [
                "Temperature: 22.0C",
                "Humidity: 29.0%"
              ]

  
# 3. 
  
  Since I'm using an IoT device I decided to use AWS IoT. In their service IoT Core I created a thing and subscribed to my publisher to be     able to see the messages from my device. 
  
 # 4.
 
  To be able to log the data it had to be saved somewhere. AWS has a database service called dynamoDB. DynamoDB is easy to integrate with the   rest of my project. To be able to send the data to dynamoDB I had to configure some other AWS services, to be specific an IoT rule and an     action. The rule says that every new message coming from the thing and publishing to our topic will trigger an action and that action will   send a message to be stored in dynamoDB.
  
 # 5. 
   
  For this project I used an API from OpenWeatherMap. I choose an API that updates every ten minutes and with the help of my coordinates,
  my longtitude and latitude I was able to get measurements from my city. 
  
  API call :
  
  # https://api.openweathermap.org/data/2.5/weather?lat={lat-coord}&lon={lon-coord}&appid={API-key}
  
 # 6. 
 
  Firstly, I had to set up an API gateway to be able to use my API in AWS Cloud services. Secondly I created a lambda function in Node.js       16.x that makes an https request and sends the data to my dynamoDB table. Thirdly I created a schedule in AWS eventbridge that updates the   function call every ten minutes.
 
 # 7. 
 
  The dynamoDB table created is used for both of our data sources. I will differentiate them with the help of an id and a timestamp. 
 
 # 8. 
 
  To visualize and analyze the data I choose Amazon Quicksight. It's a tool that makes it very easy to display and sort your data. 
 
 # Additional Notes 
 
   This project is easy to scale up, either by adding more devices or more API calls.
   IoT Core is configured in such a way that more devices can be added and DynamoDB can scale as needed.
   The Lambda function can either be configured to make multiple api calls or to have multiple lambda functions perform.
   
   Regarding the security of this project, all communication is encrypted and certificate-based.
   The hardware can also be secured by turning off ssh and changing the password regularly.
   Login is required for AWS and Quicksight.
 
   This project uses a warm path and saves data in one DynamoDB table with a ttl of three months. For longer and more extensive storage, i.e for more data and
   a longer ttl a cold path leading to long-term storage could be used. The option of saving stored data to file also exists. 
  

  
