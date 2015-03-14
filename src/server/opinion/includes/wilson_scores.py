import numpy as np
from opinion.opinion_core.models import *

def wilson_scores():
        disc_stmt = DiscussionStatement.objects.get(is_current=True)
        comments = DiscussionComment.objects.filter(discussion_statement=disc_stmt)

        wilson = []
        for c in comments:
                ca = CommentAgreement.objects.filter(comment=c)
                if ca.count() > 1:
                        ca_vl = ca.values_list('agreement')
                        rating_mean = np.mean(ca_vl)
                        rating_se = 1.96*np.std(ca_vl)/np.sqrt(ca.count())
                        result = (rating_mean - rating_se, ca.count(), c)
                        wilson.append(result)
        wilson.sort(reverse=True)
        return [w[2] for w in wilson]
