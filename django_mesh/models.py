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

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from datetime import datetime

# Create your models here.

#http://djangoadvent.com/1.2/object-permissions/

#TODO: add comments

class Channel(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=140, unique=True)
	site = models.ForeignKey(Site)
	
	#TODO: integrate with Sites framework
	
	class Meta:
		ordering = ['name']
		unique_together = (('slug', 'site'), ('name', 'site'))

class Post(models.Model):
	author = models.ForeignKey(User)
	#microblog compatible.
	slug = models.SlugField(unique_for_date='published')
	title = models.CharField(max_length=140, unique_for_date='published')
	text = models.TextField(default="")
	items = models.ManyToManyField('Item', through='PostItem')
	channels = models.ManyToManyField(Channel)
	
	
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_edited = models.DateTimeField(auto_now=True, editable=False)
	published = models.DateTimeField(default=datetime.now())#TODO: default to now
	
	class Meta:
		ordering = ['published']

class Item(models.Model):
	#http://www.oembed.com/
	#needs to handle:
	#links to web pages - show screenshot thumbnail
	#oembed-able links - store JSON, render oembed data on request. store thumbnail if none is provided.
	#attachments - generate thumbnail and store if possible, otherwise show generic icon. Embed player/viewer if possible, else give download link
	
	#I think I'll just store title and url, and leave the rest to jquery-oembed.
	#attachments can be handled by creating an oembed provider, or it could be faked.
	#services: http://api.embed.ly/
	url = models.URLField(unique=True)
	title = models.CharField(max_length=140)
	added = models.DateTimeField(auto_now_add=True, editable=False)
	
	class Meta:
		ordering = ['added']

class PostItem(models.Model):
	post = models.ForeignKey(Post)
	item = models.ForeignKey(Item)
	text = models.TextField(default="")
	order = models.PositiveIntegerField()
	
	class Meta:
		ordering = ['order']
