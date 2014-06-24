#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
import simplejson as json


import numpy as np
from opinion.includes.queryutils import *
import csv
datapath= settings.MEDIA_ROOT + "/mobile/js/mcafe-ideas-r.json"
testpath= settings.MEDIA_ROOT + "/mobile/js/mcafe-ideas-detail.csv"
comments=DiscussionComment.objects.all()
commentratings=np.zeros(len(comments))

for i in range(len(comments)):
    rating_c=CommentAgreement.objects.filter(comment=comments[i])
    ratings=np.array(rating_c.values_list('agreement', flat=True))
#rating formula mean - 1.96*sqrt((var+1/13)/N)
    if len(ratings)==1:
        commentratings[i]=ratings[0]
    if len(ratings)>1:
        sum=0
        for j in range(len(ratings)):
            sum=sum+(ratings[j]-np.mean(ratings))*(ratings[j]-np.mean(ratings))
        var=float(sum)/(len(ratings)-1)
        commentratings[i]=np.mean(ratings)-1.96*np.sqrt((var+float(1)/13)/len(ratings))

index=np.argsort(commentratings)
commentratings=np.sort(commentratings)
commentratings=commentratings[::-1]
index=index[::-1] # from highest to lowest
data=[]
for i in range(10):
    data.append({"ranking":str(i+1),"ideas":comments[index[i]].comment,"date":str(comments[index[i]].created.month)+"/"+str(comments[index[i]].created.day)})

outfile = open(datapath, "w")
json.dump(data,outfile)
outfile.close()

ofile  = open(testpath, "wb")
writer=csv.writer(ofile,delimiter=',')
title=['Rank','Comment','Number of rating','Score','Date']
writer.writerow(title)
for i in range(len(comments)):
    rating_c=CommentAgreement.objects.filter(comment=comments[index[i]])
    writer.writerow([str(i),comments[index[i]].comment,str(len(rating_c)),str(commentratings[i]),str(comments[index[i]].created.month)+"/"+str(comments[index[i]].created.day)])

