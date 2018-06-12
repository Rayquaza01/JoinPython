#!/usr/bin/env python3
import urllib.request
import json
import csv
import os
import argparse


def devices(apikeyOld, prefOld):
    if os.path.isfile("devices.json"):
        with open("devices.json", "r") as deviceJSON:
            deviceDataOld = json.loads(deviceJSON.read())
            apikeyOld = deviceDataOld["apikey"]
            prefOld = deviceDataOld["pref"]
    else:
        apikeyOld = ""
        prefOld = ""
    print("Devices Setup")
    print("An API key is needed. Get your key at "
          "https://joinjoaomgcd.appspot.com/")
    apikey = input("Enter your key (leave blank to reuse pre-existing key): ")
    if apikey == "":  # allows for using a pre-existing key
        apikey = apikeyOld
    devices = urllib.request.urlopen("https://joinjoaomgcd.appspot.com/_ah/api"
                                     "/registration/v1/listDevices?apikey=" +
                                     apikey).read()
    data = json.loads(devices.decode("utf-8"))
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


def contacts():
    print("Contacts Setup")
    print("Export your google contacts csv file into the working directory as "
          "google.csv")
    print("https://www.google.com/contacts/u/0/?cplus=0# contacts is where you"
          "can export the file.")
    print("Export the file in the Google format.")
    input("Press enter when this is done or close the window to cancel "
          "contacts setup")
    contactsData = {}
    with open("google.csv", "r") as c:
        read = csv.reader(c)
        for row in read:
            if row[31] == "Mobile":
                contactsData[row[0]] = row[32]
            if row[33] == "Mobile":
                contactsData[row[0]] = row[34]
    data = json.dumps(contactsData, sort_keys=True, indent=4)  # write to file
    with open("contacts.json", "w") as f:
        f.write(str(data))
    print("Sucessfully saved contacts data to contacts.json! "
          "You can delete google.csv")
    print("")


def main():
    os.chdir(os.path.dirname(__file__))  # sets a constant working dir
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--devices",  nargs="*")
    ap.add_argument("-c", "--contacts", nargs="*")
    opts = ap.parse_args()
    if opts.devices is not None:
        devices()
    if opts.contacts is not None:
        contacts()
    print("For more instructions, view the readme.")
    print("This concludes the setup.")
    input("Press enter or close the window.")


if __name__ == "__main__":
    main()
