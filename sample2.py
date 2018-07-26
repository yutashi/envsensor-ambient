#! /usr/bin/env pyhton3
from envstatus import EnvStatus
import ambient
import os
import sys
import time
import datetime


AMBIENT_CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
AMBIENT_WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
CHECK_SPAN = int(os.environ.get('CHECK_SPAN', '30'))

BLUETOOTH_DEVICEID = os.environ.get('BLUETOOTH_DEVICEID', 0)
BLUETOOTH_DEVICE_ADDRESS = os.environ.get('BLUETOOTH_DEVICE_ADDRESS', None)
if BLUETOOTH_DEVICE_ADDRESS is None:
    sys.exit('No sensors found')

o = EnvStatus(bt=BLUETOOTH_DEVICEID)
uId = o.setRequest(BLUETOOTH_DEVICE_ADDRESS)
o.start()

am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)

latest_update = datetime.datetime.now()
while True:
    data = o.getLatestData(uId)
    if data is not None:

        if data.tick_last_update > latest_update:
            am.send({
                'created': data.tick_last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'd1': data.val_temp,
                }
            )

        latest_update = data.tick_last_update

    time.sleep(CHECK_SPAN)
