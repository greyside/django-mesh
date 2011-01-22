# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from ..models import *
from django.core.cache import cache

class BaseTestCase(TestCase):
	def setUp(self):
		self.username = 'test_user'
		self.password = 'foobar'
		self.user = User.objects.create_user(self.username, 'test_user@example.com', self.password)
		self.c1 = Channel(
			slug='public',
			name='Public',
			site=Site.objects.get_current()
		)
		self.c2 = Channel(
			slug='another-channel',
			name='Another Channel',
			site=Site.objects.get_current()
		)
		self.p1 = Post(
			author=self.user,
			slug='unit-testing-unit-tests',
			title='Are you unit testing your unit tests? Learn all about the latest best practice: TDTDD',
			text='Lorem Ipsum etc.',
			status=Post.PUBLISHED_STATUS
		)
		self.p2 = Post(
			author=self.user,
			slug='tree-falls-forest',
			title='Tree Falls in Forest, No One Notices',
			published=datetime.now()+timedelta(days=1),
			status=Post.PUBLISHED_STATUS
		)
		self.p3 = Post(
			author=self.user,
			slug='tree-falls-forest-again',
			title='Tree Falls in Forest, Could There be a Tree Flu Epidemic?',
			status=Post.DRAFT_STATUS
		)
		self.i1 = Item(
			text='A Really Awesome Site',
			url='example.com',
			title='Example.com Homepage',
		)
		self.i2 = Item(
			text='Another Really Awesome Site',
			url='test.com',
			title='Test.com Homepage',
		)
		self.comment1 = Comment(
			site=Site.objects.get_current(),
			user=self.user,
			comment='Thanks for sharing.',
		
		)
	
	def tearDown(self):
		#FIXME: dqc doesn't intercept db destruction or rollback
		cache.clear()
