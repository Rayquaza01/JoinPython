#!/usr/bin/env python3
import os
import sys
import argparse
import json
import urllib.request
import urllib.parse


def request(args):
    # https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    # archived version as g+ is going away:
    # https://web.archive.org/web/20190218025339/https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    if "apikey" not in args:
        raise Exception("You need to provide an API key.")

    tempArgs = args.copy()
    for value in tempArgs:
        if tempArgs[value] is None or not tempArgs[value]:
            args.pop(value, None)  # Pop none parameters

    # generate url if in options
    if "generateURL" in args:
        generateURL = True
    else:
        generateURL = False

    # remove generateURL key
    args.pop("generateURL", None)

    # make sure mmsurgent is correct value
    if "mmsurgent" in args:
        args["mmsurgent"] = "1"

    url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?" + urllib.parse.urlencode(args)
    if generateURL:
        return url
    else:
        return urllib.request.urlopen(url).read().decode("utf-8")
