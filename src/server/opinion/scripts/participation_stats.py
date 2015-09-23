import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
import numpy as np
import datetime
import matplotlib.pyplot as plt
import prettyplotlib as ppl

def participation():
	user_set = User.objects.filter(is_active=True)

	num_weeks, start_date = calculate_week(user_set)

	# Weekly comment data
	comment_data = [DiscussionComment.objects.filter(user__in=user_set, \
			created__lt=(start_date+datetime.timedelta(days=7))).count()]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		comment_count = DiscussionComment.objects.filter(user__in=user_set, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count()
		comment_data.append(comment_count)
		lower_bound += 7
		upper_bound += 7


	# Weekly QAT rating data
	rating_data = [UserRating.objects.filter(user__in=user_set, \
			created__lt=(start_date+datetime.timedelta(days=7))).count()]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		rating_count = UserRating.objects.filter(user__in=user_set, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count()
		rating_data.append(rating_count)
		lower_bound += 7
		upper_bound += 7

	# Weekly login data
	login_data = [LogUserEvents.objects.filter(log_type=0, \
			created__lt=(start_date+datetime.timedelta(days=7))).count()]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		login_count = LogUserEvents.objects.filter(log_type=0, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count()
		login_data.append(rating_count)
		lower_bound += 7
		upper_bound += 7

	fig, ax = plt.subplots()
	ax.set_xlabel('Week')
	ax.set_ylabel('Weekly Participation')
	ax.set_title('Weekly User Participation')
	x = range(1, num_weeks+1)
	ppl.plot(ax, x, login_data, label='# Participants', linewidth=1.5)
	ppl.plot(ax, x, rating_data, label='# QAT ratings', linewidth=1.5)
	ppl.plot(ax, x, comment_data, label='# suggestions', linewidth=1.5)
	ppl.legend(ax, loc='lower right')
	plt.show()

	fig.savefig('../../client/media/images/participation.png')


participation()