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

#Python imports
from datetime import timedelta
import re

#Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils import timezone

#App imports
from .. import models
from ..models import Channel, Post

class BaseTestCase(TestCase):
    def setUp(self):
        self._old_oembed_regex = models.oembed_regex
        models.oembed_regex = re.compile(r'^(?P<spacing>\s*)(?P<url>http://.+)', re.MULTILINE)
        
        self.username  = 'test_user'
        self.password  = 'foobar'
        self.user  = User.objects.create_user(self.username, 'test_user@example.com', self.password)
        self.c1 = Channel(
            slug = 'public',
            title = 'Public',
        )
        self.c2 = Channel(
            slug = 'another-channel',
            title = 'Another Channel',
        )
        self.following_public_channel = Channel(
            slug = 'following-public',
            title = 'following public',
            public = True,

        )

        self.following_private_channel = Channel(
            slug = 'following-private',
            title = 'Following private',
            public = False,
        )

        self.not_following_public_channel = Channel(
            slug = 'not-following-public',
            title = 'Not following public',
            public = True,

        )

        self.not_following_private_channel = Channel(
            slug = 'not-following-private',
            title = 'not following private',
            public = False,

        )

        self.p1 = Post(
            author = self.user,
            slug = 'unit-testing-unit-tests',
            title = 'Are you unit testing your unit tests? Learn all about the latest best practice: TDTDD',
            text = 'Lorem Ipsum etc.',
            status = Post.STATUSES.PUBLISHED
        )
        self.p2 = Post(
            author = self.user,
            slug = 'tree-falls-forest',
            title = 'Tree Falls in Forest, No One Notices',
            published = timezone.now()+timedelta(days=1),
            status = Post.STATUSES.PUBLISHED
        )
        self.p3 = Post(
            author = self.user,
            slug = 'tree-falls-forest-again',
            title = 'Tree Falls in Forest, Could There be a Tree Flu Epidemic?',
            status = Post.STATUSES.DRAFT
        )
        self.comment1 = Comment(
            site = Site.objects.get_current(),
            user = self.user,
            comment = 'Thanks for sharing.',
        
        )
    
    def tearDown(self):
        #FIXME: dqc doesn't intercept db destruction or rollback
        cache.clear()
        
        models.oembed_regex = self._old_oembed_regex

