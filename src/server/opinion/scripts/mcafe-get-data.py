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

exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list)
user_exclude=User.objects.filter(username__in=exclude_list)

visitors=Visitor.objects.exclude(user__in=user_exclude).order_by(id)

#produce visitor id map to user
useridmap = np.zeros(len(visitors))
for i in range(len(visitors)):
    if visitors[i].user== None:
        useridmap[i]=-1
    else
        useridmap[i]=visitors[i].user.id



#1st time rating baseline issues visitor's grade
statements = OpinionSpaceStatement.objects.all().order_by('id')
baseline_issues=np.zeros((len(visitors),5))
for s in statements:
    for i in range(len(visitors)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors[i].id,log_type=11).exclude(details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                baseline_issues[i,s.id-1]=float(s_log_rating[0].details[-3:])
            else: #not click on skip, not move slider s, => skip
                baseline_issues[i,s.id-1]=-1
        else:
            if len(s_log_rating)==0:  #click skip, not move slider s => skip
                baseline_issues[i,s.id-1]=-1
            else:
                if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                    baseline_issues[i,s.id-1]=-1
                else:
                    baseline_issues[i,s.id-1]=float(s_log_rating[0].details[-3:])


scipy.io.savemat('mcafe_data.mat', dict(useridmap=useridmap, baseline_issues=baseline_issues))


