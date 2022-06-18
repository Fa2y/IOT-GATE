import time
from collections import OrderedDict
import numpy as np
import pyshark
import socket
import asyncio
import sys


def proto_name_by_num(proto_num):
    for name, num in vars(socket).items():
        if name.startswith("IPPROTO") and proto_num == num:
            return name[8:]
    return "Protocol not found"


class packet_flow:
    def __init__(self):
        self.flow_id = (0, 0)
        self.features_list = None

    def __str__(self):
        return "{} -> {}".format(self.flow_id[0], self.flow_id[1])


def get_conn_state(SYN, ACK, FIN, REST, RST, seq):
    if SYN == ACK == FIN == 1:
        return "SHR"
    elif SYN == ACK == 1 and seq > 1:
        return "SF"
    elif SYN == ACK == 1:
        return "S1"
    elif SYN == FIN == 1:
        return "SH"
    elif SYN == RST == 1 and seq > 1:
        return "RSTO"
    elif SYN == RST == 1:
        return "RSTOS0"
    elif SYN == 1:
        return "S0"
    elif RST == 1:
        return "RSTR"
    elif REST == 1:
        return "REJ"
    else:
        return "OTH"


def parse_packet(pkt, temp_dict):
    '''
    [
        ts ,
        src_port ,
        dst_port ,
        duration ,
        src_bytes ,
        dst_bytes ,
        conn_state ,
        missed_bytes ,
        src_pkts
        src_ip_bytes ,
        dst_pkts ,
        dst_ip_bytes ,
        proto ,
        service ,
        ssl_established ,
    ]
    '''
    pf = packet_flow()
    fields = dir(pkt)
    try:
        # to get always src->dst and dst-> same id
        if 'ip' in fields:
            pf.flow_id = tuple(sorted((str(pkt.ip.src), str(pkt.ip.dst))))
        else:
            return None
        # the highest layer name is the service
        if len(pkt.layers) >= 4:
            service = pkt.highest_layer
        else:
            service = None

        src_ip_bytes = np.float64(pkt.ip.get_field_by_showname('Total Length'))
        if service == 'SSL':
            ssl_established = True
        else:
            ssl_established = False
        if 'tcp' in fields:
            syn = int(pkt.tcp.flags_syn)
            ack = int(pkt.tcp.flags_ack)
            reset = int(pkt.tcp.flags_reset)
            rst = int(pkt.tcp.flags_res)
            fin = int(pkt.tcp.flags_fin)
            seq = int(pkt.tcp.seq)
            src_port = np.float64(pkt.tcp.srcport)
            dst_port = np.float64(pkt.tcp.dstport)
            conn_state = get_conn_state(syn, ack, fin, reset, rst, seq)
        else:
            src_port = np.float64(pkt.udp.srcport)
            dst_port = np.float64(pkt.udp.dstport)
            conn_state = None

        missed_bytes = np.float64(65535 - int(pkt.length))
        dst_ip_bytes = None
        dst_pkts = None
        src_pkts = None
        if temp_dict is not None:
            duration = time.time() - np.float64(pkt.sniff_timestamp)
        else:
            key = list(
                temp_dict[(str(pkt.ip.src), str(pkt.ip.dst))].keys())[-1]
            duration = np.float64(pkt.sniff_timestamp) - \
                temp_dict[(str(pkt.ip.src), str(pkt.ip.dst))][key][3]

        pf.features_list = np.array([np.float64(pkt.sniff_timestamp),
                                     src_port, dst_port, duration, np.float64(pkt.length), None, conn_state, missed_bytes, src_pkts, src_ip_bytes, dst_pkts, dst_ip_bytes, proto_name_by_num(int(pkt.ip.proto)), service, ssl_established])
        print(pf.features_list)
        return pf

    except Exception as e:
        # ignore packets that aren't TCP/UDP or IPv4
        print(e)
        return None

#################################################################################


def store_packet(pf, temp_dict, timestamp):
    '''
    temp_dict = {
        flow_id1:{
            timestamp:data,
            timestamp2:data,
            ...
        },
        flow_id2:{
            timestamp:{data, label},
            timestamp2:{data, label},
            ...
        }
    }

    '''
    if pf is not None:
        if pf.flow_id not in temp_dict:
            temp_dict[pf.flow_id] = {timestamp: pf.features_list}
        elif pf.flow_id in temp_dict and timestamp not in temp_dict[pf.flow_id]:
            temp_dict[pf.flow_id][timestamp] = pf.features_list
    return temp_dict

##############################################################################################

# 150528 bytes, 10s time window


def process_pcap(interface):
    start_time = time.time()
    temp_dict = OrderedDict()
    start_time_window = -1
    print(f"pkts to process...")
    cap = pyshark.LiveCapture(interface=interface)
    for pkt in cap.sniff_continuously():

        pf = parse_packet(pkt, temp_dict=temp_dict)
        temp_dict = store_packet(
            pf, temp_dict, np.float64(pkt.sniff_timestamp))

    return temp_dict


if len(sys.argv) > 1:
    print("start:")
    process_pcap(sys.argv[1])
else:
    print("[X] usage :\n\t   python3 caputer.py [INTERFACE]")
