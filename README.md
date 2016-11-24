# JoinPython
A python script that allows for pushing to Join by Joaoapps from the command line.

Setup:

1. Go to the [Join web-interface](https://joinjoaomgcd.appspot.com/)
2. Choose a device.
3. Click Join API.
4. Click the Show button.
5. Run join.py and enter the API key shown when requested.

Contacts setup:

1. Go to [Google Contacts](https://www.google.com/contacts/u/0/?cplus=0#contacts) (Old view is needed. Preview doesn't support exporting)
2. Click more
3. Click export
4. Make sure Google CSV is selected and download the CSV file
5. Place google.csv in join.py's directory and run `join.py -r False contacts`

Arguments for join.py

```
-d [DeviceName] or --device [DeviceName]
    The name of the device the push should go to.
    Accepts groups as well (group.all, group.android, group.chrome, group.windows10, group.phone, group.tablet, group.pc)
```

TODO:
* Comment code
* Write argument documentation
* Support multiple device names at once

Make sure to escape quotes (' or ") in order to push them!
