from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from .serializers import CreateChangeSerializer, GetChangesSerializer, DeleteChangeSerializer
from light_controller.models import ColorChange
import datetime # for saving/creating time of day data
import time # for ratelimit
import tinytuya
import os

class GetChanges(ListAPIView):
    queryset = ColorChange.objects.all() 
    serializer_class = GetChangesSerializer

class DeleteChange(DestroyAPIView):
    queryset = ColorChange.objects.all()
    serializer_class = DeleteChangeSerializer
    lookup_field = 'id'

def parse_time(time):
    time = time.split(':')
    return datetime.time(int(time[0]),int(time[1]))

class ChangeColorLater(CreateAPIView):
    queryset = ColorChange.objects.all() #do i need this line?
    serializer_class = CreateChangeSerializer
    #need to update worker on post
    def post(self, request, *args, **kwargs):
        print(parse_time(request.data['time']))
        request.data['time'] = parse_time(request.data['time'])
        return self.create(request, *args, **kwargs)

class ChangeColorNow(APIView):
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

