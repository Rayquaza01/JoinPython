#!/usr/bin/env python3
import os
import sys
import argparse
import json
import urllib.request
import urllib.parse


def setup():
    if os.path.isfile("devices.json"):
        with open("devices.json", "r") as deviceJSON:
            deviceDataOld = json.loads(deviceJSON.read())
            apikeyOld = deviceDataOld["apikey"]
            prefOld = deviceDataOld["pref"]
    else:
        apikeyOld = ""
        prefOld = ""
    print("Devices Setup")
    print("An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/")
    apikey = input("Enter your key (leave blank to reuse pre-existing key): ")
    if apikey == "":  # allows for using a pre-existing key
        apikey = apikeyOld
    devices = urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=" +
                                     apikey).read().decode("utf-8")
    data = json.loads(devices)
    deviceData = {}
    deviceData["apikey"] = apikey
    for x in data["records"]:  # converts json to dict to simplify it
        deviceData[x["deviceName"]] = x["deviceId"]
        print(x["deviceName"])
    pref = input("Choose the device name that you want to push to if no "
                 "device is defined: ")
    if pref == "":
        pref = prefOld
    deviceData["pref"] = pref
    data = json.dumps(deviceData, sort_keys=True, indent=4)  # write to file
    with open("devices.json", "w") as f:
        f.write(str(data))
    print("Sucessfully saved device data to devices.json!")
    print("")


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
    ap.add_argument("-ac", "--actions", help="Set notification buttons with customized behaviour. "
                    "See https://joaoapps.com/join/actions/#notifications", nargs="*")
    ap.add_argument("-c", "--clipboard", help="Clipboard", nargs="*")
    ap.add_argument("-f", "--file", help="File (must be a publicly accessible URL)")
    ap.add_argument("-d", "--device", help="The device name or a group (group.all, group.android, group.chrome, group.windows10, group."
                    "phone, group.tablet, group.pc)", nargs="*")
    ap.add_argument("-smsn", "--smsnumber", help="Phone number to send an SMS to. If you want to set an SMS you need to set this and the "
                    "smstext values", nargs="*")
    ap.add_argument("-cn", "--callnumber", nargs="*", help="A number to call")
    ap.add_argument("-smst", "--smstext", help="Some text to send in an SMS. If you want to set an SMS you need to set this and the "
                    "smsnumber values", nargs="*")
    ap.add_argument("-fi", "--find", help="Set to true to make your device ring loudly", action="store_true")
    ap.add_argument("-w", "--wallpaper", help="A publicly accessible URL of an image file. Will set the wallpaper on the receiving device")
    ap.add_argument("-mmss", "--mmssubject", help="Subject for the message. This will make the sent message be an MMS instead of an SMS",
                    nargs="*")
    ap.add_argument("-mmsu", "--mmsurgent", help="Set to 1 if this is an urgent MMS. This will make the sent message be an MMS instead of"
                    " an SMS", action="store_true")
    ap.add_argument("-mms", "--mmsfile", help="MMS file. smsnumber must be set for this to have an affect")
    ap.add_argument("-lw", "--lockWallpaper", help="The wallpaper to set on the lockscreen (Android 7+), must be publicly accessible URL")
    ap.add_argument("-if", "--interruptionFilter", help="Interruption Mode (1: Show All, 2: Priority Only, 3: Total Silence, 4: AlarmsOnly",
                    type=int, choices=range(1, 5))
    ap.add_argument("-mv", "--mediaVolume", help="Media Volume - number from 0 to 15", type=int, choices=range(0, 16))
    ap.add_argument("-av", "--alarmVolume", help="Media Volume - number from 0 to 7", type=int, choices=range(0, 8))
    ap.add_argument("-rv", "--ringVolume", help="Ringer Volume - number from 0 to 7", type=int, choices=range(0, 8))
    ap.add_argument("-sa", "--say", help="Say some text out loud.", nargs="*")
    ap.add_argument("-l", "--language", help="The language to use for the say text", nargs="*")
    ap.add_argument("-a", "--app", help="App name of the app you want to open on the remote device", nargs="*")
    ap.add_argument("-ap", "--appPackage", help="Package name of the app you want to open on the remote device. You can check the package "
                    "name for an app by going to its Google Play page and checking the end of the URL. Example: for YouTube this is the "
                    "URL (https://play.google.com/store/apps/details?id=com.google.android.youtube) and this is the package"
                    "name (com.google.android.youtube)", nargs="*")
    ap.add_argument("-gu", "--generateURL", help="Print push url rather than actually pushing", action="store_true")
    ap.add_argument("--setup", action="store_true", help="Initiate setup")
    return ap.parse_args(argue)


def devices(deviceFile):
    if os.path.isfile(deviceFile):  # loads device json into a dictionary
        with open(deviceFile, "r") as device:
            deviceData = json.loads(device.read())
    else:
        setup()
        with open(deviceFile, "r") as device:
            deviceData = json.loads(device.read())
    return deviceData


def contacts(contactsFile):
    if os.path.isfile(contactsFile):  # loads the contacts json if a number or name is supplied.
        with open(contactsFile, "r") as contact:
            contactData = json.loads(contact.read())
    else:  # defaults to a number if a name is not found in the json
        contactData = {}
    return contactData


def request(args, devices, contacts={}):
    generateURL = args["generateURL"]
    args.pop("generateURL", None)
    args.pop("setup", None)
    if args["device"] is None:
        args["device"] = devices["pref"]
    for key, value in args.items():  # fixes the need to encase args in quotes
        if type(value) is list:
            args[key] = " ".join(value)
    if args["smsnumber"] is not None:
        if args["smsnumber"] in contacts:
            args["smsnumber"] = contacts[args["smsnumber"]]
    if args["callnumber"] is not None:
        if args["callnumber"] in contacts:
            args["callnumber"] = contacts[args["callnumber"]]
    if args["find"]:
        args["find"] = "true"
    else:
        args.pop("find", None)
    if args["mmsurgent"]:
        args["mmsurgent"] = "1"
    else:
        args.pop("mmsurgent", None)
    deviceName = args["device"]
    args.pop("device", None)  # removes device to prevent sending extra params
    args["apikey"] = devices["apikey"]
    # https://plus.google.com/+Jo%C3%A3oDias/posts/GYwEvtSb238
    if "," in deviceName:  # allows for multiple device names separated by commas
        args["deviceNames"] = deviceName
    elif "group" in deviceName:  # allows for groups (group.android, etc.)
        args["deviceId"] = deviceName
    else:  # allows for single device
        args["deviceId"] = devices[deviceName]
    encoded = []
    for key, value in args.items():
        if value is not None:
            encoded.append("=".join([key, urllib.parse.quote_plus(str(value))]))
    url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?" + "&".join(encoded)
    if generateURL:
        return url
    else:
        return urllib.request.urlopen(url).read().decode("utf-8")


def main():
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    opts = vars(arguments(sys.argv[1:]))
    if opts["setup"]:
        setup()
    deviceData = devices(cwd + "/devices.json")
    if opts["smsnumber"] is not None or opts["callnumber"] is not None:
        contactData = contacts(cwd + "/contacts.json")
    else:
        contactData = {}
    print(request(opts, deviceData, contactData))


if __name__ == "__main__":
    main()
