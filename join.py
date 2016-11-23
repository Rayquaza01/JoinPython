import argparse, urllib.request, urllib.parse, json
ap = argparse.ArgumentParser()
ap.add_argument('-te','--text')
ap.add_argument('-ti','--title')
ap.add_argument('-i','--icon')
ap.add_argument('-u','--url')
ap.add_argument('-c','--clipboard')
ap.add_argument('-f','--file')
ap.add_argument('-d','--device')
ap.add_argument('-r','--refresh')
opts = ap.parse_args()
try:
    deviceJSON = open('devices.json','r')
except:
    print('An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/')
    apikey = input('Enter your key: ')
    devices = urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=' + apikey + '').read()
    deviceJSON = open('devices.json','w')
    deviceJSON.write(devices.decode('utf-8'))
