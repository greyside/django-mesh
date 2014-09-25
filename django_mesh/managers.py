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

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class PostQuerySet(QuerySet):

    def active(self):
        return self.filter(status=self.model.STATUSES.PUBLISHED, published__lte=timezone.now()).distinct()

    def get_for_user(self, user):
        if user.id == None:
            return self.filter(channel__public=True).active()
        else:
            return self.filter(Q(channel__public=True) | Q(channel__followers=user)).active()

class ChannelQuerySet(QuerySet):
    def get_for_user(self, user):
        if user.id == None:
            return self.filter(public=True)
        else:
            return self.filter(Q(public=True) | Q(followers=user) | Q(enrollment=self.model.ENROLLMENTS.SELF)).distinct()

class TagQuerySet(QuerySet):
    def get_for_user(self, user):

        from .models import Post
        q_object = Q(post__channel__public=True) & Q(post__status=Post.STATUSES.PUBLISHED)

        if user.id is not None:
            q_object = Q(post__channel__followers=user.id) | q_object

        return self.filter(q_object).distinct().filter(post__published__lte=timezone.now())
