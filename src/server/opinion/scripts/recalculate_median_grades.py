#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

active_users = list(User.objects.filter(is_active=True))
skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
statements = OpinionSpaceStatement.objects.all().order_by('id')

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

    cache = StatementMedians.objects.filter(statement = s)
    value = np.median(s_rating_list)
    if cache.count() == 0:
        StatementMedians(statement = s, rating = value).save()
    else:
	cache.update(rating = value)

    print s.id, value, len(s_rating_list)
