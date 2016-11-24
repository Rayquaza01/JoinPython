import urllib.request, json, csv
print('An API key is needed. Get your key at https://joinjoaomgcd.appspot.com/')
apikey = input('Enter your key (leave blank to reuse pre-existing key): ')
if apikey == '':
    with open('devices.json','r') as deviceJSON:
        deviceData = json.loads(deviceJSON.read())
        apikey = deviceData['apikey']
devices = urllib.request.urlopen('https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey=' + apikey + '').read()
data = json.loads(devices.decode('utf-8'))
data['apikey'] = apikey
data = json.dumps(data, sort_keys=True, indent=4)
deviceJSON = open('devices.json','w')
deviceJSON.write(str(data))
deviceJSON.close()
print('Sucessfully saved device data to devices.json!')
print('')
print('Export your google contacts csv file into the working directory as contacts.csv')
print('https://www.google.com/contacts/u/0/?cplus=0#contacts is where you can export the file.')
print('Export the file in the Google format.')
input('Press enter when this is done.')
contactsData = {}
with open('google.csv','r') as contacts:
    read = csv.reader(contacts)
    for row in read:
        if row[31] == 'Mobile':
            contactsData[row[0]] = row[32]
        if row[33] == 'Mobile':
            contactsData[row[0]] = row[34]
data = json.dumps(contactsData, sort_keys=True, indent=4)
contactsJSON = open('contacts.json','w')
contactsJSON.write(str(data))
contactsJSON.close()
print('Sucessfully saved contacts data to contacts.json! You can delete google.csv'
print('')
print('For more instructions, view the readme.')
print('This concludes the setup.')
input('Press enter or close the window.')
