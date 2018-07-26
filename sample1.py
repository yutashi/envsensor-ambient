#! /usr/bin/env pyhton3
from envstatus import EnvStatus
import os
import time
import datetime


BLUETHOOTH_DEVICEID = os.environ.get('BLUETHOOTH_DEVICEID', 0)
BLUETHOOTH_DEVICE_ADDRESS = os.environ.get('BLUETHOOTH_DEVICE_ADDRESS', 'DDF4AECB2D68')
CHECK_SPAN = int(os.environ.get('CHECK_SPAN', '10'))

o = EnvStatus(bt=BLUETHOOTH_DEVICEID)
o.start()
uId = o.setRequest(BLUETHOOTH_DEVICE_ADDRESS)

latest_update = datetime.datetime.now()
while True:
    data = o.getLatestData(uId)
    if data is not None:

        if data.tick_last_update > latest_update:
            print('Illumination: {} lx'.format(data.val_light))

        latest_update = data.tick_last_update

    time.sleep(CHECK_SPAN)
