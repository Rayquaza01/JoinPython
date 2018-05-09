#!/usr/bin/env python3
import argparse
import json
import urllib.request
import urllib.parse


def request(arguments, devices, contacts={}):
    if arguments["device"] is None:
        arguments["device"] = devices["pref"]
    for key, value in arguments.items():  # fixes the need to encase args in quotes
        if type(value) is list:
            arguments[key] = " ".join(value)
    if arguments["smsnumber"] is not None:
        if arguments["smsnumber"] in contacts:
            arguments["smsnumber"] = contacts[arguments["smsnumber"]]
    if arguments["callnumber"] is not None:
        if arguments["callnumber"] in contacts:
            arguments["callnumber"] = contacts[arguments["callnumber"]]
    deviceName = arguments["device"]
    arguments.pop("device", None)  # removes device to prevent sending extra params
    arguments["apikey"] = devices["apikey"]
    # https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    if "," in deviceName:  # allows for multiple device names separated by commas
        arguments["deviceNames"] = deviceName
    elif "group" in deviceName:  # allows for groups (group.android, etc.)
        arguments["deviceId"] = deviceName
    else:  # allows for single device
        arguments["deviceId"] = devices[deviceName]
    encoded = []
    for key, value in arguments.items():
        if value is not None:
            encoded.append("=".join([key, urllib.parse.quote_plus(str(value))]))
    return urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api/"
                                  "messaging/v1/sendPush?" +
                                  "&".join(encoded)).read().decode("utf-8")


def arguments(argue):
    ap = argparse.ArgumentParser()
    ap.add_argument("-te", "--text", help="Text (Tasker Command or notification text)", nargs="*")
    ap.add_argument("-ti", "--title", help="Title (If set will create notification)", nargs="*")
    ap.add_argument("-i", "--icon", help="Icon URI (publicly accessible URL or local file URI; used whenever a notification is created)")
    ap.add_argument("-s", "--smallicon", help="Icon URI to be used as the statusbar icon")
    ap.add_argument("-p", "--priority", help="Priority of the notification from -2 (lowest) to 2 (highest and default)",
                    type=int, choices=range(-2, 3))
    ap.add_argument("-v", "--vibration", help="Vibration for when the notification is recived. Generate the pattern at "
                    "http://autoremotejoaomgcd.appspot.com/AutoRemoteNotification.html")
    ap.add_argument("-u", "--url", help="URL")
    ap.add_argument("-so", "--sound", help="Sound URI - publicly accessible URL or local file URI; used whenever a notification is created")
    ap.add_argument("-im", "--image", help="Image URI - publicly accessible URL or local file URI; used whenever a notification is created")
    ap.add_argument("-g", "--group", help="Notification Group (Android 7 and above) - allows you to join notifications in different groups",
                    nargs="*")
    ap.add_argument("-c", "--clipboard", help="Clipboard", nargs="*")
    ap.add_argument("-f", "--file", help="File (must be a publicly accessible URL)")
    ap.add_argument("-d", "--device", help="The device name or a group (group.all, group.android, group.chrome, group.windows10, group."
                    "phone, group.tablet, group.pc)", nargs="*")
    ap.add_argument("-smsn", "--smsnumber", help="Phone number to send an SMS to. If you want to set an SMS you need to set this and the "
                    "smstext values", nargs="*")
    ap.add_argument("-cn", "--callnumber", nargs="*", help="A number to call")
    ap.add_argument("-smst", "--smstext", help="Some text to send in an SMS. If you want to set an SMS you need to set this and the "
                    "smsnumber values", nargs="*")
    ap.add_argument("-fi", "--find", help="Set to true to make your device ring loudly")
    ap.add_argument("-w", "--wallpaper", help="A publicly accessible URL of an image file. Will set the wallpaper on the receiving device")
    ap.add_argument("-mms", "--mmsfile", help="MMS file. smsnumber must be set for this to have an affect")
    ap.add_argument("-lw", "--lockWallpaper", help="The wallpaper to set on the lockscreen (Android 7+), must be publicly accessible URL")
    ap.add_argument("-if", "--interruptionFilter", help="Interruption Mode (1: Show All, 2: Priority Only, 3: Total Silence, 4: AlarmsOnly",
                    type=int, choices=range(1, 5))
    ap.add_argument("-mv", "--mediaVolume", help="Media Volume - number from 0 to 15", type=int, choices=range(0, 16))
    ap.add_argument("-av", "--alarmVolume", help="Media Volume - number from 0 to 7", type=int, choices=range(0, 8))
    ap.add_argument("-rv", "--ringVolume", help="Ringer Volume - number from 0 to 7", type=int, choices=range(0, 8))
    return ap.parse_args(argue)


def devices(deviceFile):
    try:  # loads device json into a dictionary
        with open(deviceFile, "r") as device:
            deviceData = json.loads(device.read())
    except:
        os.system("joinsetup.py -d")
        with open(deviceFile, "r") as device:
            deviceData = json.loads(device.read())
    return deviceData


def contacts(contactsFile):
    try:  # loads the contacts json if a number or name is supplied.
        with open(contactsFile, "r") as contact:
            contactData = json.loads(contact.read())
    except:  # defaults to a number if a name is not found in the json
        contactData = {}
    return contactData
