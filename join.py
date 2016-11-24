import argparse, urllib.request, urllib.parse, json, csv
def refresh( keyNeeded, type ): #function for refreshing the devices
    if type == 'devices' or type == 'both':
        if keyNeeded is True:
            print('An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/')
            apikey = input('Enter your key: ')
        if keyNeeded is False:
            apikey = deviceData['apikey']
        devices = urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=' + apikey + '').read()
        data = json.loads(devices.decode('utf-8'))
        data['apikey'] = apikey
        data = json.dumps(data, sort_keys=True, indent=4)
        deviceJSON = open('devices.json','w')
        deviceJSON.write(str(data))
        print('Sucessfully saved device data to devices.json!')
        deviceJSON = open('devices.json','r')
    if type == 'contacts' or type == 'both':
        print('Export your google contacts csv file into the working directory as google.csv')
        print('https://www.google.com/contacts/u/0/?cplus=0#contacts is where you can export the file.')
        print('For more instructions, view the readme.')
        input('When this is done, press enter.')
        contactsDict = {}
        with open('google.csv','r') as contacts:
            read = csv.reader(contacts)
            for row in read:
                if row[31] == 'Mobile':
                    contactsDict[row[0]] = row[32]
                if row[33] == 'Mobile':
                    contactsDict[row[0]] = row[34]
        data = json.dumps(contactsDict, sort_keys=True, indent=4)
        contactsJSON = open('contacts.json','w')
        contactsJSON.write(str(data))
        print('Sucessfully saved contacts data to contacts.json!')
##### Argument Parser starts here #####
ap = argparse.ArgumentParser()
ap.add_argument('-te','--text',help='Text (Tasker Command or notification text)',nargs='*')
ap.add_argument('-ti','--title',help='Title (If set will create notification)',nargs='*')
ap.add_argument('-i','--icon',help='Icon URI (publicly accessible URL or local file URI; used whenever a notification is created)')
ap.add_argument('-si','--smallicon',help='Icon URI to be used as the statusbar icon')
ap.add_argument('-p','--priority',help='Priority of the notification from -2 (lowest) to 2 (highest and default)')
ap.add_argument('-v','--vibration',help='Vibration for when the notification is recived. Generate the pattern at http://autoremotejoaomgcd.appspot.com/AutoRemoteNotification.html')
ap.add_argument('-u','--url',help='URL')
ap.add_argument('-c','--clipboard',help='Clipboard',nargs='*')
ap.add_argument('-f','--file',help='File (must be a publicly accessible URL)')
ap.add_argument('-d','--device',help='The device name or a group (group.all, group.android, group.chrome, group.windows10, group.phone, group.tablet, group.pc)',nargs='*')
ap.add_argument('-smsn','--smsnumber',help='Phone number to send an SMS to. If you want to set an SMS you need to set this and the smstext values',nargs='*')
ap.add_argument('-smst','--smstext',help='Some text to send in an SMS. If you want to set an SMS you need to set this and the smsnumber values',nargs='*')
ap.add_argument('-fi','--find',help='Set to true to make your device ring loudly')
ap.add_argument('-w','--wallpaper',help='A publicly accessible URL of an image file. Will set the wallpaper on the receiving device')
ap.add_argument('-r','--refresh',nargs='*',help='Refreshes the device list. Will request an API key if devices.json is missing from the working directory. Add True to force asking for an API key and False to use the pre existing key. Add devices, contacts, or both to define what should be refreshed.')
opts = ap.parse_args()
##### Argument Parser ends here #####
argsdict = {'text': opts.text, 'title': opts.title, 'icon': opts.icon, 'smallicon': opts.smallicon, 'priority': opts.priority, 'vibration': opts.vibration, 'url': opts.url, 'clipboard': opts.clipboard, 'file': opts.file, 'smsnumber': opts.smsnumber, 'smstext': opts.smstext, 'find': opts.find, 'wallpaper': opts.wallpaper, 'device': opts.device} #puts args into a dictionary for more convinient use
for key, value in argsdict.items(): #curcumvents the need to encase args in quotes
    if type(value) is list:
        argsdict[key] = ' '.join(value)
    if type(value) is str:
        argsdict[key] = value
#refreshes devices if devices.json doesn't exist or if launched with the -r arg
try:
    deviceJSON = open('devices.json','r')
    deviceData = json.loads(deviceJSON.read()) #reads and converts JSON into dict
except:
    refresh(True, 'devices')
if opts.smsnumber is not None:
    try:
        contactsJSON = open('contacts.json','r')
        contactsData = json.loads(contactsJSON.read())
    except:
        refresh(False, 'contacts')
    if contactsData[argsdict['smsnumber']]:
        argsdict['smsnumber'] = contactsData[argsdict['smsnumber']]
    else:
        number = argsdict['smsnumber']
if opts.refresh is not None:
    refresh(opts.refresh[0], opts.refresh[1])
if opts.device is not None:
    devices = {}
    for x in deviceData['records']:
        devices[x['deviceName']] = x['deviceId']
    encoded = []
    for key, value in argsdict.items():
        try:
            encoded.append('&' + key + '=' + urllib.parse.quote_plus(value) + '')
        except:
            encoded.append('')
    encodedPush = ''.join(encoded)
    try:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + devices[argsdict['device']] + encodedPush + '')
    except:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + opts.device + encodedPush + '&apikey=' + deviceData['apikey'] + '')
else:
    print('No device defined.')
