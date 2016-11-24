import argparse, urllib.request, urllib.parse, json, os
os.chdir(os.path.dirname(__file__)) #sets a constant working dir
##### Argument Parser starts here #####
ap = argparse.ArgumentParser()
ap.add_argument('-te','--text',help='Text (Tasker Command or notification text)',nargs='*')
ap.add_argument('-ti','--title',help='Title (If set will create notification)',nargs='*')
ap.add_argument('-i','--icon',help='Icon URI (publicly accessible URL or local file URI; used whenever a notification is created)')
ap.add_argument('-s','--smallicon',help='Icon URI to be used as the statusbar icon')
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
opts = ap.parse_args()
##### Argument Parser ends here #####
argsdict = {'text': opts.text, 'title': opts.title, 'icon': opts.icon, 'smallicon': opts.smallicon, 'priority': opts.priority, 'vibration': opts.vibration, 'url': opts.url, 'clipboard': opts.clipboard, 'file': opts.file, 'smsnumber': opts.smsnumber, 'smstext': opts.smstext, 'find': opts.find, 'wallpaper': opts.wallpaper, 'device': opts.device} #puts args into a dictionary for more convinient use
for key, value in argsdict.items(): #curcumvents the need to encase args in quotes
    if type(value) is list:
        argsdict[key] = ' '.join(value)
    if type(value) is str:
        argsdict[key] = value
try: #loads device json into a dictionary
    with open('devices.json','r') as device:
        deviceData = json.loads(device.read())
except:
    print('Could not read devices. Please run setup.py')
if opts.smsnumber is not None:
    try: #loads the contacts json as a dictionary if a number or name is supplied.
        with open('contacts.json','r') as contact:
            contactData = json.loads(contact.read())
        argsdict['smsnumber'] = contactData[argsdict['smsnumber']] #replaces the name with the number
    except: #defaults to a number if a name is not found in the json
        print('No contact names found. Using numbers. Run setup.py for instructions on using names.')
if opts.device is not None: #main process
    encoded = []
    deviceName = argsdict['device']
    argsdict.pop('device',None) #removes device from argsdict to prevent sending extra params
    for key, value in argsdict.items(): #sets up params to send to join
        if value is not None:
            encoded.append('&' + key + '=' + urllib.parse.quote_plus(value) + '')
        if value is None:
            encoded.append('')
    encodedPush = ''.join(encoded) #finalizes params
    if 'group' not in deviceName: #push to send if going to an individual device
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + deviceData[deviceName] + encodedPush + '')
    if 'group' in deviceName: #push to send if going to a group
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + deviceName + encodedPush + '&apikey=' + deviceData['apikey'] + '')
else:
    print('No device defined.')
