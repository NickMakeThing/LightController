from rest_framework.views import APIView
from rest_framework.response import Response
import tinytuya
import os
import time 

class ChangeLightbulbColor(APIView):
    light = tinytuya.BulbDevice(os.getenv('LIGHTBULB_DEVICE_ID'),'192.168.0.213',os.getenv('LIGHTBULB_LOCAL_KEY'))
    light.set_version(3.3)
    light.set_socketPersistent(True)
    next_allowed_request = {'time':0} #using a dict so all instances share changes to this attribute

    def post(self, request, format=None):
        current_time = time.time()
        if(current_time > self.next_allowed_request['time']):
            print(request.data['color'])
            self.light.set_colour(*request.data['color'])
            self.light.set_brightness(request.data['brightness']*10)
            self.next_allowed_request['time'] = time.time()+1
            #color can only change color every 1 seconds 
        return Response(200)

