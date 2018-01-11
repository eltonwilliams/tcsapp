# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Store, NextInvoice, IntegrityCheck, Yealink

admin.site.register(Yealink)
admin.site.register(Store)
admin.site.register(NextInvoice)
admin.site.register(IntegrityCheck)

# Register your models here.
