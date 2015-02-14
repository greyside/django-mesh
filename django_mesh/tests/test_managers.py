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

# App imports
from ..models import Post, Channel, Tag

# Test imports
from .util import BaseTestCase

from django.contrib.auth import get_user_model

class PostQuerySetTestCase(BaseTestCase):
    def test_active(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.p7.channel = self.c1
        self.p7.save()
        self.p3.channel = self.c1
        self.p3.save()

        active_posts = Post.objects.active()

        self.assertIn(self.p1, active_posts)
        self.assertNotIn(self.p7, active_posts)
        self.assertNotIn(self.p3, active_posts)

    def test_get_for_user(self):
        user = self.user

        self.following_public_channel.save()
        self.following_public_channel.followers.add(user)
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.following_private_channel.save()
        self.following_private_channel.followers.add(user)
        self.p2.channel = self.following_private_channel
        self.p2.save()

        self.p7.channel = self.following_private_channel
        self.p7.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5.channel = self.not_following_private_channel
        self.p5.save()

        viewable = Post.objects.get_for_user(user)

        self.assertIn(self.p1, viewable)
        self.assertIn(self.p2, viewable)
        self.assertIn(self.p4, viewable)

        self.assertNotIn(self.p7, viewable)

        self.assertNotIn(self.p5, viewable)

    def test_get_for_user_not_following_channel(self):
        user = self.user

        self.following_public_channel.save()
        self.p1.channel = self.following_public_channel
        self.p1.save()
        self.p7.channel = self.following_public_channel
        self.p7.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.following_private_channel.save()
        self.p2.channel = self.following_private_channel
        self.p2.save()

        self.not_following_private_channel.save()
        self.p5.channel = self.not_following_private_channel
        self.p5.save()

        viewable = Post.objects.get_for_user(user)

        self.assertIn(self.p1, viewable)
        self.assertIn(self.p4, viewable)

        self.assertNotIn(self.p7, viewable)
        self.assertNotIn(self.p2, viewable)
        self.assertNotIn(self.p5, viewable)

    def test_get_for_user_anonymous(self):
        user = self.user
        user.id == None

        self.following_public_channel.save()
        self.p1.channel = self.following_public_channel
        self.p1.save()
        self.p7.channel = self.following_public_channel
        self.p7.save()

        self.not_following_private_channel.save()
        self.p5.channel = self.not_following_private_channel
        self.p5.save()

        viewable = Post.objects.get_for_user(user)

        self.assertIn(self.p1, viewable)
        self.assertNotIn(self.p7, viewable)
        self.assertNotIn(self.p5, viewable)

class ChannelQuerySetTestCase(BaseTestCase):
    def test_get_for_user(self):
        user = self.user

        self.following_public_channel.save()
        self.following_public_channel.followers.add(user)
        
        self.following_private_channel.save()
        self.following_private_channel.followers.add(user)

        self.not_following_public_channel.save()
        self.not_following_private_channel.save()

        self.private_self_enroll.save()
        self.private_author_enroll.save()

        viewable = Channel.objects.get_for_user(user)

        self.assertIn(self.following_public_channel, viewable)
        self.assertIn(self.following_private_channel, viewable)
        self.assertIn(self.not_following_public_channel, viewable)
        self.assertIn(self.not_following_private_channel, viewable)
        self.assertIn(self.private_self_enroll, viewable)

        self.assertNotIn(self.private_author_enroll, viewable)

    def test_get_for_user_anonymous(self):
        user = self.user
        user.id = None

        self.following_public_channel.save()
        self.following_private_channel.save()
        self.not_following_public_channel.save()
        self.not_following_private_channel.save()

        self.private_author_enroll.save()
        self.private_self_enroll.save()

        viewable = Channel.objects.get_for_user(user)

        self.assertIn(self.following_public_channel, viewable)
        self.assertIn(self.not_following_public_channel, viewable)

        self.assertNotIn(self.following_private_channel, viewable)
        self.assertNotIn(self.not_following_private_channel, viewable)
        self.assertNotIn(self.private_self_enroll, viewable)
        self.assertNotIn(self.private_author_enroll, viewable)

class TagQuerySetTestCase(BaseTestCase):
    def test_get_for_user_with_a_user(self):
        user = self.user

        self.c1.save()
        self.c2.save()
        self.c3.save() # private channel that we are not following
        self.following_private_channel.save()
        self.following_private_channel.followers.add(user)

        self.t1.save()
        self.t2.save()
        self.t3.save()
        self.t4.save()
        self.t5.save()

        self.p1.channel = self.c1
        self.p1.save()
        self.p1.tags.add(self.t1)

        self.p6.channel = self.c2
        self.p6.save()
        self.p6.tags.add(self.t2)
        self.p7.channel = self.c2
        self.p7.save()
        self.p7.tags.add(self.t5)

        self.p5.channel = self.c3
        self.p5.save()
        self.p5.tags.add(self.t3)

        self.p4.channel = self.following_private_channel
        self.p4.save()
        self.p4.tags.add(self.t4)

        viewable = Tag.objects.get_for_user(user)

        self.assertIn(self.t1, viewable)
        self.assertIn(self.t2, viewable)
        self.assertIn(self.t4, viewable)
        self.assertNotIn(self.t3, viewable)
        self.assertNotIn(self.t5, viewable)

    def test_get_for_user_anonymous(self):
        user = self.user
        user.id == None

        self.c1.save()
        self.c3.save()
        self.t1.save()
        self.t2.save()
        self.t3.save()
        self.t4.save()

        self.p1.channel = self.c1
        self.p7.channel = self.c1
        self.p5.channel = self.c3

        self.p1.save()
        self.p7.save()
        self.p5.save()

        self.p1.tags.add(self.t1)
        self.p1.tags.add(self.t2)
        self.p5.tags.add(self.t3)
        self.p7.tags.add(self.t4)

        viewable = Tag.objects.get_for_user(user)

        self.assertIn(self.t1, viewable)
        self.assertIn(self.t2, viewable)

        self.assertNotIn(self.t4, viewable)
        self.assertNotIn(self.t3, viewable)

    def test_only_published_posts_shows_up(self):
        user = self.user

        self.c1.save()
        self.t1.save()
        self.t2.save()

        self.p1.channel = self.c1
        self.p3.channel = self.c1

        self.p1.save()
        self.p3.save() # Status = DRAFT

        self.p1.tags.add(self.t1)
        self.p3.tags.add(self.t2)

        viewable = Tag.objects.get_for_user(user)

        self.assertIn(self.t1, viewable)
        self.assertNotIn(self.t2, viewable)

    def test_tags_only_show_up_if_user_has_access_to_that_Channel(self):

        new_user = get_user_model()
        new_user.id = 1
        self.c1.save()
        self.c3.save() # user does not have access to this channel

        self.p1.channel = self.c1
        self.p2.channel = self.c3

        self.p1.save()
        self.p2.save()

        self.t1.save()
        self.t2.save() 

        self.p1.tags.add(self.t1)
        self.p2.tags.add(self.t2)

        viewable = Tag.objects.get_for_user(new_user)

        self.assertIn(self.t1, viewable)
        self.assertNotIn(self.t2, viewable)