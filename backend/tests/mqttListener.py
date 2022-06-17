import paho.mqtt.client as mqtt
from config import Config, Keys
import asyncio
from datetime import datetime
import aioredis

config  = Config()
redis_keys = Keys()
client = mqtt.Client("mqtt_listener")
redis = aioredis.from_url(config.redis_url, decode_responses=True)
loop = asyncio.get_event_loop()


async def flows_add(key, ts, flows):
    await redis.execute_command("XADD",key, ts, "connections", flows)

def mqtt_onmessage(client, userdata, message):
    '''
    ("message received " ,str(message.payload.decode("utf-8")))
    ("message topic=",message.topic)
    ("message qos=",message.qos)
    ("message retain flag=",message.retain)
    '''
    if message.topic == "iot-gate/netview":
        now_timestamp = int(datetime.utcnow().timestamp()*1000)
        loop.run_until_complete(flows_add(redis_keys.timeseries_flows_key(), now_timestamp, message.payload.decode("utf-8")))
        print(f"[+] Adding flows to redisTS:{message.payload.decode('utf-8')}:{now_timestamp}")
    else:
        print("NOT IMPLIMENTED")

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def mqtt_init():
    client.connect(config.mqtt_host)
    client.on_message = mqtt_onmessage
    client.on_log=on_log
    client.subscribe("iot-gate/netview")
    client.loop_forever()    

if __name__ == "__main__":
    mqtt_init()