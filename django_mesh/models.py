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

# Python imports
from __future__ import unicode_literals
import re

# Django imports
#from django.contrib.sitemaps import ping_google
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings

# 3d party imports
from model_utils import Choices
from model_utils.managers import PassThroughManager
from taggit.managers import TaggableManager

# App imports
from .managers import PostQuerySet, ChannelQuerySet

oembed_regex = re.compile(r'^(?P<spacing>\s*)(?P<url>http://.+)', re.MULTILINE)

@python_2_unicode_compatible
class _Abstract(models.Model):     #microblog compatible.
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=140, unique=True)
    text = models.TextField(default='')
    rendered_text = models.TextField(default='', blank=True)

    def get_oembed_markup(self, matchobj):
        gd = matchobj.groupdict('')
        return '%(spacing)s<a href="%(url)s">%(url)s</a>' % gd

    def render(self):
        #TODO: strip out dangerous HTML attributes, only allow basic formatting tags
        self.rendered_text = oembed_regex.sub(self.get_oembed_markup, self.text)

    def save(self, *args, **kwargs):
        if self.rendered_text == '':
            self.render()

        super(_Abstract, self).save(*args, **kwargs)
#        try:
#            ping_google()
#        except Exception:
#            # Bare 'except' because we could get a variety of HTTP-related exceptions.
#            pass

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class Channel(_Abstract):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    ENROLLMENTS = Choices(
        (0, 'SELF', 'Self'),
        (1, 'AUTHOR', 'Author'),
    )

    public = models.BooleanField(default=True, help_text="If False, only followers will be able to see content.")

    enrollment = models.IntegerField(max_length=1, default=ENROLLMENTS.SELF, choices=ENROLLMENTS)

    objects = PassThroughManager.for_queryset_class(ChannelQuerySet)()

    def get_absolute_url(self):
        return reverse('mesh_channel_view', args=(self.slug,))

    class Meta:
        ordering = ['title']

class Post(_Abstract):
    SUMMARY_LENGTH = 50

    STATUSES = Choices(
        (0, 'DRAFT',     'Draft',),
        (1, 'PUBLISHED', 'Published',),
    )

    channel         = models.ForeignKey(Channel)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL)
    status          = models.IntegerField(max_length=1, default=STATUSES.DRAFT, choices=STATUSES)
    custom_summary  = models.TextField(default='')
    created         = models.DateTimeField(auto_now_add=True, editable=False)
    modified        = models.DateTimeField(auto_now=True, editable=False)
    published       = models.DateTimeField(default=timezone.now())

    objects = PassThroughManager.for_queryset_class(PostQuerySet)()
    tags            = TaggableManager()

    def _get_teaser(self):
        "A small excerpt of text that can be used in the absence of a custom summary."
        return self.text[:Post.SUMMARY_LENGTH]

    teaser = property(_get_teaser)

    def _get_summary(self):
        "Returns custom_summary, or teaser if not available."
        if len(self.custom_summary) > 0:
            return self.custom_summary
        else:
            return self.teaser

    summary = property(_get_summary)

    def get_absolute_url(self):
        return reverse('mesh_post_view', args=(self.slug,))

    class Meta:
        ordering = ['published']