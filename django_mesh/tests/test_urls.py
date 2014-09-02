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

# Django imports
from django.core.urlresolvers import reverse

# Test imports
from .util import BaseTestCase

class IndexViewTestCase(BaseTestCase):
    def test_empty(self):

        response = self.client.get(reverse('mesh_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts to display.")

    def test_has_only_active_posts(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.p2.channel = self.c1
        self.p2.save()
        self.p3.channel = self.c1
        self.p3.save()

        response = self.client.get(reverse('mesh_post_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p2.title)
        self.assertNotContains(response, self.p3.title)

class ChannelIndexViewTestCase(BaseTestCase):
    def test_index_empty(self):
        response = self.client.get(reverse('mesh_channel_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no channels to display.")

    def test_index_non_empty(self):
        self.c1.save()

        response = self.client.get(reverse('mesh_channel_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.c1.title)

    def test_what_channel_anony_sees(self):

        self.not_following_public_channel.save()
        self.not_following_private_channel.save()
        self.following_public_channel.save()
        self.following_private_channel.save()

        response = self.client.get(reverse('mesh_channel_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.not_following_public_channel.title)
        self.assertContains(response, self.following_public_channel.title)

        self.assertNotContains(response, self.not_following_private_channel.title)
        self.assertNotContains(response, self.following_private_channel.title)


    def test_what_user_sees(self):
        self.client.login(username='test_user', password='foobar')
        user = self.user
        user.save()

        self.not_following_public_channel.save()
        self.not_following_private_channel.save()
        self.following_public_channel.save()
        self.following_private_channel.save()

        self.following_public_channel.followers.add(user)
        self.following_private_channel.followers.add(user)

        response = self.client.get(reverse('mesh_channel_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.not_following_public_channel.title)
        self.assertContains(response, self.following_public_channel.title)
        self.assertContains(response, self.following_private_channel.title)
        self.assertNotContains(response, self.not_following_private_channel.title)


class ChannelDetailViewTestCase(BaseTestCase):
    def test_view_empty(self):
        self.c1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug': self.c1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts to display.")

    def test_view_has_no_posts_from_other_channels(self):
        self.c1.save()

        self.p1.channel = self.c1
        self.p1.save()

        self.c2.save()

        self.p2.channel = self.c2
        self.p2.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug': self.c1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p2.title)

    def test_view_has_only_active_posts(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.p2.channel = self.c1
        self.p2.save()
        self.p3.channel = self.c1
        self.p3.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug': self.c1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)

        self.assertNotContains(response, self.p2.title)
        self.assertNotContains(response, self.p3.title)

class PostIndexViewTestCase(BaseTestCase):
    def test_index_empty(self):
        response = self.client.get(reverse('mesh_post_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts to display.")

    def test_index_has_only_active_posts(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.p2.channel = self.c1
        self.p2.save()
        self.p3.channel = self.c1
        self.p3.save()

        response = self.client.get(reverse('mesh_post_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p2.title)
        self.assertNotContains(response, self.p3.title)


class PostDetailViewTestCase(BaseTestCase):
    def test_post_view(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.comment1.content_object = self.p1
        self.comment1.save()
        self.p2.channel = self.c1
        self.p2.published = self.p1.published
        self.p2.save()

        response = self.client.get(reverse('mesh_post_view', kwargs={'slug': self.p1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertContains(response, self.comment1.comment)
        self.assertNotContains(response, self.p2.title)

class PostCommentsViewTestCase(BaseTestCase):
    def test_comments(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.comment1.content_object = self.p1
        self.comment1.save()
        self.p2.channel = self.c1
        self.p2.published = self.p1.published
        self.p2.save()

        response = self.client.get(reverse('mesh_post_comments', kwargs={'slug': self.p1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)
        self.assertContains(response, self.comment1.comment)
        self.assertNotContains(response, self.p2.title)

