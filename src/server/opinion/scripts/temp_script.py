#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *

for c in DiscussionComment.objects.filter(comment__icontains='social media'):
	c.comment = ''
	c.save()

