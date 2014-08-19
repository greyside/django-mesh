from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.register, name='register'), # ADD NEW PATTERN!
    )

