#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import time

exclude_list=['nonnecke@berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','alisoncliff@berkeley.edu','hunallen@berkeley.edu']
all_user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).order_by('id')
alluser=User.objects.filter(username='hunallen@gmail.com')

for user in alluser:
    entrycode=EntryCode.objects.filter(username=user.username)
    
    if len(entrycode)>0:
        subject = "Help improve the CS 169.2x course !"
        email_list = [user.username]
        message = render_to_string('registration/mcafe-3rd-regrade.txt',
                                   {'entrycode': entrycode[0].code,
                                   })
        email = EmailMessage(subject, message, Settings.objects.string('DEFAULT_FROM_EMAIL'),email_list, headers = {'Reply-To': 'cafe.mooc@gmail.com'})
    try:
        email.send()

        time.sleep(0.3)
    except:
        pass

