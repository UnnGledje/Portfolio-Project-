// This code is written in Node.js 16.x
// Calls an api and sends to DynamoDB
// A scheduler in AWS eventbridge triggers this function to be called every 10 minutes

const https = require('https');
const AWS= require('aws-sdk');

//Configure the DynamoDB table
const dynamoDB = new AWS.DynamoDB.DocumentClient();

//This is the main function that will be executed by lamda
exports.handler = (event) => {
    console.log('Started....');
//Make a request to external HTTPS
const response = https.get("https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API-KEY}", (res) =>{
    res.on('data', (data) => {
    
        //Parse the response data in Javascript object 
        //Log the data recieved from api
        console.log("Data recieved ", data);
        const result = JSON.parse(data);
     
        // Converting from epoch to "normal" datetime
        result.ID = new Date(result.dt*1000).toString();
       
        result.dataSource = "weathermap";
        console.log("Data", result);
        
        //Store the result in DynamoDB
        console.log("Put...");
        dynamoDB.put({
            TableName: '{Your table name here}',
            Item: result, 
        }, (err) => {
            if (err) {
                console.error(`Error storing item: ${err}`);
            }else {
                console.log('Item Stored succesfully');
            }
        });
    });
});
};

