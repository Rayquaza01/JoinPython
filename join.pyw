#!/usr/bin/env python3
import os
import sys
import join_module
cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
opts = vars(join_module.arguments(sys.argv[1:]))
deviceData = join_module.devices(cwd + "/devices.json")
if opts["smsnumber"] is not None or opts["callnumber"] is not None:
    contactData = join_module.contacts(cwd + "/contacts.json")
else:
    contactData = {}
join_module.request(opts, deviceData, contactData)
