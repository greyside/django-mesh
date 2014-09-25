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

# Test imports
from .util import BaseTestCase
import markdown, textile
import requests
from pyembed.markdown import PyEmbedMarkdown
from pyembed.core import PyEmbed
from django_mesh.models import _Abstract
from .youtube_data import get_mock, get_mock_no_oembed
from django.core.urlresolvers import reverse

from mock import patch, Mock



class PostTestCase(BaseTestCase):
    def test_has_auto_summary(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        self.assertEqual(self.p1.summary, self.p1.teaser)
        self.assertNotEqual(self.p1.summary, self.p1.custom_summary)

    def test_has_custom_summary(self):
        self.c1.save()
        self.p1.custom_summary = 'This is a summary.'
        self.p1.channel = self.c1
        self.p1.save()
        
        self.assertNotEqual(self.p1.summary, self.p1.teaser)
        self.assertEqual(self.p1.summary, self.p1.custom_summary)

    def test_markup(self):
        self.c1.save()

        self.p1.channel = self.c1
        self.p7.channel = self.c1
        self.p8.channel = self.c1

        self.p1.text = 'hello'
        self.p7.text = 'hello'
        self.p8.text = 'hello'

        self.p1.save() # simple
        self.p7.save() #markdown
        self.p8.save() #textile

        expected_html_markup_and_textile = """<p>hello</p>"""
        expected_html_simple = """hello"""


        self.assertHTMLEqual(expected_html_simple, self.p1.rendered_text)
        self.assertHTMLEqual(expected_html_markup_and_textile, self.p7.rendered_text)
        self.assertHTMLEqual(expected_html_markup_and_textile, self.p8.rendered_text)

    def test_rendered_text_stays_the_same_when_no_links(self):
        self.assertNotEqual(self.p1.text, '')
        self.assertEqual(self.p1.rendered_text, '')

        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()

        self.assertEqual(self.p1.rendered_text, self.p1.text)

    def test_get_absolute_url(self):
        self.c1.save()
        self.p1.channel = self.c1
        url = self.p1.get_absolute_url()

        self.assertGreater(len(url),0)

    def test_str_unicode(self):
        self.c1.save()
        self.p1.channel = self.c1
        self.p1.save()


        returned_title = str(self.p1)
        self.assertEqual(self.p1.title, returned_title)

    @patch('requests.sessions.Session.request')
    def test_check_if_markdown_automatically_wrap_plain_URLs_in_anchor_tags(self, mock_request):

        self.c1.save()
        self.p7.channel = self.c1

        self.p7.text = 'hello, \n plain_url \n www.google.com \n or \n https://www.google.com' # only add anchors if Protocol, also markdown needs doublespace for new paragraph
        expected_html = """<p>hello, plain_url www.google.com or <a href="https://www.google.com">https://www.google.com</a></p>"""
        self.p7.save() #markdown

        self.assertHTMLEqual(expected_html, self.p7.rendered_text)
        self.assertEqual(mock_request.call_count, 0)

    @patch('requests.sessions.Session.request')
    def test_simple(self, mock_request):

        self.c1.save()
        self.p1.channel = self.c1
        self.p1.text = '<a href="www.google.com"> google link </a> is the link, also https://www.facebook.com but not www.google.com\n  \n  should not have paragraph insert'
        self.p1.slug = 'testing_html_escape'
        self.p1.save()
        expected_html = """<a href="www.google.com"> google link </a> is the link, 
                            also <a href="https://www.facebook.com">https://www.facebook.com</a> 
                            but not www.google.com\n  \n  should not have paragraph insert"""

        self.assertHTMLEqual(expected_html,self.p1.rendered_text)
        self.assertEqual(mock_request.call_count, 0)

    @patch('requests.sessions.Session.request')
    def test_automatic_anchors_to_links_on_own_line_if_markdown_chosen(self, mock_request):
        mock_request.side_effect = get_mock_no_oembed()
        
        self.p7.text = "foo\n   \n http://somelink\n" # generates foo, paragraph, anchored links
        expected_html = """<p>foo</p>
                            <p><a href="http://somelink">http://somelink</a></p>"""

        self.assertEqual(self.p7.rendered_text, '')

        self.c1.save()
        self.p7.channel = self.c1
        self.p7.save()

        self.assertHTMLEqual(expected_html, self.p7.rendered_text)
        self.assertEqual(mock_request.call_count, 2)

    @patch('requests.sessions.Session.request')
    def test_doesnt_embed_with_surrounding_text(self, mock_request):

        self.c1.save()
        self.p7.text = "some text here, should NOT embed http://www.youtube.com/watch?v=Uqa8YSxx8Gs other text here"
        self.p7.channel = self.c1
        self.p7.save()
        expected_html = """<p>some text here, should NOT embed <a href="http://www.youtube.com/watch?v=Uqa8YSxx8Gs">http://www.youtube.com/watch?v=Uqa8YSxx8Gs</a> other text here</p>""" 

        self.assertHTMLEqual(expected_html, self.p7.rendered_text)
        self.assertEqual(mock_request.call_count, 0)

    @patch('requests.sessions.Session.request')
    def test_embed_works_with_markdown(self, mock_request):

        mock_request.side_effect = iter(get_mock())

        self.c1.save()
        self.p7.text = "http://www.youtube.com/watch?v=Uqa8YSxx8Gs"
        self.p7.channel = self.c1
        self.p7.save()

        expected_html = """<p><iframe allowfullscreen="" frameborder="0" height="344" 
                                src="http://www.youtube.com/embed/Uqa8YSxx8Gs?feature=oembed" width="459">
                            </iframe></p>""" 

        self.assertHTMLEqual(expected_html, self.p7.rendered_text)
        self.assertEqual(mock_request.call_count, 3)

class ChannelTestCase(BaseTestCase):
    def test_get_absolute_url(self):
        self.c1.save()
        url = self.c1.get_absolute_url()
        self.assertGreater(len(url),0)

    def test_str_unicode(self):
        self.c1.save()

        returned_title = str(self.c1)
        self.assertEqual(self.c1.title, returned_title)

class TagTestCase(BaseTestCase):

    def test_get_absolute_url(self):
        self.t1.save()
        url = self.t1.get_absolute_url()

        self.assertGreater(len(url), 0)

    def test_str_unicode(self):
        self.t1.save()
        returned_title = str(self.t1)
        self.assertEqual(self.t1.title, returned_title)
