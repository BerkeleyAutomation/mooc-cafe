#!/usr/bin/env python
import sys
import environ
import numpy
import datetime
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from math import *


def main():
	if len(sys.argv) < 2:
		print "Usage: python recalculate_discussion_weights.py os_id [disc_stmt_id]"
		sys.exit()
	
	os_id = sys.argv[1]
	if len(sys.argv) < 3:
		filter_ds = DiscussionStatement.objects.filter(opinion_space = os_id, is_current = True)[:1]
		disc_stmt = filter_ds[0].id
	else:
		disc_stmt = sys.argv[2]

	print "Calculating weights for os_id = " + os_id + " and disc_stmt = " + str(disc_stmt)

	comments = DiscussionComment.objects.filter(opinion_space = os_id, discussion_statement = disc_stmt)

	# If we're using comments to position users
	if Settings.objects.boolean('NO_STATEMENTS'):

		# remove the comments of users whose ids match the statement ids
		os = get_os(os_id)
		statement_ids = os.statements.values_list('id')
		comments = comments.exclude(user__in = statement_ids)

	comments = list(comments) #evaluate once
	max_weight = 0
	comment_id_to_num_ratings_map = {}
	for comment in comments:
		agreement = [r[1] for r in get_recent_ratings_from_all_revisions(comment,'agreement',-1)]
		insight = [r[1] for r in get_recent_ratings_from_all_revisions(comment,'insight', -1)]
		num_ratings = len(union_sort_agreement_and_insight(agreement, insight))
		comment_id_to_num_ratings_map[comment.id] = num_ratings
		if num_ratings > max_weight:
			max_weight = num_ratings

	for comment in comments:
		
		#this is the decay rate
		k = 6

		#this is the time lag
		t = 6

		#this is todays date
		current_time = datetime.datetime.now()

		#this is the difference in days
		difference = (current_time - comment.created).days + 0.0
		if difference < t:
			difference = 0

		print comment.i, difference, "Original Weight: ", comment.query_weight, "Final Weight: ", comment.query_weight*numpy.exp(-difference/k)

		comment.query_weight = comment.query_weight*numpy.exp(-difference/k)
		comment.save()

	print "Done."
main()