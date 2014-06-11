#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time

today_date=datetime.datetime.today()-datetime.timedelta(days=1)
user_today=User.objects.filter(date_joined__gte=today_date)


for user in user_today:
    entrycode=EntryCode.objects.filter(username=user.username)
    
    if len(entrycode)>0:
        subject = "Your unique link to the CS169.2x MCAFE"
        email_list = [user.email]
        message = render_to_string('registration/mcafe-confirmation.txt',
                                  {'entrycode': entrycode[0].code,
                                    })
        try:
           #send_mail(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'), email_list)
           
           time.sleep(0.3)
        except:
           pass
