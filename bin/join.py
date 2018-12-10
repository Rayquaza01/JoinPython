#!/usr/bin/env python3
import joinpython as join
import os
import json
import urllib.request
import argparse


def configExists(name):
    homefile = os.path.join(os.path.expanduser("~"), name)
    if os.path.exists(name):  # if file in current folder
        return name
    elif os.path.exists(homefile):  # if file in home folder
        return homefile
    else:  # file not found
        return False


def loadConfig(file):
    if os.path.isfile(file):  # loads device json into a dictionary
        with open(file, "r") as device:
            deviceData = json.loads(device.read())
    else:
        deviceData = {
            "devices": {
                "pref": ""
            },
            "contacts": {}
        }
    return deviceData


def arguments():
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
    ap.add_argument("-d", "--deviceId", help="The device name or a group (group.all, group.android, group.chrome, group.windows10, group."
                    "phone, group.tablet, group.pc)", nargs="*")
    ap.add_argument("-api", "--apikey", help="Your Join API key", nargs="?")
    ap.add_argument("-smsn", "--smsnumber", help="Phone number to send an SMS to. If you want to set an SMS you need to set this and the "
                    "smstext values", nargs="*")
    ap.add_argument("-smsc", "--smscontactname", help="Alternatively to the smsnumber you can specify this and Join will send the SMS to "
                    "the first number that matches the name", nargs="*")
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
    ap.add_argument("-dot", "--dismissOnTouch", help="set to true to make the notification go away when you touch it", action="store_true")
    ap.add_argument("-gu", "--generateURL", help="Print push url rather than actually pushing", action="store_true")
    ap.add_argument("--setup", action="store_true", help="Initiate setup")
    return ap.parse_args()


def setup():
    configFile = os.path.expanduser("~/JoinPython.json")
    if os.path.isfile(configFile):  # save old config options
        with open(configFile, "r") as deviceJSON:
            deviceDataOld = json.loads(deviceJSON.read())
            apikeyOld = deviceDataOld["devices"]["apikey"]
            prefOld = deviceDataOld["devices"]["pref"]
            contactsOld = deviceDataOld["contacts"]
    else:
        apikeyOld = ""
        prefOld = ""
        contactsOld = {}
    print("Devices Setup")
    print("An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/")
    apikey = input("Enter your key (leave blank to reuse pre-existing key): ")
    if apikey == "":  # allows for using a pre-existing key
        apikey = apikeyOld
    url = "https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=" + apikey
    deviceJSON = urllib.request.urlopen(url).read().decode("utf-8")
    data = json.loads(deviceJSON)
    deviceData = {"devices": {}, "contacts": contactsOld}
    deviceData["devices"]["apikey"] = apikey
    for x in data["records"]:  # converts json to dict to simplify it
        deviceData["devices"][x["deviceName"]] = x["deviceId"]
        print(x["deviceName"])
    pref = input("Choose the device name that you want to push to if no device is defined: ")
    if pref == "":
        pref = prefOld
    deviceData["devices"]["pref"] = pref
    data = json.dumps(deviceData, sort_keys=True, indent=4)  # write to file
    with open(configFile, "w") as f:
        f.write(data)
    print("Sucessfully saved device data to {0}!".format(configFile))
    print("")


def main():
    opts = vars(arguments())
    if opts["setup"]:
        setup()
    configFile = configExists("JoinPython.json")
    if configFile:
        print("Using config {0}".format(configFile))
    config = loadConfig(configFile)
    print(join.request(opts, config["devices"], config["contacts"]))


if __name__ == "__main__":
    main()
