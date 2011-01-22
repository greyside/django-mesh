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

from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('django_mesh.views',
	url(r'^$', 'index', name="mesh_index"),
	url(r'^channels/$', 'channel_index', name="mesh_channel_index"),
	url(r'^channels/(.*)/$', 'channel_view', name="mesh_channel_view"),
	url(r'^posts/$', 'post_index', name="mesh_post_index"),
	url(r'^posts/(.*)/comments/$', 'post_comments', name="mesh_post_comments"),
	url(r'^posts/(.*)/$', 'post_view', name="mesh_post_view"),
)
