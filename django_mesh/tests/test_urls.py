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

#Django imports
from django.core.urlresolvers import reverse

#Test imports
from util import BaseTestCase

class IndexTestCase(BaseTestCase):
	def test_empty(self):
		response = self.client.get(reverse('mesh_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_has_only_active_posts(self):
		self.c1.save()
		self.p1.channel = self.c1
#		self.p1.save()
#		self.p1.channel.add(self.c1)
		self.p1.save()
		self.p2.channel = self.c1
#		self.p2.save()
#		self.p2.channel.add(self.c1)
		self.p2.save()
		self.p3.channel = self.c1
#		self.p3.save()
#		self.p3.channel.add(self.c1)
		self.p3.save()
		
		response = self.client.get(reverse('mesh_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertNotContains(response, self.p2.title)
		self.assertNotContains(response, self.p3.title)

class ChannelTestCase(BaseTestCase):
	def test_index_empty(self):
		response = self.client.get(reverse('mesh_channel_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no channels to display.")
	
	def test_index_non_empty(self):
		self.c1.save()
		
		response = self.client.get(reverse('mesh_channel_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.c1.title)
	
	def test_view_empty(self):
		self.c1.save()
		
		response = self.client.get(reverse('mesh_channel_view', args=[self.c1.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_view_has_no_posts_from_other_channels(self):
		self.c1.save()
		
		self.p1.channel = self.c1
#		self.p1.save()
#		self.p1.channel.add(self.c1)
		self.p1.save()
		
		self.c2.save()
		
		self.p2.channel = self.c2
#		self.p2.save()
#		self.p2.channel.add(self.c2)
		self.p2.save()
		
		response = self.client.get(reverse('mesh_channel_view', args=[self.c1.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertNotContains(response, self.p2.title)
	
	def test_view_has_only_active_posts(self):
		self.c1.save()
		self.p1.channel = self.c1
#		self.p1.save()
#		self.p1.channel.add(self.c1)
		self.p1.save()
		self.p2.channel = self.c1
#		self.p2.save()
#		self.p2.channel.add(self.c1)
		self.p2.save()
		self.p3.channel = self.c1
#		self.p3.save()
#		self.p3.channel.add(self.c1)
		self.p3.save()
		
		response = self.client.get(reverse('mesh_channel_view', args=[self.c1.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertNotContains(response, self.p2.title)
		self.assertNotContains(response, self.p3.title)
	

class PostTestCase(BaseTestCase):
	def test_index_empty(self):
		response = self.client.get(reverse('mesh_post_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no posts to display.")
	
	def test_index_has_only_active_posts(self):
		self.c1.save()
		self.p1.channel = self.c1
#		self.p1.save()
#		self.p1.channel.add(self.c1)
		self.p1.save()
		self.p2.channel = self.c1
#		self.p2.save()
#		self.p2.channel.add(self.c1)
		self.p2.save()
		self.p3.channel = self.c1
#		self.p3.save()
#		self.p3.channel.add(self.c1)
		self.p3.save()
		
		response = self.client.get(reverse('mesh_post_index'))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertNotContains(response, self.p2.title)
		self.assertNotContains(response, self.p3.title)
	
	def test_post_view(self):
		self.c1.save()
		self.p1.channel = self.c1 ###############
		self.p1.save()
		self.comment1.content_object = self.p1
		self.comment1.save()
		self.p2.channel = self.c1 #############
		self.p2.published = self.p1.published
		self.p2.save()
		
		response = self.client.get(reverse('mesh_post_view', args=[self.p1.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertContains(response, self.comment1.comment)
		self.assertNotContains(response, self.p2.title)
	
	def test_comments(self):
		self.c1.save()
		self.p1.channel = self.c1 ############
		self.p1.save()
		self.comment1.content_object = self.p1
		self.comment1.save()
		self.p2.channel = self.c1 #############
		self.p2.published = self.p1.published
		self.p2.save()
		
		response = self.client.get(reverse('mesh_post_comments', args=[self.p1.slug]))
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.p1.title)
		self.assertContains(response, self.comment1.comment)
		self.assertNotContains(response, self.p2.title)
	
