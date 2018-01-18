# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from django.db import transaction

from .models import Store, NextInvoice, IntegrityCheck, Yealink

import os, glob, re
from datetime import datetime 


def update(): 
    print "got to the update"



# Create your views here.
def clear_stores(): 
    Store.objects.all().delete()
    print "Cleared Stores Info"

def clear_invoices(): 
    NextInvoice.objects.all().delete()
    print "Cleared Invoices"

def clear_checks(): 
    IntegrityCheck.objects.all().delete()
    print "Cleared checks"

def dashboard(request):

    overall_slaves = NextInvoice.objects.all().count()
    current_slaves = IntegrityCheck.objects.filter(check_code = 0).count()
    outstanding_slaves = overall_slaves - current_slaves

    overall_stores = Store.objects.all().count()
    current_stores = 0
    outstanding_stores = 0

    progress = int(float(current_slaves) / overall_slaves * 100)

     #check status of Store's slaves for any fails
    for store in Store.objects.all():
        store_status = IntegrityCheck.objects.filter(slave__startswith = store.code)
        if store_status:
            result = not any(check for check in store_status if check.check_code != 0)
        else:
            result = False
        if result:
            current_stores+=1
        else:
            outstanding_stores+=1

        

    return render(request, 'dashboard.html',{'progress' : progress , 'current_slaves': current_slaves, 'overall_slaves': overall_slaves, 'outstanding_slaves': outstanding_slaves, 'current_stores': current_stores, 'outstanding_stores': outstanding_stores })

def watcher(request):
    print request
    zreport = IntegrityCheck.objects.filter(check_code = 5)
    check2 = IntegrityCheck.objects.all()
    return render(request, 'watcher.html', {'zreport' : zreport, 'check' : check2 })

def info(request):
    ip_phone = Yealink.objects.get(user__username='wgoosen')

    return render(request, 'info.html',{'out': ip_phone.ext })

def table_info(request):
    store_info = Store.objects.all()
    info = serializers.serialize('json', store_info)
    return HttpResponse(info, content_type='application/json')

def yealink(request):
    #ip_phone = Yealink.objects.filter(user='wgoosen')
    ip_phone = Yealink.objects.get(user__username='wgoosen')
    dail = '5834'
    uri = "http://admin:Connexion1@sip-t23g-{}/cgi-bin/ConfigManApp.com?number={}&outgoing_uri={}@192.168.20.156".format( ip_phone.ext, dail, ip_phone.ext )
    return render(request, 'base.html', {'uri' : uri })

def refresh_codes():   
            start = datetime.now() 

            lines = []
            path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'CLLOI*')
            filename = max(glob.glob(path), key=lambda x: os.stat(x).st_mtime)

            print "Using path>>"+filename

            with open(filename, 'r') as codes:
                for line in codes:
                    if 'LOCATION' not in line and 'RUN DATE' not in line and 'O F F L I N E' not in line and 'UNKNOWN' not in line and 'RECORDS' not in line and line.isspace()==False:
                        lines.append(line)

            codes = {}
            invoices = []
            key = " "
            name = " "

            for line in lines:
                if line[3:5].strip():
                    invoices = []
                    key = line[3:5]
                    name = line[10:27].strip()
                    invoices.append(int(line[27:33].strip()))
                else:
                    invoices.append(int(line.strip()))

                codes[key] = {'name': name, 'invoices': invoices}
                
            

            lines = []

            with open(os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'OPOPP001.SPL'), 'r') as details:
                for line in details:
                    if 'LOCATION' not in line and 'RUN DATE' not in line and 'O P S' not in line and line.isspace()==False:
                        lines.append(line)

            key = " "

            for line in lines:
                if line[:2] != "  ":
                    key = line[:2].strip()
                elif key not in codes:
                    continue
                elif 'Sunday   ' in line:
                    num = re.sub(r'\+27 ', "0", line[84:].strip())
                    # Remove anything other than digits
                    formated = re.sub(r'\D', "", num)  
                    codes[key]['telephone'] = formated
                elif 'GPS ' in line:
                    codes[key]['gps'] = (float(line[28:44].strip()), float(line[44:].strip()))
                elif line[24:26] == 'AM':
                    AM_num = re.sub(r'\+27 ', "0", line[68:].strip())
                    # Remove anything other than digits
                    AM_formated = re.sub(r'\D', "", AM_num)
                    codes[key]['area_manager'] = {
                        'name': line[31:62].strip(),
                        'telephone': AM_formated,
                    }
                elif line[24:26] == 'SM':
                    SM_num = re.sub(r'\+27 ', "0", line[68:].strip())
                    # Remove anything other than digits
                    SM_formated = re.sub(r'\D', "", SM_num)
                    codes[key]['store_manager'] = {
                        'name': line[31:62].strip(),
                        'telephone': SM_formated,
                    }
                elif line[24:26] == 'TM':
                    TM_num = re.sub(r'\+27 ', "0", line[68:].strip())
                    # Remove anything other than digits
                    TM_formated = re.sub(r'\D', "", TM_num)
                    codes[key]['trainee_manager'] = {
                        'name': line[31:62].strip(),
                        'telephone': TM_formated,
                    }
            
            with transaction.atomic():
                for code, data in codes.items():
                    DBStore = Store(code=code, name=data['name'], \
                    telephone=data['telephone'] if 'telephone' in data else "No Data", \
                    latitude=data['gps'][0] if 'gps' in data else 0.0, \
                    longitude=data['gps'][1] if 'gps' in data else 0.0, \
                    area_manager=data['area_manager']['name'] if 'area_manager' in data else 'No Data', \
                    area_manager_tel=data['area_manager']['telephone'] if 'area_manager' in data else 'No Data', \
                    store_manager=data['store_manager']['name'] if 'store_manager' in data else 'No Data', \
                    store_manager_tel=data['store_manager']['telephone'] if 'store_manager' in data else 'No Data', \
                    trainee_manager=data['trainee_manager']['name'] if 'trainee_manager' in data else 'No Data', \
                    trainee_manager_tel=data['trainee_manager']['telephone'] if 'trainee_manager' in data else 'No Data')
                    DBStore.save()
                
                # if not store:
                #     store = Store(code=code)

                    for i, invoice in enumerate(data['invoices']):       
                        DBInvoice = NextInvoice(code=code, invoice=invoice)
                        DBInvoice.save()
            

            time_elapsed = datetime.now() - start
            print 'Refreshing Store info run time: {}'.format(time_elapsed)
            print "Store Data Imported Successfully"


