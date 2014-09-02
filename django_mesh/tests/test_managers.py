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
        
        assert self.p1 in active_posts
        assert self.p2 not in active_posts
        assert self.p3 not in active_posts

class ChannelQuerySetTestCase(BaseTestCase):
    def test_get_for_user(self):
        user = self.user
        user.save() 

        self.following_public_channel.save()
        self.following_public_channel.followers.add(user)    
        
        self.following_private_channel.save()               
        self.following_private_channel.followers.add(user)

        self.not_following_public_channel.save()

        self.not_following_private_channel.save()

        viewable = Channel.objects.get_for_user(user)
        
        assert self.following_public_channel in viewable  
        assert self.following_private_channel in viewable
        assert self.not_following_public_channel in viewable
        assert self.not_following_private_channel not in viewable