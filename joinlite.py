import urllib.request, urllib.parse, json, re, sys
def pushFunc( url ):
    if url is True:
        encodedPush = '&clipboard=' + encoded + '&url=' + encoded + ''
    if url is False:
        encodedPush = '&clipboard=' + encoded + ''
    try:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + devices[device] + encodedPush + '')
    except:
        urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?deviceId=' + device + encodedPush + '&apikey=' + deviceData['apikey'] + '')
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
push = ' '.join(sys.argv[2:])
encoded = urllib.parse.quote_plus(push)
device = sys.argv[1]
try:
    deviceJSON = open('devices.json','r')
    deviceData = json.loads(deviceJSON.read())
except:
    refresh(True)
if device == 'refresh':
    refresh(False)
if device != 'refresh':
    deviceJSON.close()
    devices = {}
    for x in deviceData['records']:
        devices[x['deviceName']] = x['deviceId']
    if re.match('^https://.*',push) is not None:
        pushFunc(True)
    else:
        pushFunc(False)
else:
    print('No device defined.')
