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
datapath= settings.MEDIA_ROOT + "/mobile/js/mcafe-ideas-r.json"
from collections import OrderedDict

comments=DiscussionComment.objects.all()
commentratings=np.zeros(len(comments))

for i in range(len(comments)):
    rating_c=CommentAgreement.objects.filter(comment=comments[i])
    ratings=np.array(rating_c.values_list('agreement', flat=True))
#rating formula mean - 1.96*sqrt((var+1/13)/N)
    if len(ratings)==1:
        commentratings[i]=ratings[0]
    if len(ratings)>1:
        commentratings[i]=np.mean(ratings)-1.96*np.sqrt((np.var(ratings,ddof=1)+float(1)/13)/len(ratings))

index=np.argsort(commentratings)
index=index[::-1] # from highest to lowest
data=[]
for i in range(10):
    data.append(OrderedDict([("ranking",str(i+1)),("ideas",comments[index[i]].comment),("date",str(comments[index[i]].created.month)+"/"+str(comments[index[i]].created.day))]))

with open(datapath,'w') as outfile:
    json.dump(data,outfile)

