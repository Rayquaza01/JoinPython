# JoinPython
A python script that allows for pushing to Join by Joaoapps from the command line.

**Note**

Requires: Python 3 and a Join account

Only tested on Windows and Bash on Windows. Should work with other systems, though.

Devices setup:

1. Go to the [Join web-interface](https://joinjoaomgcd.appspot.com/)
2. Choose a device.
3. Click Join API.
4. Click the Show button.
5. Run `joinsetup.py -d` and enter the API key shown when requested.
6. Choose a default device to be used when the device argument is ommited.
7. devices.json should be created. End of setup.

Contacts setup:

1. Go to [Google Contacts](https://www.google.com/contacts/u/0/?cplus=0#contacts) (Old view is needed. Preview doesn't support exporting)
2. Click more
3. Click export
4. Make sure Google CSV is selected and download the CSV file
5. Place google.csv in join.py's directory and run `joinsetup.py -c`
6. contacts.json should be created. You can delete google.csv. End of setup.

OR

Requires Tasker, AutoTools, and AutoContacts

1. Add `ContactsGenerator.tsk.xml` to Tasker
2. Run the task
3. Move `contacts.json` to join.py's directory. (A share dialog will appear to send the file) End of setup.

AutoRemote Setup:

1. Run `joinsetup.py -a`.
2. Enter name of the device you want to set up.
3. Enter the short url for that device. (after the goo.gl)
4. Repeat 2 & 3 until all devices are accounted for.
5. arDevices.json should be created. End of setup.

For the best results, add join.py's working directory to your system's path.

**Arguments for join.py**

No arguments need to be surrounded with quotes, but it doesn't hurt.

```
-d [DeviceName] or --device [DeviceName] !REQUIRED!
    The name of the device the push should go to.
    Accepts groups (group.all, group.android, group.chrome, group.windows10, group.phone,
    group.tablet, group.pc) and multiple device names (Phone,Tablet,Desktop) as well.
-c [Clipboard] or --clipboard [Clipboard]
    Clipboard
-u [URL] or --url [URL]
    URL
-f [File URL] or --file [File URL]
    File (must be a publicly accessible URL)
-smsn [Contact Name or Number] or --smsnumber [Contact Name or Number]
    Phone number to send an SMS to. If you want to set an SMS you need to set this and the smstext values.
    Contact names can be used if contacts setup is completed.
-smst [SMS Text] or --smstext [SMS Text]
    Some text to send in an SMS. If you want to set an SMS you need to set this and the smsnumber values
-fi [True] or --find [True]
    Set to true to make your device ring loudly
-w [Wallpaper URL] or --wallpaper [Wallpaper URL]
    URL to an image to set as the target device's wallpaper
-ti [Title] or --title [Title]
    Title (If set will create notification)
-te [Text] or --text [Text]
    Text (Tasker Command or notification text)
-i [Icon URL] or --icon [Icon URL]
    Icon URI (publicly accessible URL or local file URI; used whenever a notification is created)
-s [Icon URL] or --smallicon [Icon URL]
    Icon URI to be used as the statusbar icon (Android 6.0 and above)
-p [Priority] or --priority [Priority]
    Priority of the notification from -2 (lowest) to 2 (highest) (Default is 2)
-v [Vibration Pattern] or --vibration [Vibration Pattern]
    Vibration for when the notification is recived. Generate the pattern at
    http://autoremotejoaomgcd.appspot.com/AutoRemoteNotification.html
```

Make sure to escape quotes (\") in order to push them!
