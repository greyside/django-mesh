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

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ..models import *
from ..views import *
from django.core.cache import cache
import pdb
from django.contrib.sites.models import Site

class IndexTestCase(TestCase):
	def setUp(self):
		username = 'test_user'
		password = 'foobar'
		self.user = User.objects.create_user(username, 'test_user@example.com', password)
	
	def test_empty(self):
		response = self.client.get(reverse('mesh_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_non_empty(self):
		c = Channel(
			slug='public',
			name='Public',
			site=Site.objects.get_current()
		)
		c.save()
		p = Post(
			author=self.user,
			slug='tree-falls-forest',
			title='Tree Falls in Forest, No One Notices'
		)
		p.save()
		p.channels.add(c)
		p.save()
		
		response = self.client.get(reverse('mesh_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, p.title)
	
	def tearDown(self):
		#FIXME: dqc doesn't intercept db destruction or rollback
		cache.clear()

class ChannelTestCase(TestCase):
	def setUp(self):
		username = 'test_user'
		password = 'foobar'
		self.user = User.objects.create_user(username, 'test_user@example.com', password)
		self.c = Channel(
			slug='public',
			name='Public',
			site=Site.objects.get_current()
		)
	
	def test_index_empty(self):
		response = self.client.get(reverse('mesh_channel_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no channels to display.")
	
	def test_index_non_empty(self):
		self.c.save()
		
		response = self.client.get(reverse('mesh_channel_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.c.name)
	
	def test_view_empty(self):
		self.c.save()
		
		response = self.client.get(reverse('mesh_channel_view', args=[self.c.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_view_non_empty(self):
		self.c.save()
		p = Post(
			author=self.user,
			slug='tree-falls-forest',
			title='Tree Falls in Forest, No One Notices'
		)
		p.save()
		p.channels.add(self.c)
		p.save()
		c2 = Channel(
			slug='another-channel',
			name='Another Channel',
			site=Site.objects.get_current()
		)
		c2.save()
		p2 = Post(
			author=self.user,
			slug='tree-falls-forest-again',
			title='Tree Falls in Forest, Could There be a Tree Flu Epidemic?'
		)
		p2.save()
		p2.channels.add(c2)
		p2.save()
		
		response = self.client.get(reverse('mesh_channel_view', args=[self.c.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, p.title)
		self.assertNotContains(response, p2.title)
	
	def tearDown(self):
		#FIXME: dqc doesn't intercept db destruction or rollback
		cache.clear()

class PostTestCase(TestCase):
	def setUp(self):
		username = 'test_user'
		password = 'foobar'
		self.user = User.objects.create_user(username, 'test_user@example.com', password)
		self.c = Channel(
			slug='public',
			name='Public',
			site=Site.objects.get_current()
		)
		self.p = Post(
			author=self.user,
			slug='unit-testing-unit-tests',
			title='Are you unit testing your unit tests? Learn all about the latest best practice: TDTDD'
		)
	
	def test_index_empty(self):
		response = self.client.get(reverse('mesh_post_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_index_non_empty(self):
		self.c.save()
		self.p.save()
		
		response = self.client.get(reverse('mesh_post_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p.title)
	
	def test_view(self):
		self.c.save()
		self.p.save()
		
		response = self.client.get(reverse('mesh_post_view', args=[self.p.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p.title)
	
	def tearDown(self):
		#FIXME: dqc doesn't intercept db destruction or rollback
		cache.clear()
	
