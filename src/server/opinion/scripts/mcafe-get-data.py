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
user=User.objects.exclude(username__in=exclude_list).order_by('id')
userid=[]
for u in user:
    userid.append(u.id)

user_exclude=User.objects.filter(username__in=exclude_list)

visitors=Visitor.objects.exclude(user__in=user_exclude).order_by('id')

#produce visitor id map to user
useridmap = np.zeros(len(visitors))
for i in range(len(visitors)):
    if visitors[i].user== None:
        useridmap[i]=-1
    else:
        useridmap[i]=visitors[i].user.id



#1st time rating baseline issues visitor's grade
statements = OpinionSpaceStatement.objects.all().order_by('id')
baseline_issues=np.zeros((len(visitors),5))
for s in statements:
    for i in range(len(visitors)):
        s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors[i].id,log_type=11,details__contains='skip').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
        s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitors[i].id,log_type=11).exclude(details__contains='skip').exclude(details__contains='grade').filter(details__contains='slider_set '+str(s.id)).order_by('-created')
        if len(s_log_skip)==0: #no skip
            if len(s_log_rating)>0:
                if s_log_rating[0].details[-2]==' ':
                    baseline_issues[i,s.id-1]=float(s_log_rating[0].details[-1:])
                else:
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
                    if s_log_rating[0].details[-2]==' ':
                        baseline_issues[i,s.id-1]=float(s_log_rating[0].details[-1:])
                    else:
                        baseline_issues[i,s.id-1]=float(s_log_rating[0].details[-3:])

#produce comment rating
comments=DiscussionComment.objects.all().order_by('id')
comment_ratings=-1*np.ones((len(user),len(comments)))
for comment in comments:
    ratings=CommentAgreement.objects.filter(comment=comment)
    for rating in ratings:
        if rating.rater.id in userid:
            comment_ratings[userid.index(rating.rater.id),rating.agreement]


#participation level
#   1 : 'visited the site, pressed "Begin"',
#	2 : 'submitted grades',
#	3 : 'registration',
#	4 : 'rated at least 2 other participant\'s ideas',
#	5 : 'submitted a valid idea',
#	6 : 'returns using unique URL',

participation=np.zeros((len(visitors),6))
for i in range(len(visitors)):
    participation[i,0]=1
    level2=LogUserEvents.objects.filter(details='sliders finished',log_type=5, logger_id=visitors[i].id,is_visitor=True)
    if len(level2)>0:
        participation[i,1]=1
    if visitors[i].user != None:
        participation[i,2]=1
        if CommentAgreement.objects.filter(rater = visitors[i].user).count() >= 2:
            participation[i,3]=1
        if DiscussionComment.objects.filter(user = visitors[i].user).count()>0:
            participation[i,4]=1



scipy.io.savemat('mcafe_data.mat', dict(useridmap=useridmap, baseline_issues=baseline_issues,comment_ratings=comment_ratings,participation=participation))


