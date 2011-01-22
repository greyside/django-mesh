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

from django.views.generic import list_detail
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from models import *
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
	return list_detail.object_list(
		request,
		queryset = Post.objects.active(),
		template_name='django_mesh/index.html',
		template_object_name='post'
	)

def channel_index(request):
	#FIXME: only show channels for this site
	return list_detail.object_list(
		request,
		queryset = Channel.objects.all(),
		template_name='django_mesh/channel_index.html',
		template_object_name='channel'
	)

def channel_view(request, slug):
	c = Channel.objects.get(slug=slug)
	return list_detail.object_list(
		request,
		queryset = Post.objects.active().filter(channels=c),
		template_name='django_mesh/channel_view.html',
		template_object_name='post'
	)

def post_index(request):
	return list_detail.object_list(
		request,
		queryset = Post.objects.active(),
		template_name='django_mesh/post_index.html',
		template_object_name='post'
	)

def post_view(request, slug):
	return list_detail.object_detail(
		request,
		Post.objects.active(),
		slug=slug,
		template_name='django_mesh/post_view.html',
		template_object_name='post'
	)

def post_comments(request, slug):
	return list_detail.object_detail(
		request,
		Post.objects.active(),
		slug=slug,
		template_name='django_mesh/post_comments.html',
		template_object_name='post'
	)
