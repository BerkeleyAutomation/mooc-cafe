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
datapath= settings.MEDIA_ROOT + "/mobile/stats_data/"

#calculate grade distribution for each question and output csv for stats page

statements = OpinionSpaceStatement.objects.all().order_by('id')
active_users = User.objects.filter(is_active=True)
bins=[0,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1]

for s in statements:
    s_rating_list=[]
    s_skip=0
    for user in active_users:
        user_s_rating=UserRating.objects.filter(opinion_space_statement=s,user=user).order_by('-created')
        if len(user_s_rating)==1: #only rate 1 time, get visitor info
            visitor=Visitor.objects.filter(user=user_s_rating[0].user)
            if len(visitor)>0:
                s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
                s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
                if len(s_log_skip)==0: #no skip
                    if len(s_log_rating)>0:
                        s_rating_list.append(user_s_rating[0].rating)
                    else: #not click on skip, not move slider s, => skip
                        s_skip=s_skip+1
                else:
                    if len(s_log_rating)==0:  #click skip, not move slider s => skip
                        s_skip=s_skip+1
                    else:
                        if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            s_skip=s_skip+1
                        else:
                            s_rating_list.append(user_s_rating[0].rating)
            else:
                s_rating_list.append(user_s_rating[0].rating)
        if len(user_s_rating)>1: #rate more than 1 time, get user log info
            s_log_skip=LogUserEvents.objects.filter(is_visitor=False, logger_id=user_s_rating[0].user.id,log_type=11,details__contains='skip').filter(details__contains=str(len(user_s_rating))+' visit ').filter(details__contains=str(s.id)).order_by('-created')
            s_log_rating=LogUserEvents.objects.filter(is_visitor=False, logger_id=user_s_rating[0].user.id,log_type=11).exclude(details__contains='skip').filter(details__contains=str(len(user_s_rating))+' visit ').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
            if len(s_log_skip)==0: #no skip
                if len(s_log_rating)>0:
                    s_rating_list.append(user_s_rating[0].rating)
                else: #not click on skip, not move slider s, => skip
                    s_skip=s_skip+1
            else:
                if len(s_log_rating)==0:  #click skip, not move slider s => skip
                    s_skip=s_skip+1
                else:
                    if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                        s_skip=s_skip+1
                    else:
                        s_rating_list.append(user_s_rating[0].rating)

    if len(s_rating_list)>0:
        ofile  = open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"issue"+str(s.id)+"_r.csv", "wb")
        writer=csv.writer(ofile,delimiter=',')
        title=['score','total']
        writer.writerow(title)

        hist,bin_edges = np.histogram(s_rating_list,bins,normed=False)
        value = np.median(s_rating_list)
        skip=np.array([s_skip])
        hist=np.concatenate((hist,skip), axis=1)
        print hist
        for i in range(len(hist)-1):
            row=[i,hist[i]]
            writer.writerow(row)
        writer.writerow(["Skip",hist[len(hist)-1]])

