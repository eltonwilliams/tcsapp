from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Yealink(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ext = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return "YEALINK ClickToDail - "+str(self.user).upper()+' - '+self.ext
    

class Store(models.Model):
    code = models.CharField(max_length=2 , primary_key=True, default='##')
    name = models.CharField(max_length=20, default='NONE')
    telephone = models.CharField(max_length=15, default='NONE')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    area_manager = models.CharField(max_length=40, default='NONE')
    area_manager_tel = models.CharField(max_length=15, default='NONE')
    store_manager = models.CharField(max_length=40, default='NONE')
    store_manager_tel = models.CharField(max_length=15, default='NONE')
    trainee_manager = models.CharField(max_length=40, default='NONE')
    trainee_manager_tel = models.CharField(max_length=15, default='NONE')
    status = models.BooleanField(default=True)
    called = models.BooleanField(default=False)
    #invoices = models.OneToManyField(NextInvoice)
    

   # user = models.ForeignKey('auth.User')   
   # call_date = models.DateTimeField(blank=True, null=True)  
   # call_comment = models.TextField()
   

    # def called(self):
    #     self.call_date = timezone.now()
    #     self.save()

    def __str__(self):
        return self.code+' - '+self.name

class NextInvoice(models.Model):
    #code = models.ForeignKey(Store)
    code = models.CharField(max_length=2, default='##', unique=False,null=True)
    invoice = models.IntegerField(default=0, unique=False,null=True)

    def __str__(self):
        return self.code+" : "+str(self.invoice)

    #def checkInvoice(invoice):


class IntegrityCheck(models.Model):
    #code = models.CharField(max_length=2, default='##', unique=False,null=True)
    #slave = models.IntegerField(default=0, unique=False,null=True)
    slave = models.CharField(max_length=3, default='###', primary_key=True)
    #check_id = models.IntegerField(primary_key=True)
    check_code = models.IntegerField(default=0, unique=False,null=True)
    message = models.CharField(max_length=20, default='NONE')

    def __str__(self):
        #return self.slave
        return self.slave[:2]+" - SLAVE "+self.slave[2]+" - (Error code: "+str(self.check_code)+") - "+self.message
