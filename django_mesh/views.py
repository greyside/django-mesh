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
import logging

# Django imports
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

#try for restriction
#from login.views import user_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# App imports
from .models import Channel, Post

logger = logging.getLogger(__name__)

class IndexView(ListView):
    queryset = Post.objects.active()
    template_name = 'django_mesh/index.html'
    context_object_name='post_list'

class ChannelIndexView(ListView):
    model = Channel
    template_name = 'django_mesh/channel_index.html'
    context_object_name='channel_list'

class ChannelDetailView(ListView):
    queryset = Post.objects.active()
    template_name = 'django_mesh/channel_view.html'
    context_object_name='post_list'
    
    def get_queryset(self, *args, **kwargs):
        ret = super(ChannelDetailView, self).get_queryset(*args, **kwargs)
        
        c = get_object_or_404(Channel, slug=self.kwargs['slug'])
        
        return ret.filter(channel=c)


class PostIndexView(ListView):

    logged_in = ()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
         if not request.user.has_perms(self.logged_in):
            messages.error( request,
                            'You do not have the permission required to perform the '
                            'requested operation.')
            return redirect(settings.LOGIN_URL)
         else:
            return super(PostIndexView, self).dispatch(request, *args, **kwargs)

    queryset = Post.objects.active()
    template_name = 'django_mesh/post_index.html'
    context_object_name='post_list'

class PostDetailView(DetailView):
    queryset = Post.objects.active()
    template_name = 'django_mesh/post_view.html'
    context_object_name='post'

class PostCommentsView(DetailView):
    queryset = Post.objects.active()
    template_name = 'django_mesh/post_comments.html'
    context_object_name='post'
