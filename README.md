# JoinPython
A python script that allows for pushing to Join by Joaoapps from the command line.

![image](https://i.imgur.com/9Yv4YVl.gif)

## Requires
 * Python3
 * A Join Account
## Setup
 * Download JoinPython somewhere on your computer.
   * You can download it here: https://github.com/Rayquaza01/JoinPython/archive/master.zip
   * You can also run `git clone https://github.com/Rayquaza01/JoinPython` if that's more your style
   * It may be helpful to add the folder it's in to your path
 * Run `join.py --setup` to start the setup
   * Setup can be skipped if you pass `--deviceId` and `--apikey` parameters to the script. Setup is for convenience only.
   * Enter your Join API key when requested
   * Choose a device to default to when you omit the `--deviceId` argument
   * A file named `devices.json` will be created in the same directory that contains all of your device IDs and API key.
   * `--deviceId` can be a device name if you complete setup, must be an ID otherwise.
### Contacts Setup
The `--smsnumber` and `--callnumber` arguments take a phone number to be used by Join. You can create a file named `contacts.json` with contact names to allow these arguments to take a name instead.  
The file should look something like this:
```
{
    "Name 1": "5555555555",
    "Name 2": "(555) 555-5555",
    "Name 3": "+1 555.555.5555"
}

```
The actual formatting of the numbers is unimportant; Join should be able to handle most formats.  
You can also use [this Tasker task](https://raw.githubusercontent.com/Rayquaza01/JoinPython/master/ContactsGenerator.tsk.xml) to pull the numbers from your phone's contacts (Requires Tasker, AutoTools, and AutoContacts to run)
#### Update:
 * **2018-07-25**: You can use `--smscontactname` instead of this contacts setup. Contacts setup will still work, and is still required to use contact names in `--callnumber` and `--smsnumber`.
## Usage
Run `join.py` with arguments corresponding to what you want to do. Arguments correspond directly to [the Join API](https://joaoapps.com/join/api/) (Ex: The clipboard parameter is `--clipboard`). `join.py --help` gives a list of accepted arguments.
### Irregularities
 * The `deviceNames` parameter is used when `--deviceId` is given a comma separated list of names. `deviceIds` is never used right now.
   * Including a comma anywhere in the `--deviceId` parameter will force it to use `deviceNames`, even if you only list one device. `join.py -d Phone -c test` won't work without `devices.json`, but `join.py -d Phone, -c test` will.
 * `--deviceId` can take device names, groups, or use an ID directly.
 * `--apikey` can take an API key or be ommitted to use the key in `devices.json`
 * `--generateURL` prints the Join API URL without actually calling it.
### join.pyw
Use `join.pyw` to run the program without any output.
### As a module
```
#!/usr/bin/env python3
import join
args = {
    "deviceId": "DEVICE_ID_HERE",
    "apikey": "API_KEY_HERE",
    "clipboard": "Clipboard Text",
    "find": True
}
response = join.request(args)
```
