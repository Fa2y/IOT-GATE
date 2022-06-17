from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from datetime import datetime
import json
from redis.config import Config, Keys
import aioredis
import asyncio
from time import sleep

config = None
redis_keys = None
redis = None

app = FastAPI()

@app.on_event("startup")
async def setup():
    global config, redis_keys, redis
    config  = Config()
    redis_keys = Keys()
    redis = aioredis.from_url(config.redis_url, decode_responses=True)

async def fetch_flows(key, ts):
    '''
        Fetch flow from redis stream
        (closest to timestamp ts)
    '''
    result = await redis.xrevrange(key, max=ts, count=1)
    return result[0][1] # unnest results

async def fetch_alerts(key, count):
    """
        Fetch latest `count` alerts from redis stream
    """
    result = await redis.xrevrange(key, max='+', count=count)
    return dict(result)

def parse_flows(flows):
    '''
        Parse to flows to hosts and connections
    '''
    hosts = set()
    parsed_flows = flows["connections"].split(',') 
    for flow in parsed_flows:
        hosts.add(flow.split('-')[0])
        hosts.add(flow.split('-')[1])

    return {"hosts":list(hosts), "connections":parsed_flows} 

@app.websocket("/alerts-ws")
async def alerts_websocket(websocket: WebSocket):
    await websocket.accept()
    all_alerts = await fetch_alerts(redis_keys.alerts_stream_key(), count=None)
    await websocket.send_text(json.dumps(all_alerts))
    old_alerts = await fetch_alerts(redis_keys.alerts_stream_key(), count=1)
    while True:
        sleep(2)
        latest_alert = await fetch_alerts(redis_keys.alerts_stream_key(), count=1)
        if old_alerts != latest_alert:
            old_alerts = latest_alert
            await websocket.send_text(json.dumps(latest_alert))

@app.websocket("/netview-ws")
async def netview_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        timestamp_shift = await websocket.receive_text()
        if timestamp_shift == "latest":# Get Latest
            flows = await fetch_flows(redis_keys.flows_stream_key(), '+') # + for timestamp to get latest
            result_data = parse_flows(flows)
            await websocket.send_text(json.dumps(result_data))

        else:# Get at specific timestamp
            timestamp = int((datetime.utcnow().timestamp()*1000) - int(timestamp_shift))   
            flows = await fetch_flows(redis_keys.flows_stream_key(), str(timestamp))
            result_data = parse_flows(flows)
            await websocket.send_text(json.dumps(result_data))
