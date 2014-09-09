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
from django.utils import timezone
from django.db.models.query import QuerySet 
from django.db.models import Q

class PostQuerySet(QuerySet):
    def active(self):
        return self.filter(status=self.model.STATUSES.PUBLISHED, published__lt=timezone.now())

    def get_for_user(self, user):
        if user.id == None:
            return self.filter(channel__public=True)
        else:
            return self.filter(Q(channel__public=True) | Q(channel__followers=user))

class ChannelQuerySet(QuerySet):
    def get_for_user(self, user):
        if user.id == None:
            return self.filter(public=True)
        else:
            return self.filter(Q(public=True) | Q(followers=user) | Q(enrollment=self.model.ENROLLMENTS.SELF)).distinct()


