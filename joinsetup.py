#!/usr/bin/env python3
import urllib.request, json, csv, os, argparse, re
os.chdir(os.path.dirname(__file__)) # sets a constant working dir
ap = argparse.ArgumentParser()
ap.add_argument('-d','--devices',nargs='*')
ap.add_argument('-c','--contacts',nargs='*')
ap.add_argument('-a','--autoremote',nargs='*')
opts = ap.parse_args()
if opts.devices is None and opts.contacts is None and opts.autoremote is None:
    runAll = True
else:
    runAll = False
try:
    with open('devices.json','r') as deviceJSON:
        deviceDataOld = json.loads(deviceJSON.read())
        apikeyOld = deviceDataOld['apikey']
        prefOld = deviceDataOld['pref']
except:
    pass
if opts.devices is not None or runAll is True:
    print('Devices Setup')
    print('An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/')
    apikey = input('Enter your key (leave blank to reuse pre-existing key): ')
    if apikey == '': # allows for using a pre-existing key
        apikey = apikeyOld
    devices = urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=' + apikey + '').read()
    data = json.loads(devices.decode('utf-8'))
    deviceData ={}
    deviceData['apikey'] = apikey
    for x in data['records']: # converts json to dict to simplify it
        deviceData[x['deviceName']] = x['deviceId']
        print(x['deviceName'])
    pref = input('Choose the device name that you want to push to if no device is defined: ')
    if pref == '':
        pref = prefOld
    deviceData['pref'] = pref
    data = json.dumps(deviceData, sort_keys=True, indent=4) # convert back to json and write to file
    with open('devices.json','w') as f:
        f.write(str(data))
    print('Sucessfully saved device data to devices.json!')
    print('')
if opts.contacts is not None or runAll:
    print('Contacts Setup')
    print('Export your google contacts csv file into the working directory as contacts.csv')
    print('https://www.google.com/contacts/u/0/?cplus=0# contacts is where you can export the file.')
    print('Export the file in the Google format.')
    input('Press enter when this is done or close the window to cancel contacts setup')
    contactsData = {}
    with open('google.csv','r') as contacts: # converts csv to dict to simplify it
        read = csv.reader(contacts)
        for row in read:
            if row[31] == 'Mobile':
                contactsData[row[0]] = re.sub('[^\d+]', '', row[32])
            if row[33] == 'Mobile':
                contactsData[row[0]] = re.sub('[^\d+]', '', row[34])
    data = json.dumps(contactsData, sort_keys=True, indent=4) # convert to json and write to file
    with open('contacts.json','w') as f:
        f.write(str(data))
    print('Sucessfully saved contacts data to contacts.json! You can delete google.csv')
    print('')
if opts.autoremote is not None or runAll is True:
    print('Autoremote Setup')
    print('Enter the short url provided with the autoremote app (after goo.gl)')
    print('Leave blank to cancel.')
    arDict = {}
    while True:
        name = input('Enter the device\'s name: ')
        id = input('Enter the device\'s id: ')
        if name is '':
            break
        else:
            fullURL = urllib.request.urlopen('http://expandurl.com/api/v1/?url=goo.gl/' + id).read()
            arDeviceId = fullURL.decode('utf-8').split('=')
            arDict[name] = arDeviceId[1]
    data = json.dumps(arDict, sort_keys=True, indent=4)
    with open('arDevices.json','w') as f:
        f.write(str(data))
    print('Sucessfully saved Autoremote data to arDevices.json!')
    print('')
print('For more instructions, view the readme.')
print('This concludes the setup.')
input('Press enter or close the window.')
