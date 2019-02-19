# JoinPython

A python script that allows for pushing to Join by Joaoapps from the command line.

![image](https://i.imgur.com/9Yv4YVl.gif)

## Requires

-   Python3
-   A Join Account

## Setup

-   Run `pip3 install joinpython` or `pip3 install git+https://github.com/Rayquaza01/JoinPython`
-   Run `join.py --setup` to start the setup (optional)

### The Config File

If you run setup, a config file is created at `~/JoinPython.json` with your device and contact data. This allows you to omit certain arguments (`--apikey`, `--deviceId`, etc.) when running the program.  
If you have a file named `JoinPython.json` in your current directory, it will be used instead of the one in your home folder.

Sample config file:

```json
{
    "version": "VERSION",
    "apikey": "YOUR_API_KEY",
    "default_device": "Phone",
    "contacts": {
        "Name 1": "5555555555"
    },
    "devices": {
        "Phone": "PHONE_DEVICE_ID",
        "Tablet": "TABLET_DEVICE_ID"
    }
}
```

### Contacts Setup

The `--smsnumber` and `--callnumber` arguments take a phone number to be used by Join. You can edit the config file (`~/JoinPython.json`) with contact names to allow these arguments to take a name instead.  
The contacts section should look something like this:

```json
{
    "Name 1": "5555555555",
    "Name 2": "(555) 555-5555",
    "Name 3": "+1 555.555.5555"
}
```

The actual formatting of the numbers is unimportant; Join should be able to handle most formats.  
You can also use [this Tasker task](https://raw.githubusercontent.com/Rayquaza01/JoinPython/master/ContactsGenerator.tsk.xml) ([also available here](https://taskernet.com/shares/?user=AS35m8ln60P2bw2QxMdurJqOe5aESjUdS8HTc0B35EGwTB2qVtotZiazaLMpwomX2PvkhnktwDQ%3D&id=Task%3AJoinPythonContactsGenerator)) to pull the numbers from your phone's contacts (Requires Tasker, AutoTools, and AutoContacts to run)

`--smscontactname` can be used instead of contact setup, but contact setup is still required for `--callnumber` and `--smsnumber`

## Usage

Run `join.py` with arguments corresponding to what you want to do. Arguments correspond directly to [the Join API](https://joaoapps.com/join/api/) (Ex: The clipboard parameter is `--clipboard`). `join.py --help` gives a list of accepted arguments.

### Irregularities

-   The `deviceNames` parameter is used when `--deviceId` is given a comma separated list of names. `deviceIds` is never used right now.
-   Including a comma anywhere in the `--deviceId` parameter will force it to use `deviceNames`, even if you only list one device. `join.py -d Phone -c test` won't work without `devices.json`, but `join.py -d Phone, -c test` will.
-   `--deviceId` can take device names, groups, or use an ID directly.
-   `--apikey` can take an API key or be ommitted to use the key in `devices.json`
-   `--generateURL` prints the Join API URL without actually calling it.

### As a module

```python
#!/usr/bin/env python3
import joinpython as join
args = {
    "deviceId": "DEVICE_ID_HERE",
    "apikey": "API_KEY_HERE",
    "clipboard": "Clipboard Text",
    "find": True
}
response = join.request(args)
```

## Old Version

The older (pre pip installation support) version is still available at https://github.com/Rayquaza01/JoinPython/releases/tag/0.0.0  
The main differences are:

-   The older versions did not have version numbers
-   The contact and device data was stored in two separate files
-   The config file was stored in the installation directory, not the home folder
-   It can now be imported as a module without copying the join.py file
-   Pip handles adding the script to the path automatically
