#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
try:
    import json
except ImportError:
    import simplejson as json
import numpy as np
from opinion.includes.queryutils import *
import csv
import scipy.io
import datetime

exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).order_by('id')
user=user[11:]

statements = OpinionSpaceStatement.objects.all().order_by('id')

#rating date
rate_2nd_date=datetime.datetime(2014,6,19,7,0,0)
rate_3rd_date=datetime.datetime(2014,6,26,9,0,0)
rate_4th_date=datetime.datetime(2014,7,3,10,0,0)
rate_5th_date=datetime.datetime(2014,7,10,10,0,0)
rate_6th_date=datetime.datetime(2014,7,17,10,0,0)
rate_7th_date=datetime.datetime(2014,7,24,10,0,0)

#4th week grade
baseline_issues_4th=-1*np.ones((len(user),5))
for s in statements:
    for i in range(len(user)):
        if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date: #user join 4th week, get their first rating
            user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('created')
            visitor=Visitor.objects.filter(user=user[i])
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
                    else: #not click on skip, not move slider s, => skip
                        baseline_issues_4th[i,s.id-1]=-1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        baseline_issues_4th[i,s.id-1]=-1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            baseline_issues_4th[i,s.id-1]=-1
                        else:
                            rating=s_log_rating[0].details.split()
                            baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(user_s_rating)>0:
                    baseline_issues_4th[i,s.id-1]=user_s_rating[0].rating
        
        else: #user join before 3rd week, check if they regrade
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).filter(created__gte=rate_4th_date,created__lt=rate_5th_date).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    rating=s_log_rating[0].details.split()
                    baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    baseline_issues_4th[i,s.id-1]=-1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        baseline_issues_4th[i,s.id-1]=-1
                    else:
                        rating=s_log_rating[0].details.split()
                        baseline_issues_4th[i,s.id-1]=float(rating[len(rating)-1])


#appear 4th week
appear_week4=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date:
        appear_week4[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id).filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
        if len(s_log)>0:
            appear_week4[i]=1

#grade 4th week
grade_week4=np.zeros(len(user))
for i in range(len(user)):
    if user[i].date_joined>=rate_4th_date and user[i].date_joined<rate_5th_date:
        grade_week4[i]=1
    else:
        s_log=LogUserEvents.objects.filter(is_visitor=False, logger_id=user[i].id,log_type=11).filter(created__gte=rate_4th_date,created__lt=rate_5th_date)
        if len(s_log)>0:
            grade_week4[i]=1


#number of submit ideas in the 4th week
submit_week4=np.zeros(len(user))
for i in range(len(user)):
    comments=DiscussionComment.objects.filter(user=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date)
    submit_week4[i]=len(comments)

#number of rated ideas in the 4th week
rate_week4=np.zeros(len(user))
for i in range(len(user)):
    ratings=CommentAgreement.objects.filter(rater=user[i],created__gte=rate_4th_date,created__lt=rate_5th_date)
    rate_week4[i]=len(ratings)


scipy.io.savemat('mcafe_data_2.mat',dict(baseline_issues_4th=baseline_issues_4th,appear_week4=appear_week4,grade_week4=grade_week4,rate_week4=rate_week4,submit_week4=submit_week4))