from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from threading import Thread
from light_controller.worker import color_changer

def create_change_dict(query_set):
    changes_dict = {} 
    for obj in query_set:
        changes_dict[obj.time] = {
            'color' : [obj.red, obj.green, obj.blue],
            'date' : None
        }
    return changes_dict

class LightControllerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'light_controller'
    changes_dict = None

    def addJob(self,sender,instance,**kwargs):
        self.changes_dict[instance.time] = {
            'color': [instance.red, instance.green, instance.blue],
            'date': None
        }

    def removeJob(self,sender,instance,**kwargs):
        del self.changes_dict[instance.time] 

    def ready(self):
        from light_controller.models import ColorChange
        
        self.ColorChange = ColorChange
        self.changes_dict = create_change_dict(ColorChange.objects.all())
        
        worker = Thread(target=color_changer, args=(self.changes_dict,))
        worker.daemon = True #https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c
        worker.start() #to prevent running two workers, use: py .\manage.py runserver --noreload
        
        post_save.connect(self.addJob, sender=ColorChange)
        post_delete.connect(self.removeJob, sender=ColorChange)
        

        
        
        



        