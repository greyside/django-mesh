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

#Django imports
from django.conf.urls import patterns, url
from .views import IndexView, ChannelIndexView, ChannelDetailView, PostIndexView, PostDetailView, PostCommentsView
from django_mesh import views

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="mesh_index"),
    url(r'^channels/$', ChannelIndexView.as_view(), name="mesh_channel_index"),
    url(r'^channels/(?P<slug>.+)/$', ChannelDetailView.as_view(), name="mesh_channel_view"),
    url(r'^sub/(?P<slug>.+)/$', views.self_enrollment, name="mesh_sub"),

    url(r'^posts/$', PostIndexView.as_view(), name="mesh_post_index"),
    url(r'^posts/(?P<slug>.+)/comments/$', PostCommentsView.as_view(), name="mesh_post_comments"),
    url(r'^posts/(?P<slug>.+)/$', PostDetailView.as_view(), name="mesh_post_view"),
)

#override dispatch method first, then later on edit queryset
#set self.channel before overriding dispatch method