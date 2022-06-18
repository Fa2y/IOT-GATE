from redis.config import Config, Keys
import asyncio
from datetime import datetime
import aioredis
import random
from time import sleep
import threading
from faker import Faker

config = Config()
redis_keys = Keys()
redis = aioredis.from_url(config.redis_url, decode_responses=True)
loop = asyncio.get_event_loop()
faker = Faker()


async def flow_stream_add(key, ts, flows):
    """Adding network flows to redis stream"""
    await redis.execute_command("XADD", key, ts, "connections", flows)


async def alert_stream_add(key, ts, alert_host, alert_details):
    """Adding IDS alert to redis stream"""
    await redis.execute_command("XADD", key, ts, "alert_host", alert_host, "alert_details", alert_details)

HOSTS = [
    "192.168.14.32",
    "192.168.14.45",
    "192.168.14.22",
    "172.31.2.16",
    "172.18.3.64",
    "192.168.1.1",
]


class FlowsSimulation(threading.Thread):
    '''
     This is a simulation to add flows to stream
     from fake data
    '''

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get_fake_hosts(self):
        """Generate fake public ips"""
        # send flow ids here
        return HOSTS + [faker.ipv4() for i in range(random.randint(2, 6))]

    def make_fake_connections(self):
        """Generate fake network flows"""
        hosts_copy = []
        connections = []
        hosts = self.get_fake_hosts()
        for host in hosts:
            hosts_copy = hosts.copy()
            hosts_copy.remove(host)
            connections.append(f"{host}-{random.choice(hosts_copy)}")
        return connections

    def run(self):
        while True:
            connections = self.make_fake_connections()
            for i in range(12):
                sleep(5)
                now_timestamp = int(datetime.utcnow().timestamp()*1000)
                loop.run_until_complete(flow_stream_add(
                    redis_keys.flows_stream_key(), now_timestamp, ','.join(connections)))
                print(
                    f"[+] Adding flows to redis stream:{redis_keys.flows_stream_key()}:{','.join(connections)}:{now_timestamp}")


def main():
    flows_sim = FlowsSimulation()
    flows_sim.start()
    while True:
        """Wait for input to launch an alert"""
        input()
        now_timestamp = int(datetime.utcnow().timestamp()*1000)
        attack_host = random.choice(HOSTS)
        loop.run_until_complete(alert_stream_add(redis_keys.alerts_stream_key(
        ), now_timestamp, attack_host, "Malicious activity detected, you should take immediate actions!"))
        print(f"[+] Sending alert by host:{attack_host} at:{now_timestamp}")


if __name__ == "__main__":
    main()
