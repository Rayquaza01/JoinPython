#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
version = "1.0.2"


def listDevices(apikey):
    reg = urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=" + apikey)
    return json.loads(reg.read().decode("utf-8"))


def request(args):
    # https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    # archived version as g+ is going away:
    # https://web.archive.org/web/20190218025339/https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    if "apikey" not in args:
        raise Exception("You need to provide an API key.")

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
        return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
