from awscrt import mqtt
import sys
import threading
import time
from uuid import uuid4
import json
import board
import adafruit_dht

# define Bboard (dht11) and pin (D4)
dhtDevice = adafruit_dht.DHT11(board.D4) 
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

# Message Broker for AWS IoT to send and receive messages through an MQTT connection. 
# The device connects to the server, subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# Parse arguments
import command_line_utils;
cmdUtils = command_line_utils.CommandLineUtils("PubSub - Send and recieve messages through an MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmdUtils.register_command("port", "<int>", "Connection port, 8883", type=int)
cmdUtils.register_command("client_id", "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))

# Needs to be called so the command utils parse the commands
cmdUtils.get_args()

received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
     print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

    
    # Evaluate result with a callback.
    resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))

if __name__ == '__main__':
    mqtt_connection = cmdUtils.build_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    print("Connecting to {} with client ID '{}'...".format(
    cmdUtils.get_command(cmdUtils.m_cmd_endpoint), cmdUtils.get_command("client_id")))
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message_topic = cmdUtils.get_command(cmdUtils.m_cmd_topic)
    message_string = cmdUtils.get_command(cmdUtils.m_cmd_message)

    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=message_topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

   
    # Send message
    if message_string:
        print ("Sending messages until program killed\n")
                
        print ("Sending {} message(s)".format)
                
        while 1:

            temperature_x = dhtDevice.temperature
            humidity_y = dhtDevice.humidity
            
            message = ("Temperature: {:.1f}C".format(temperature_x), "Humidity: {:.1f}%".format(humidity_y))
            print("Publishing message to topic '{}' :{} {}".format(message_topic, message, message))
            message_json = json.dumps(message)
            mqtt_connection.publish(
               topic=message_topic,
               payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(100)
