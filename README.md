# JoinPython
A python script that allows for pushing to Join by Joaoapps from the command line.

**Note**

Requires: Python 3 and a Join account

Only tested on Windows and Bash on Windows. Should work with other systems, though.

[Installation Instructions](https://github.com/Rayquaza01/JoinPython/wiki/Installation)

[Contacts Setup](https://github.com/Rayquaza01/JoinPython/wiki/Contacts-Setup)

[Escape Characters](https://github.com/Rayquaza01/JoinPython/wiki/Escape-Characters)

**Arguments for join.py**

No arguments need to be surrounded with quotes, but it doesn't hurt.

```
-d [DeviceName] or --device [DeviceName] (Uses pref defined on setup if this is not passed)
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
-mms [MMS file] or --mmsfile [MMS file]
    A file to send in a MMS. smsnumber must be set for this to take affect.
-cn [Contact Name or Number] or --callnumber [Contact Name or Number]
    A phone number to call on the target device
-fi [True] or --find [True]
    Set to true to make your device ring loudly
-w [Wallpaper URL] or --wallpaper [Wallpaper URL]
    URL to an image to set as the target device's wallpaper
-lw [Wallpaper URL] or --lockWallpaper [Wallpaper URL]
    URL to an image to set as the target device's lockscreen wallpaper (Android 7 or above)
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
