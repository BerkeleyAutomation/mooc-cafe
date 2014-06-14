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

#1: Africa, 2: Asia, 3: Oceania , 4: Europe, 5: North America, 6: South America
region_dict={"AGO":"1",
"SHN":"1",
"BEN":"1",
"BWA":"1",
"BFA":"1",
"BDI":"1",
"CMR":"1",
"CPV":"1",
"CAF":"1",
"TCD":"1",
"COM":"1",
"COG":"1",
"DJI":"1",
"EGY":"1",
"GNQ":"1",
"ERI":"1",
"ETH":"1",
"GAB":"1",
"GMB":"1",
"GHA":"1",
"GNB":"1",
"GIN":"1",
"CIV":"1",
"KEN":"1",
"LSO":"1",
"LBR":"1",
"LBY":"1",
"MDG":"1",
"MWI":"1",
"MLI":"1",
"MRT":"1",
"MUS":"1",
"MYT":"1",
"MAR":"1",
"MOZ":"1",
"NAM":"1",
"NER":"1",
"NGA":"1",
"STP":"1",
"REU":"1",
"RWA":"1",
"STP":"1",
"SEN":"1",
"SYC":"1",
"SLE":"1",
"SOM":"1",
"ZAF":"1",
"SHN":"1",
"SDN":"1",
"SWZ":"1",
"TZA":"1",
"TGO":"1",
"TUN":"1",
"UGA":"1",
"COD":"1",
"ZMB":"1",
"TZA":"1",
"ZWE":"1",
"SSD":"1",
"COD":"1",
"AFG":"2",
"ARM":"2",
"AZE":"2",
"BHR":"2",
"BGD":"2",
"BTN":"2",
"BRN":"2",
"KHM":"2",
"CHN":"2",
"CXR":"2",
"CCK":"2",
"IOT":"2",
"GEO":"2",
"HKG":"2",
"IND":"2",
"IDN":"2",
"IRN":"2",
"IRQ":"2",
"ISR":"2",
"JPN":"2",
"JOR":"2",
"KAZ":"2",
"PRK":"2",
"KOR":"2",
"KWT":"2",
"KGZ":"2",
"LAO":"2",
"LBN":"2",
"MAC":"2",
"MYS":"2",
"MDV":"2",
"MNG":"2",
"MMR":"2",
"NPL":"2",
"OMN":"2",
"PAK":"2",
"PHL":"2",
"QAT":"2",
"SAU":"2",
"SGP":"2",
"LKA":"2",
"SYR":"2",
"TWN":"2",
"TJK":"2",
"THA":"2",
"TUR":"2",
"TKM":"2",
"ARE":"2",
"UZB":"2",
"VNM":"2",
"YEM":"2",
"PSE":"2",
"ASM":"3",
"AUS":"3",
"NZL":"3",
"COK":"3",
"FJI":"3",
"PYF":"3",
"GUM":"3",
"KIR":"3",
"MNP":"3",
"MHL":"3",
"FSM":"3",
"UMI":"3",
"NRU":"3",
"NCL":"3",
"NZL":"3",
"NIU":"3",
"NFK":"3",
"PLW":"3",
"PNG":"3",
"MNP":"3",
"SLB":"3",
"TKL":"3",
"TON":"3",
"TUV":"3",
"VUT":"3",
"UMI":"3",
"WLF":"3",
"WSM":"3",
"TLS":"3",
"ALB":"4",
"AND":"4",
"AUT":"4",
"BLR":"4",
"BEL":"4",
"BIH":"4",
"BGR":"4",
"HRV":"4",
"CYP":"4",
"CZE":"4",
"DNK":"4",
"EST":"4",
"FRO":"4",
"FIN":"4",
"FRA":"4",
"DEU":"4",
"GIB":"4",
"GRC":"4",
"HUN":"4",
"ISL":"4",
"IRL":"4",
"ITA":"4",
"LVA":"4",
"LIE":"4",
"LTU":"4",
"LUX":"4",
"MKD":"4",
"MLT":"4",
"MDA":"4",
"MCO":"4",
"NLD":"4",
"NOR":"4",
"POL":"4",
"PRT":"4",
"ROU":"4",
"RUS":"4",
"SMR":"4",
"SRB":"4",
"SVK":"4",
"SVN":"4",
"ESP":"4",
"SWE":"4",
"CHE":"4",
"UKR":"4",
"GBR":"4",
"VAT":"4",
"RSB":"4",
"IMN":"4",
"XKX":"4",
"MNE":"4",
"AIA":"5",
"ATG":"5",
"ABW":"5",
"BHS":"5",
"BRB":"5",
"BLZ":"5",
"BMU":"5",
"VGB":"5",
"CAN":"5",
"CYM":"5",
"CRI":"5",
"CUB":"5",
"CUW":"5",
"DMA":"5",
"DOM":"5",
"SLV":"5",
"GRL":"5",
"GRD":"5",
"GLP":"5",
"GTM":"5",
"HTI":"5",
"HND":"5",
"JAM":"5",
"MTQ":"5",
"MEX":"5",
"SPM":"5",
"MSR":"5",
"ANT":"5",
"KNA":"5",
"NIC":"5",
"PAN":"5",
"PRI":"5",
"KNA":"5",
"LCA":"5",
"SPM":"5",
"VCT":"5",
"TTO":"5",
"TCA":"5",
"VIR":"5",
"USA":"5",
"SXM":"5",
"BES":"5",
"BES":"5",
"BES":"5",
"ARG":"6",
"BOL":"6",
"BRA":"6",
"CHL":"6",
"COL":"6",
"ECU":"6",
"FLK":"6",
"GUF":"6",
"GUF":"6",
"GUY":"6",
"PRY":"6",
"PER":"6",
"SUR":"6",
"URY":"6",
"VEN":"6"}

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
for i in range(len(comments)):
    ratings=CommentAgreement.objects.filter(comment=comments[i])
    for rating in ratings:
        if rating.rater.id in userid:
            comment_ratings[userid.index(rating.rater.id),i]=rating.agreement


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

#country map and region map
countrymap = []
regionmap=-1*np.ones(len(user))
for i in range(len(user)):
    country=UserData.objects.filter(user=user[i],key='country')
    if len(country)>0:
        countrymap.append(country[0].value)
        if country[0].value in region_dict:
            regionmap[i]=int(region_dict[country[0].value])
    else:
        countrymap.append('-1')

#gender 1: male 2: female -1: NA
gendermap=-1*np.ones(len(user))
for i in range(len(user)):
    gender=UserData.objects.filter(user=user[i],key='gender')
    if len(gender)>0:
        if gender[0].value=='m':
            gendermap[i]=1
        elif gender[0].value=='f':
            gendermap[i]=2
        else:
            gendermap[i]=-1

#age
agemap=-1*np.ones(len(user))
for i in range(len(user)):
    age=UserData.objects.filter(user=user[i],key='age')
    if len(age)>0:
        if age[0].value != '-1':
            agemap[i]=int(age[0].value)





scipy.io.savemat('mcafe_data.mat', dict(useridmap=useridmap, baseline_issues=baseline_issues,comment_ratings=comment_ratings,participation=participation,userid=userid,countrymap=countrymap,regionmap=regionmap,gendermap=gendermap,agemap=agemap))


