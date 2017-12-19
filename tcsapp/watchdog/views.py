# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from .models import Store

# Create your views here.


def post_list(request):
    store = Store.objects.all()
    return render(request, 'watcher.html', {'store' : store })

