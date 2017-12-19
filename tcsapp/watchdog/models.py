from django.db import models
from django.utils import timezone


class Store(models.Model):
    code = models.CharField(max_length=2 , primary_key=True)
    name = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_manager = models.CharField(max_length=40)
    area_manager_tel = models.CharField(max_length=15)
    store_manager = models.CharField(max_length=40)
    store_manager_tel = models.CharField(max_length=15)
    trainee_manager = models.CharField(max_length=40)
    trainee_manager_tel = models.CharField(max_length=15)

   # user = models.ForeignKey('auth.User')   
   # call_date = models.DateTimeField(blank=True, null=True)  
   # call_comment = models.TextField()
   

    def called(self):
        self.call_date = timezone.now()
        self.save()

    def __str__(self):
        return self.code+' - '+self.name
