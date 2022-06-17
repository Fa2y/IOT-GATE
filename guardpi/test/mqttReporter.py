import paho.mqtt.client as mqtt
from time import sleep
HOST = "localhost"

DATA = [ # For testing purposes
        "192.168.14.32-8.8.8.8",
        "192.168.14.45-192.168.14.22",
        "192.168.14.45-8.8.8.8",
        "192.168.14.22-1.1.1.1",
        "192.168.14.22-142.251.37.174",
        "192.168.14.32-142.251.37.174",
        "192.168.14.45-98.137.11.164",
        ]


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOST, 1883, 60)

while True:
    client.publish('iot-gate/netview', payload=','.join(DATA), qos=0, retain=False)
    sleep(5)

# client.loop_forever()