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

        response = self.client.get(reverse('mesh_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p2.title)
        self.assertNotContains(response, self.p3.title)

    def test_what_posts_user_sees(self):
        self.client.login(username='test_user', password='foobar')
        user = self.user

        self.following_public_channel.save()
        self.following_public_channel.followers.add(user)
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.following_private_channel.save()
        self.following_private_channel.followers.add(user)
        self.p6.channel = self.following_private_channel
        self.p6.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        response = self.client.get(reverse('mesh_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.p1.title)
        self.assertContains(response, self.p6.title)
        self.assertContains(response, self.p4.title)
        self.assertNotContains(response, self.p5.title)

    def test_what_posts_anon_sees(self):
        user = self.user

        self.following_public_channel.save()
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.following_private_channel.save()
        self.p6.channel = self.following_private_channel
        self.p6.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        response = self.client.get(reverse('mesh_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p6.title)
        self.assertContains(response, self.p4.title)
        self.assertNotContains(response, self.p5.title)

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
        self.private_author_enroll.save()
        self.private_self_enroll.save()

        response = self.client.get(reverse('mesh_channel_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.not_following_public_channel.title)
        self.assertContains(response, self.following_public_channel.title)

        self.assertNotContains(response, self.not_following_private_channel.title)
        self.assertNotContains(response, self.following_private_channel.title)

        self.assertNotContains(response, self.private_author_enroll.title)
        self.assertNotContains(response, self.private_self_enroll.title)

    def test_what_channel_user_sees(self):
        self.client.login(username='test_user', password='foobar')
        user = self.user


        self.not_following_public_channel.save()
        self.not_following_private_channel.save()
        self.following_public_channel.save()
        self.following_private_channel.save()
        self.private_author_enroll.save()
        self.private_self_enroll.save()

        self.following_public_channel.followers.add(user)
        self.following_private_channel.followers.add(user)

        response = self.client.get(reverse('mesh_channel_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.not_following_public_channel.title)
        self.assertContains(response, self.following_public_channel.title)
        self.assertContains(response, self.following_private_channel.title)
        self.assertContains(response, self.not_following_private_channel.title)

        self.assertNotContains(response, self.private_author_enroll.title)
        self.assertContains(response, self.private_self_enroll.title)


class ChannelDetailViewTestCase(BaseTestCase):

    def test_subscribe_button_shows_up_for_not_logged_in(self):
        user=self.user
        self.c1.save()
        self.c3.save()
        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subscribe to channel button")

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c3.slug}))
        self.assertEqual(response.status_code, 404)

    def test_subscribe_button_shows_up_for_logged_in_user(self):
        user = self.user
        self.client.login(username='test_user', password='foobar')
        self.c1.save()
        self.c3.save()
        self.private_author_enroll.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subscribe to channel button")

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subscribe to channel button")

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.private_author_enroll.slug}))
        self.assertEqual(response.status_code, 404)



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

    def test_available_post_for_logged_in_user(self):
        user = self.user
        self.client.login(username='test_user', password='foobar')

        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)

        self.c3.save()
        self.p1.channel = self.c3
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.p1.title)

        self.c3.followers.add(user)
        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)

        self.private_author_enroll.save()
        self.p1.channel = self.private_author_enroll
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.private_author_enroll.slug}))
        self.assertEqual(response.status_code, 404)

        self.private_author_enroll.followers.add(user)
        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.private_author_enroll.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)


    def test_available_post_for_not_logged_in_user(self):

        user = self.user
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)

        self.c3.save()
        self.p1.channel = self.c3
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.c3.slug}))
        self.assertEqual(response.status_code, 404)


        self.private_author_enroll.save()
        self.p1.channel = self.private_author_enroll
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view', kwargs={'slug':self.private_author_enroll.slug}))
        self.assertEqual(response.status_code, 404)


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

    def test_what_posts_user_sees(self):
        self.client.login(username='test_user', password='foobar')
        user = self.user

        self.following_public_channel.save()
        self.following_public_channel.followers.add(user)
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.following_private_channel.save()
        self.following_private_channel.followers.add(user)
        self.p6.channel = self.following_private_channel
        self.p6.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        response = self.client.get(reverse('mesh_post_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.p1.title)
        self.assertContains(response, self.p6.title)
        self.assertContains(response, self.p4.title)
        self.assertNotContains(response, self.p5.title)

    def test_what_posts_anon_sees(self):
        user = self.user

        self.following_public_channel.save()
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.following_private_channel.save()
        self.p6.channel = self.following_private_channel
        self.p6.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        response = self.client.get(reverse('mesh_post_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.p1.title)
        self.assertNotContains(response, self.p6.title)
        self.assertContains(response, self.p4.title)
        self.assertNotContains(response, self.p5.title)


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

class SelfEnrollmentTestCase(BaseTestCase):

    def test_GET_request_returns_to_channel_index(self):
        user = self.user
        self.client.login(username='test_user', password='foobar')

        self.c1.save()
        response = self.client.get(reverse('mesh_sub',kwargs={'slug': self.c1.slug}))
        self.assertRedirects(response, reverse('mesh_channel_index'), status_code=302)

    def test_Post_request(self):
        user = self.user
        self.client.login(username='test_user', password='foobar')

        self.c3.save()
        self.p1.channel = self.c3
        self.p1.save()

        response = self.client.get(reverse('mesh_channel_view',kwargs={'slug': self.c3.slug}))

        self.assertNotContains(response, self.p1.title)

        self.client.post(reverse('mesh_sub', kwargs={'slug':self.c3.slug}))

        response = self.client.get(reverse('mesh_channel_view',kwargs={'slug': self.c3.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.p1.title)