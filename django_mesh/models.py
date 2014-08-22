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
import re


# Django imports
#from django.contrib.sitemaps import ping_google
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings

#try for adding restricting access
from django.shortcuts import redirect
from model_utils.managers import PassThroughManager
##delete
from login.views import user_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# 3d party imports
from model_utils import Choices
from taggit.managers import TaggableManager

# App imports
from .managers import PostManager, ChannelQuerySet

oembed_regex = re.compile(r'^(?P<spacing>\s*)(?P<url>http://.+)', re.MULTILINE)

#http://djangoadvent.com/1.2/object-permissions/

#TODO: add pages, custom menus
#TODO: Use http://code.google.com/p/django-trackback/

class _Abstract(models.Model):
    slug  = models.SlugField(unique=True)
    #microblog compatible.
    title = models.CharField(max_length=140, unique=True)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        abstract = True

class Channel(_Abstract):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    #TODO: add allowed authors
    #TODO: add members (who can view the channel) and privacy types
    # members self enroll or members added by owner

    ENROLLMENTS = Choices(
        (0, 'SELF', 'Self'),
        (1, 'AUTHOR', 'Author'),
    )
    
    enrollment = models.IntegerField(max_length=1, default=ENROLLMENTS.SELF, choices=ENROLLMENTS)
    
    public = models.BooleanField(default=True, help_text="If False, only followers will be able to see content.")
    
    objects = PassThroughManager.for_queryset_class(ChannelQuerySet)()

    def get_absolute_url(self):
        return reverse('mesh_channel_view', args=(self.slug,))

    
    def can_author(self, user):
        return user in self.authors.all()
    
    class Meta:
        ordering = ['title']


class Post(_Abstract):
    SUMMARY_LENGTH = 50
    
    STATUSES = Choices(
        (0, 'DRAFT',     'Draft',),
        (1, 'PUBLISHED', 'Published',),
    )
    
    channel        = models.ForeignKey(Channel)
    author         = models.ForeignKey(settings.AUTH_USER_MODEL)
    status         = models.IntegerField(max_length=1, default=STATUSES.DRAFT, choices=STATUSES)
    text           = models.TextField(default='')                        #move to abstract
    rendered_text  = models.TextField(default='', blank=True)            #move to abstract
    custom_summary = models.TextField(default='')
    created        = models.DateTimeField(auto_now_add=True, editable=False)
    modified       = models.DateTimeField(auto_now=True, editable=False)
    published      = models.DateTimeField(default=timezone.now())
    
    objects = PostManager()
    tags    = TaggableManager()
    
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
    
    def get_oembed_markup(self, matchobj):
        gd = matchobj.groupdict('')
        
        return '%(spacing)s<a href="%(url)s">%(url)s</a>' % gd
    
    def render(self):
        #TODO: strip out dangerous HTML attributes, only allow basic formatting tags
        
        self.rendered_text = oembed_regex.sub(self.get_oembed_markup, self.text)
    
    def save(self, *args, **kwargs):
        if self.rendered_text == '':
            self.render()
        super(Post, self).save(*args, **kwargs)
#        try:
#            ping_google()
#        except Exception:
#            # Bare 'except' because we could get a variety of HTTP-related exceptions.
#            pass
    
    def get_absolute_url(self):
        return reverse('mesh_post_view', args=(self.slug,))
    
    class Meta:
        ordering = ['published']

