from time import sleep
import datetime
import tinytuya
import os

def current_time():
    time = datetime.datetime.now().time()
    return datetime.time(hour=time.hour,minute=time.minute)

def current_date():
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    return f'{day}/{month}/{year}'

def color_changer(changes_dict):
    light = tinytuya.BulbDevice(os.getenv('LIGHTBULB_DEVICE_ID'),'192.168.0.213',os.getenv('LIGHTBULB_LOCAL_KEY'))
    light.set_version(3.3)
    light.set_socketPersistent(True)
    print('WORKER STARTED')
    while(True):
        sleep(5)
        time = current_time()
        date = current_date()
        if time in changes_dict and changes_dict[time]['date'] != date:
            #only occurs once during the minute for each day
            color = changes_dict[time]['color']
            changes_dict[time]['date'] = date
            light.set_colour(*color)