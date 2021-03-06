#!/usr/bin/env python

# File name:            peerloganalyser.py
# Author:               Sarah-Louise Justin
# e-mail:               sarahlouise.justin@student.kuleuven.be
# Python Version:       2.7

"""
This file is designed to process the logpeerinfo.txt log-file:
    - Converts the log-file to a valid json format

The following information are extracted:
    - The time of connection of each peer
    - The list of round-trip time of each peer
    - the type of connection: inbound or outbound of each peer
"""

import time, os
import schedule
import datetime
import json
import re
import sys
import datetime
import pickle
import jsonprocess
import statistics


def init():
    """
    Prepares the log file to be processed by converting to a valid json format

    """
    #date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y_%m_%d")
    #log = 'logpeerinfo_'+date+'.txt'
    log = 'AMSLogPeers/logpeerinfo_2017_05_24.txt'
    peerlog = open(log, 'r+')


    peerlog_json = ["["]
    pattern = re.compile("(}{)")
    for line in peerlog:
        if re.search(pattern, line):
            temp = "}"+","+"{"
            peerlog_json.append(temp)
        else:
            peerlog_json.append(line)

    peerlog_json.append("]")

    for line in peerlog_json:
        #with open("logpeerjson"+date+".txt", "a") as out:
        with open("AMSLogPeers/logpeerjson.txt", "a") as out:
            out.write("".join(line))

def json_parse(log):
    """
    Parse the logpeerinfo.txt file of the day.
    Extract following data:
        - The connection time in an unix format of each peer
        - The updated round-trip time of each peer
        - The type of connection: inbound of outbound
        - The list of IP addresses of the currently connected peers
    :param log: The log file of the day
    :return:
    """

    date = log[0]['logday']

    dictConntime = {}
    dictRTT = {}
    dictPeerList = {}
    dictPeerIP = {}

    RTTList = []

    for i in log:
        # Save data on a daily base
        if (date != i['logday']):
            print i['logday']
            print i['logtime']

            with open("Peers/Conntime/Conntime_" + date + ".txt", "a") as out1:
                pickle.dump(dictConntime, out1)
            dictConntime = {}

            with open("Peers/RTTstats/RTTstats_" + date + ".txt", "a") as out2:
                pickle.dump(dictRTT, out2)
            dictRTT = {}

            with open("Peers/in_out/in_out_bound_" + date + ".txt", "a") as out3:
                pickle.dump(dictPeerList, out3)
            dictPeerList = {}

            with open("Peers/Peerlist/PeerList_" + date + ".txt", "a") as out4:
                pickle.dump(dictPeerIP, out4)
            dictPeerIP = {}

            logtimes = open("Peers/RTTlogtimes/RTTlogtimes_" + date + ".txt", "a")
            for item in RTTList:
                logtimes.write(item + "\n")
            RTTList = []

            date = i['logday']

        RTTList.append(i['logtime'])

        for peer in i['peers']:
            id = peer['id']
            conntime_unix = peer['conntime']
            conntime = datetime.datetime.fromtimestamp(conntime_unix).strftime('%Y-%m-%d %H:%M:%S')

            # Extract RTT
            if 'pingtime' in peer:
                if id in dictRTT.keys():
                    dictRTT[id].append(peer['pingtime'])
                else:
                    dictRTT[id] = []
                    dictRTT[id].append(peer['pingtime'])

            # If proper node has restarted
            if id in dictConntime.keys():
                if dictConntime[id] != conntime:
                    with open("Peers/Conntime/Conntime_" + date + "_" + i['logtime'] + ".txt", "a") as out:
                        pickle.dump(dictConntime, out)
                    dictConntime = {}

                    with open("Peers/RTTstats/RTTstats_" + date + "_" + i['logtime'] + ".txt", "a") as out2:
                        pickle.dump(dictRTT, out2)
                    dictRTT = {}

                    with open("Peers/in_out/in_out_bound_" + date + "_" + i['logtime'] + ".txt", "a") as out3:
                        pickle.dump(dictPeerList, out3)
                    dictPeerList = {}

                    with open("Peers/Peerlist/PeerList_" + date + "_" + i['logtime'] + ".txt", "a") as out4:
                        pickle.dump(dictPeerIP, out4)
                    dictPeerIP = {}
            else:
                # Extract conenction moment
                dictConntime[id] = conntime

            # Extract information about ingoing and outgoing connections
            if id not in dictPeerList.keys():
                if peer['inbound']:
                    dictPeerList[id] = 'inbound'
                else:
                    dictPeerList[id] = 'outbound'
            if id not in dictPeerIP.keys():
                dictPeerIP[id] = peer['addr']

    with open("Peers/Conntime/Conntime_" + date + ".txt", "a") as out:
        pickle.dump(dictConntime, out)
    with open("Peers/RTTstats/RTTstats_" + date + ".txt", "a") as out2:
        pickle.dump(dictRTT, out2)
    with open("Peers/in_out/in_out_bound_" + date + ".txt", "a") as out3:
        pickle.dump(dictPeerList, out3)
    with open("Peers/Peerlist/PeerList_" + date + ".txt", "a") as out4:
        pickle.dump(dictPeerIP, out4)

    logtimes = open("Peers/RTTlogtimes/RTTlogtimes_" + date + ".txt", "a")
    for item in RTTList:
        logtimes.write(item + "\n")
