#!/usr/bin/env python3
import joinpython as join
import os
import json
import argparse


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
    ap.add_argument("--config", help="The config file")
    return ap.parse_args()


def configExists(name, cfg):
    if cfg is not None and os.path.exists(cfg):
        return cfg
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
        # load blank config if there is no config file
        deviceData = {
            "devices": {},
            "default_device": "",
            "apikey": "",
            "contacts": {},
            "version": join.version
        }
    return deviceData


def setup(cfg):
    print("JoinPython Setup")
    configFile = cfg if cfg is not None else os.path.expanduser("~/JoinPython.json")

    # get old info from config, if it exists
    if os.path.isfile(configFile):  # save old config options
        with open(configFile, "r") as deviceJSON:
            configOld = json.loads(deviceJSON.read())
            apikeyOld = configOld["apikey"]
            prefOld = configOld["default_device"]
            contactsOld = configOld["contacts"]
    else:
        apikeyOld = ""
        prefOld = ""
        contactsOld = {}

    # base config
    config = {"devices": {}, "contacts": contactsOld, "version": join.version}

    # ask for key
    print("An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/")
    apiPrompt = "Enter your API key"
    if apikeyOld != "":
        apiPrompt += " ({})".format(apikeyOld)
    config["apikey"] = input(apiPrompt + ": ")
    if config["apikey"] == "":  # allows for using a pre-existing key
        config["apikey"] = apikeyOld

    print("")
    print("Devices:")

    # get list of devices
    devices = join.listDevices(config["apikey"])

    # store device names and ids to config, print names
    for device in devices["records"]:  # converts json to dict to simplify it
        config["devices"][device["deviceName"]] = device["deviceId"]
        print("  " + device["deviceName"])
    print("")

    prefPrompt = "Choose the device name that you want to push to if you don't provide the deviceId argument"
    if prefOld != "":
        prefPrompt += " ({})".format(prefOld)
    config["default_device"] = input(prefPrompt + ": ")
    if config["default_device"] == "":
        config["default_device"] = prefOld

    # write config
    with open(configFile, "w") as f:
        f.write(json.dumps(config, sort_keys=True, indent=4))

    print("Sucessfully saved device data to {0}!".format(configFile))
    print("")


def fixOpts(opts, config):
    # remove setup, config key
    opts.pop("setup", None)
    opts.pop("config", None)

    # remove None and False from opts
    tempArgs = opts.copy()
    for value in tempArgs:
        if tempArgs[value] is None or not tempArgs[value]:
            if type(tempArgs[value]) is not int:  # keep values with 0, like volume
                opts.pop(value, None)  # Pop none parameters

    for key, value in opts.items():  # fixes the need to encase opts in quotes
        if type(value) is list:
            opts[key] = " ".join(value)

    # put api key in opts if not provided
    if "apikey" not in opts:
        opts["apikey"] = config["apikey"]

    # replace contact names with phone numbers if "smsnumber" in opts:
    if "smsnumber" in opts:
        if opts["smsnumber"] in config["contacts"]:
            opts["smsnumber"] = config["contacts"][opts["smsnumber"]]
    if "callnumber" in opts:
        if opts["callnumber"] in config["contacts"]:
            opts["callnumber"] = config["contacts"][opts["callnumber"]]

    # fill in default device if not provided
    if "deviceId" not in opts:
        opts["deviceId"] = config["default_device"]

    if "," in opts["deviceId"]:  # replace device id with device names if comma present
        opts["deviceNames"] = opts["deviceId"]
        opts.pop("deviceId", None)
    elif opts["deviceId"].startswith("group."):  # leave alone if group is in device id
        pass
    elif opts["deviceId"] in config["devices"]:  # replace device name with device id
        opts["deviceId"] = config["devices"][opts["deviceId"]]

    return opts


def main():
    opts = vars(arguments())
    if opts["setup"]:
        setup(opts["config"])
    configFile = configExists("JoinPython.json", opts["config"])
    if configFile:
        print("Using config {0}".format(configFile))
    config = loadConfig(configFile)

    # Update config to new version, move non devices out of devices section
    if "version" not in config:
        config["apikey"] = config["devices"]["apikey"]
        config["devices"].pop("apikey", None)
        config["default_device"] = config["devices"]["pref"]
        config["devices"].pop("pref", None)
        config["version"] = join.version
        with open(configFile, "w") as f:
            f.write(json.dumps(config, sort_keys=True, indent=4))
        print("Updated config!")

    # process args, prepare for sending to join
    opts = fixOpts(opts, config)

    response = join.request(opts)
    # print error message if not successful
    if type(response) is dict:
        if not response["success"]:
            print(response["errorMessage"])
    # print generated url
    else:
        print(response)


if __name__ == "__main__":
    main()
