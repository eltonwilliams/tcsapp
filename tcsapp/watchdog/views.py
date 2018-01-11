# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from .models import Store, NextInvoice, IntegrityCheck, Yealink
import os, glob, re
#import glob



# Create your views here.
def clear_stores(): 
    Store.objects.all().delete()

def clear_invoices(): 
    NextInvoice.objects.all().delete()

def watcher(request):
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
           # Store.objects.all().delete()
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
            

            for code, data in codes.items():
                store = Store.objects.filter(code=code).first()
                #Ninv = NextInvoice.objects.filter(code_id=code).first()
                #print code
                #print data
                

                if not store:
                    store = Store(code=code)

               # if not Ninv:
               #     Ninv = Store(code=code)

                # print "\n\n\n\nbelow >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
                # print "\t\t",data['invoices']
                # print "\nabove >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n\n"

                for i, invoice in enumerate(data['invoices']):      
                    #print invoice        
                    NextInvoice.objects.create(code=code, invoice=invoice) 


                Store.objects.create(code=code, name=data['name'], \
                telephone=data['telephone'] if 'telephone' in data else "No Data", \
                latitude=data['gps'][0] if 'gps' in data else 0.0, \
                longitude=data['gps'][1] if 'gps' in data else 0.0, \
                area_manager=data['area_manager']['name'] if 'area_manager' in data else 'No Data', \
                area_manager_tel=data['area_manager']['telephone'] if 'area_manager' in data else 'No Data', \
                store_manager=data['store_manager']['name'] if 'store_manager' in data else 'No Data', \
                store_manager_tel=data['store_manager']['telephone'] if 'store_manager' in data else 'No Data', \
                trainee_manager=data['trainee_manager']['name'] if 'trainee_manager' in data else 'No Data', \
                trainee_manager_tel=data['trainee_manager']['telephone'] if 'trainee_manager' in data else 'No Data') 

    
               # for invoice in data['invoices']:
                #    store.next_invoice_numbers.append(NextInvoiceNumber(invoice=invoice))

            print "Store Data Imported Successfully"

def testStuff():
    IntegrityCheck.objects.all().delete()
    # var="BQ"
    # rs = NextInvoice.objects.filter(code=var)
    # print "prints list of invoices:"
    # for i in rs:
    #     print i.invoice

    # print "\nprints number of slaves"
    # print len(rs)

    #path = os.path.join(app.config['SALES_PATH'], 'R*.SEQ')
    path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', 'R*.SEQ')
    for sales_file in glob.iglob(path):
        shortname = sales_file.rsplit('\\', 1)[1]
        try:
            #Linux  ->  slave = int(sales.rsplit('/', 1)[1][3])
            slave = int(sales_file.rsplit('\\', 1)[1][3])
            #print slave

            store_code = sales_file.rsplit('\\', 1)[1][1:3]
            #print store_code

            invoiceQS = NextInvoice.objects.filter(code=store_code)
            check = IntegrityCheck.objects.filter(code=store_code)
                        
            

        except:
            continue
        
        # TODO
        #if not store:
            #check = IntegrityCheck(code=store_code, slave=slave, check_code=4, message='NO ENTRY IN CODES FILE {}'.format(sales))
            #db.session.add(check)
        #    continue
    
        if os.stat(sales_file).st_size == 0:
            check.create(code=store_code, slave=slave, check_code=3, message='0KB FILE {}'.format(shortname))
            print shortname, "0KB FILEs"
            #break
            continue
    
        with open(sales_file, 'r') as fd:
            lines = ''.join(fd.readlines()[-2:]).strip()
            #print lines

        if 'Z REPORT NOT RUN' in lines:
            check.create(code=store_code, slave=slave, check_code=5, message=store_code+" - "+shortname)
            print shortname, "- NO Z REPORT RUN"
            continue

        if 'clbackup completed' not in lines:
            check.create(code=store_code, slave=slave, check_code=6, message='MAY BE INCOMPLETE')
            print shortname, "- MAY BE INCOMPLETE"
            continue

        flag = False
        for item in invoiceQS:
            #print item.invoice
            if int(lines.split('\n')[1][27:33]) == 0 and item.invoice + 1 == int(lines.split('\n')[1][81:87]):
                flag = True
                #print flag
                print shortname,"- First Invoice correct - NO SALES DATA"
                break
            elif item.invoice + 1 == int(lines.split('\n')[-1][27:33]):
                flag = True
                #print flag
                print shortname,"- First Invoice correct"
                break

        # TODO: why is x >= needed

        if not flag:
            check.create(code=store_code, slave=slave, check_code=7, message='MISSING SALES {}'.format(shortname))
            print shortname,"- Missing sales"    
            continue

        file = 'SEQCTL{}{}.SEQ'.format(store_code, slave)
        path = os.path.join('C:\\Users\\EWilliams\\Documents\\tcsapp\\tcsapp\\CODES', file)
        if os.path.exists(path):
            with open(path, 'r') as control:
                line = control.readline()
                if int(line[34:40]) != int(lines.split('\n')[-1][81:87]):
                    check.create(code=store_code, slave=slave, check_code=8, message='CONTROL FILE MISMATCH {}'.format(file))
                    
                    continue
        else:
            print shortname,"- Missing control file___" 
            check.create(code=store_code, slave=slave, check_code=9, message='CONTROL FILE MISSING')
            
            continue

        check.create(code=store_code, slave=slave, check_code=0)
        #return render(request, 'blog/post_list.html', {'posts': posts})
        #db.session.add(check)


