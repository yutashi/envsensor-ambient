#! /usr/bin/env pyhton3
from envstatus import EnvStatus
import ambient
import os
import time
import datetime


AMBIENT_CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
AMBIENT_WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
BLUETHOOTH_DEVICEID = os.environ.get('BLUETHOOTH_DEVICEID', 0)
BLUETHOOTH_DEVICE_ADDRESS = os.environ.get('BLUETHOOTH_DEVICE_ADDRESS', 'DDF4AECB2D68')
CHECK_SPAN = int(os.environ.get('CHECK_SPAN', '30'))

o = EnvStatus(bt=BLUETHOOTH_DEVICEID)
o.start()
uId = o.setRequest(BLUETHOOTH_DEVICE_ADDRESS)

am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)

latest_update = datetime.datetime.now()
while True:
    data = o.getLatestData(uId)
    if data is not None:

        if data.tick_last_update > latest_update:
            am.send({
                'created': data.tick_last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'd1': data.val_temp,
                'd2': data.val_pressure,
                'd3': data.val_humi,
                'd4': data.val_light,
                'd5': data.val_uv,
                'd6': data.val_noise,
                'd7': data.rssi,
                'd8': data.val_battery,
                }
            )

        latest_update = data.tick_last_update

    time.sleep(CHECK_SPAN)