def testStuff():
    start = datetime.now()

    with transaction.atomic():
        with open('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES\\storelist', 'r') as stores:
            for store in stores:
                store = store.strip('#').strip()
                QS = NextInvoice.objects.filter(code=store)

                if not store:
                    continue

                path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'R{}*'.format(store))
                for file in glob.iglob(path):
                    slave = int(file.rsplit('\\', 1)[1][3])
                    shortname = file.rsplit('\\', 1)[1]
                    if slave > len(QS):
                        DBcheck = IntegrityCheck(slave=store+str(slave), check_code=1, message='NOT IN CODES FILE {}'.format(shortname))
                        DBcheck.save()
                        break
                        #continue

                # check if sales file exist for that slave
                for slave in range(1, len(QS) + 1):
                    path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'R{}{}*'.format(store, slave))
                    if not glob.glob(path):
                        DBcheck = IntegrityCheck(slave=store+str(slave), check_code=2, message='NOT FOUND')
                        DBcheck.save()
                        continue

    
    
    #check for integrity                    
        path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'R*.SEQ')
    #with transaction.atomic():
        for sales_file in glob.iglob(path):
            shortname = sales_file.rsplit('\\', 1)[1]
            try:
                #Linux  ->  slave = int(sales.rsplit('/', 1)[1][3])
                slave = int(sales_file.rsplit('\\', 1)[1][3])
                store_code = sales_file.rsplit('\\', 1)[1][1:3]
                comb = store_code+str(slave)

                invoiceQS = NextInvoice.objects.filter(code=store_code)
                        
            

            except Exception as e:
                print e
                continue
        
            # TODO
            #if not store:
                #check = IntegrityCheck(code=store_code, slave=slave, check_code=4, message='NO ENTRY IN CODES FILE {}'.format(sales))
                #db.session.add(check)
            #    continue
    
            if os.stat(sales_file).st_size == 0:
                DBcheck = IntegrityCheck(slave=comb, check_code=3, message='0KB FILE {}'.format(shortname))
                DBcheck.save()
                continue
    
            with open(sales_file, 'r') as fd:
                lines = ''.join(fd.readlines()[-2:]).strip()

            if 'Z REPORT NOT RUN' in lines:
                DBcheck = IntegrityCheck(slave=comb, check_code=5, message=shortname)
                DBcheck.save()
                continue

            if 'clbackup completed' not in lines:
                DBcheck = IntegrityCheck(slave=comb, check_code=6, message='MAY BE INCOMPLETE {}'.format(shortname))
                DBcheck.save()
                continue

            flag = False
            for item in invoiceQS:
                if int(lines.split('\n')[1][27:33]) == 0 and item.invoice + 1 == int(lines.split('\n')[1][81:87]):
                    flag = True
                    break
                elif item.invoice + 1 == int(lines.split('\n')[-1][27:33]):
                    flag = True
                    break

            # TODO: why is x >= needed

            if not flag:
                DBcheck = IntegrityCheck(slave=comb, check_code=7, message='MISSING SALES {}'.format(shortname))
                DBcheck.save()
                continue

            file = 'SEQCTL{}{}.SEQ'.format(store_code, slave)
            path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', file)
            if os.path.exists(path):
                with open(path, 'r') as control:
                    line = control.readline()
                    if int(line[34:40]) != int(lines.split('\n')[-1][81:87]):
                        DBcheck = IntegrityCheck(slave=comb, check_code=8, message='CONTROL FILE MISMATCH {}'.format(file))
                        DBcheck.save()
                        continue
            else:
                DBcheck = IntegrityCheck(slave=comb, check_code=9, message='CONTROL FILE MISSING {}'.format(file))
                DBcheck.save()
            
                continue

            DBcheck = IntegrityCheck(slave=comb, check_code=0, message='ALL CHECKS OK')
            DBcheck.save()

            # for store in Store.objects.all():
            #     store_status = IntegrityCheck.objects.filter(slave__startswith = store.code)
            #     if store_status:
            #         result = not any(check for check in store_status if check.check_code != 0)
            #     else:
            #         result = False
            #     DBstore = Store(code=store_code, status=result)
            #     DBstore.save()



    time_elapsed = datetime.now() - start
    print 'File checking run time: {}'.format(time_elapsed)

