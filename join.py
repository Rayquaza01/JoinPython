import argparse, urllib.request, urllib.parse, json
def refresh( keyNeeded ):
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
ap = argparse.ArgumentParser()
ap.add_argument('-te','--text',help='Text (Tasker Command or notification text)')
ap.add_argument('-ti','--title',help='Title (If set will create notification)')
ap.add_argument('-i','--icon',help='Icon URI (publicly accessible URL or local file URI; used whenever a notification is created)')
ap.add_argument('-u','--url',help='URL')
ap.add_argument('-c','--clipboard',help='Clipboard')
ap.add_argument('-f','--file',help='File (must be a publicly accessible URL)')
ap.add_argument('-d','--device',help='The device name or a group (group.all, group.android, group.chrome, group.windows10, group.phone, group.tablet, group.pc)')
ap.add_argument('-r','--refresh',nargs='*',help='Refreshes the device list. Will request an API key if devices.json is missing from the working directory.')
opts = ap.parse_args()
argsdict = {'text': opts.text, 'title': opts.title, 'icon': opts.icon, 'url': opts.url, 'clipboard': opts.clipboard, 'file': opts.file}
try:
    deviceJSON = open('devices.json','r')
    deviceData = json.loads(deviceJSON.read())
except:
    refresh(True)
if opts.refresh is not None:
    refresh(False)
if opts.device is not None:
    deviceJSON.close()
    devices = {}
    for x in deviceData['records']:
        devices[x['deviceName']] = x['deviceId']
    encoded = []
    for key, value in argsdict.items():
        try:
            encoded.append('&' + key + '=' + urllib.parse.quote_plus(value) + '')
        except:
            encoded.append('')
    try:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + devices[opts.device] + ''.join(encoded) + '')
    except:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + opts.device + ''.join(encoded) + '&apikey=' + deviceData['apikey'] + '')
else:
    print('No device defined.')
