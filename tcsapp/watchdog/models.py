from django.db import models
from django.utils import timezone


class Store(models.Model):
    code = models.CharField(max_length=2 , primary_key=True)
    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_manager = models.TextField()
    area_manager_tel = models.TextField()
    store_manager = models.TextField()
    store_manager_tel = models.TextField()
    trainee_manager = models.TextField()
    trainee_manager_tel = models.TextField()

    user = models.ForeignKey('auth.User')   
    call_date = models.DateTimeField(blank=True, null=True)  
    call_comment = models.TextField()
   

    def called(self):
        self.call_date = timezone.now()
        self.save()

    def __str__(self):
        return self.code
