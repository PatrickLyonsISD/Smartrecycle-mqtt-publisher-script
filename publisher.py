import sys
import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "unique_topic/mqtt_test"
client_id = f'python-mqtt-publisher-{random.randint(1000, 9999)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, detected_object):
    msg_count = 0
    while msg_count < 5:
        time.sleep(1)
        msg = f"Detected object: {detected_object} | Message count: {msg_count}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run(detected_object):
    client = connect_mqtt()
    client.loop_start()
    publish(client, detected_object)
    client.loop_stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        detected_object = sys.argv[1]
        run(detected_object)
    else:
        print("No detected object passed to the script.")
