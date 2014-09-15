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
from ..models import Post, Channel

# Test imports
from .util import BaseTestCase

class PostQuerySetTestCase(BaseTestCase):
    def test_active(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()
        self.p2.channel = self.c1
        self.p2.save()
        self.p3.channel = self.c1
        self.p3.save()

        active_posts = Post.objects.active()

        self.assertIn(self.p1, active_posts)
        self.assertNotIn(self.p2, active_posts)
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

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        viewable = Post.objects.get_for_user(user)

        self.assertIn(self.p1, viewable)
        self.assertIn(self.p2, viewable)
        self.assertIn(self.p4, viewable)

        self.assertNotIn(self.p5, viewable)

    def test_get_for_user_not_following_channel(self):
        user = self.user

        self.following_public_channel.save()
        self.p1.channel = self.following_public_channel
        self.p1.save()

        self.not_following_public_channel.save()
        self.p4.channel = self.not_following_public_channel
        self.p4.save()

        self.following_private_channel.save()
        self.p2.channel = self.following_private_channel
        self.p2.save()

        self.not_following_private_channel.save()
        self.p5 = self.not_following_private_channel
        self.p5.save()

        viewable = Post.objects.get_for_user(user)

        self.assertIn(self.p1, viewable)
        self.assertIn(self.p4, viewable)

        self.assertNotIn(self.p2, viewable)
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