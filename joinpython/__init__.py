#!/usr/bin/env python3
import os
import sys
import argparse
import json
import urllib.request
import urllib.parse


def request(args, deviceData={"pref": ""}, contacts={}):
    tempArgs = args.copy()
    for value in tempArgs:
        if tempArgs[value] is None or not tempArgs[value]:
            args.pop(value, None)  # Pop none parameters
    if "generateURL" in args:
        generateURL = True
    else:
        generateURL = False
    args.pop("generateURL", None)
    args.pop("setup", None)
    if "deviceId" not in args:
        args["deviceId"] = deviceData["pref"]
    for key, value in args.items():  # fixes the need to encase args in quotes
        if type(value) is list:
            args[key] = " ".join(value)
    if "smsnumber" in args:
        if args["smsnumber"] in contacts:
            args["smsnumber"] = contacts[args["smsnumber"]]
    if "callnumber" in args:
        if args["callnumber"] in contacts:
            args["callnumber"] = contacts[args["callnumber"]]
    if "mmsurgent" in args:
        args["mmsurgent"] = "1"
    # https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    if "apikey" not in args:
        if "apikey" in deviceData:
            args["apikey"] = deviceData["apikey"]
        else:
            raise Exception("You need to provide an API key.")
    if "," in args["deviceId"]:  # allows for multiple device names separated by commas
        args["deviceNames"] = args["deviceId"]
        args.pop("deviceId", None)
    elif "group" in args["deviceId"]:  # allows for groups (group.android, etc.)
        args["deviceId"] = args["deviceId"]
    elif args["deviceId"] in deviceData:  # allows for single device
        args["deviceId"] = deviceData[args["deviceId"]]
    url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?" + urllib.parse.urlencode(args)
    if generateURL:
        return url
    else:
        return urllib.request.urlopen(url).read().decode("utf-8")
