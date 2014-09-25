# -*- coding: utf-8 -*-
from collections import namedtuple
import json
from mock import Mock


MockYoutube = namedtuple(
    'MockYoutube',
    ['ysc', 'yu', 'yc', 'yt', 'yh', 'yosc']
)


youtube_status_code = 200
youtube_url = 'http://www.youtube.com/watch?v=Uqa8YSxx8Gs'
youtube_headers = {'alternate-protocol': '80:quic,p=0.01', 'x-xss-protection': '1; mode=block; report=https://www.google.com/appserve/security-bugs/log/youtube', 'x-content-type-options': 'nosniff', 'transfer-encoding': 'chunked', 'set-cookie': 'VISITOR_INFO1_LIVE=CjPr-wSJxcs; path=/; domain=.youtube.com; expires=Tue, 09-Jun-2015 08:41:28 GMT, YSC=7OUlrcCybMk; path=/; domain=.youtube.com; httponly', 'expires': 'Tue, 27 Apr 1971 19:44:06 EST', 'server': 'gwiseguy/2.0', 'cache-control': 'no-cache', 'date': 'Wed, 08 Oct 2014 20:48:28 GMT', 'p3p': 'CP="This is not a P3P policy! See http://support.google.com/accounts/bin/answer.py?answer=151657&hl=en for more info."', 'content-type': 'text/html; charset=utf-8', 'x-frame-options': 'SAMEORIGIN'}
youtube_cookies = "[Cookie(version=0, name='VISITOR_INFO1_LIVE', value='CjPr-wSJxcs', port=None, port_specified=False, domain='.youtube.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=1433839288, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False), Cookie(version=0, name='YSC', value='7OUlrcCybMk', port=None, port_specified=False, domain='.youtube.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'httponly': None}, rfc2109=False)]"


youtube_text = """<!DOCTYPE html><html lang="en" data-cast-api-enabled="true"><head><script>var ytcsi = {gt: function(n) {n = (n || '') + 'data_';return ytcsi[n] || (ytcsi[n] = {tick: {},span: {},info: {}});},tick: function(l, t, n) {ytcsi.gt(n).tick[l] = t || +new Date();},span: function(l, s, n) {ytcsi.gt(n).span[l] = (typeof s == 'number') ? s :+new Date() - ytcsi.data_.tick[l];},info: function(k, v, n) {ytcsi.gt(n).info[k] = v;}};(function(w, d) {ytcsi.perf = w.performance || w.mozPerformance ||w.msPerformance || w.webkitPerformance;ytcsi.tick('_start', ytcsi.perf ? ytcsi.perf.timing.responseStart : null);var isPrerender = (d.visibilityState || d.webkitVisibilityState) == 'prerender';var vName = d.webkitVisibilityState ? 'webkitvisibilitychange' : 'visibilitychange';if (isPrerender) {ytcsi.info('prerender', 1);var startTick = function() {ytcsi.tick('_start');d.removeEventListener(vName, startTick);};d.addEventListener(vName, startTick, false);}if (d.addEventListener) {d.addEventListener(vName, function() {ytcsi.tick('vc');}, false);}})(window, document);</script>  <script>
try {window.ytbuffer = {};ytbuffer.handleClick = function(e) {var element = e.target || e.srcElement;while (element.parentElement) {if (element.className.match(/(^| )yt-can-buffer( |$)/)) {window.ytbuffer = {bufferedClick: e};element.className += ' yt-is-buffered';break;}element = element.parentElement;}};if (document.addEventListener) {document.addEventListener('click', ytbuffer.handleClick);} else {document.attachEvent('onclick', ytbuffer.handleClick);}} catch(e) {}
(function(){function a(g,h,b){var k=document.getElementsByTagName("html")[0],e=[k.className];g&&1251<=(window.innerWidth||document.documentElement.clientWidth)&&(e.push("guide-pinned"),h&&e.push("show-guide"));b&&(b=(window.innerWidth||document.documentElement.clientWidth)-21-50,1251<=(window.innerWidth||document.documentElement.clientWidth)&&g&&h&&(b-=230),e.push(" ",1262<=b?"content-snap-width-3":1056<=b?"content-snap-width-2":"content-snap-width-1"));k.className=e.join(" ")}
var c=["yt","www","masthead","sizing","runBeforeBodyIsReady"],d=this;c[0]in d||!d.execScript||d.execScript("var "+c[0]);for(var f;c.length&&(f=c.shift());)c.length||void 0===a?d[f]?d=d[f]:d=d[f]={}:d[f]=a;})();
yt.www.masthead.sizing.runBeforeBodyIsReady(false,true,false);
</script>

<script src="//s.ytimg.com/yts/jsbin/www-scheduler-vflBfYpBZ/www-scheduler.js" type="text/javascript" name="www-scheduler/www-scheduler"></script>

<script>var ytimg = {};ytimg.count = 1;ytimg.preload = function(src) {var img = new Image();var count = ++ytimg.count;ytimg[count] = img;img.onload = img.onerror = function() {delete ytimg[count];};img.src = src;};</script>

<link rel="stylesheet" href="//s.ytimg.com/yts/cssbin/www-core-vfl075efx.css" name="www-core">

<script>ytimg.preload("http:\/\/r20---sn-vgqs7ner.googlevideo.com\/crossdomain.xml");ytimg.preload("http:\/\/r20---sn-vgqs7ner.googlevideo.com\/generate_204");</script>


<title>My Voicemail from Uncle Ruckus (Kickstarter Reward!) - YouTube</title><link rel="search" type="application/opensearchdescription+xml" href="http://www.youtube.com/opensearch?locale=en_US" title="YouTube Video Search"><link rel="shortcut icon" href="http://s.ytimg.com/yts/img/favicon-vfldLzJxy.ico" type="image/x-icon">     <link rel="icon" href="//s.ytimg.com/yts/img/favicon_32-vflWoMFGx.png" sizes="32x32"><link rel="canonical" href="http://www.youtube.com/watch?v=Uqa8YSxx8Gs"><link rel="alternate" media="handheld" href="http://m.youtube.com/watch?v=Uqa8YSxx8Gs"><link rel="alternate" media="only screen and (max-width: 640px)" href="http://m.youtube.com/watch?v=Uqa8YSxx8Gs"><link rel="shortlink" href="http://youtu.be/Uqa8YSxx8Gs">      <meta name="title" content="My Voicemail from Uncle Ruckus (Kickstarter Reward!)">

<meta name="description" content="Glenn Beck Special: http://www.kickstarter.com/projects/362353100/the-uncle-ruckus-movie">

<meta name="keywords" content="the boondocks, uncle ruckus, voicemail">

<link rel="alternate" href="android-app://com.google.android.youtube/http/youtube.com/watch/Uqa8YSxx8Gs">


<link rel="alternate" type="application/json+oembed" href="http://www.youtube.com/oembed?format=json&amp;url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DUqa8YSxx8Gs" title="My Voicemail from Uncle Ruckus (Kickstarter Reward!)">
<link rel="alternate" type="text/xml+oembed" href="http://www.youtube.com/oembed?format=xml&amp;url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DUqa8YSxx8Gs" title="My Voicemail from Uncle Ruckus (Kickstarter Reward!)">

<meta property="og:site_name" content="YouTube">
<meta property="og:url" content="http://www.youtube.com/watch?v=Uqa8YSxx8Gs">
<meta property="og:title" content="My Voicemail from Uncle Ruckus (Kickstarter Reward!)">
<meta property="og:image" content="http://i.ytimg.com/vi/Uqa8YSxx8Gs/hqdefault.jpg">

<meta property="og:description" content="Glenn Beck Special: http://www.kickstarter.com/projects/362353100/the-uncle-ruckus-movie">

<meta property="al:ios:app_store_id" content="544007664">
<meta property="al:ios:app_name" content="YouTube">
<meta property="al:ios:url" content="vnd.youtube://www.youtube.com/watch?v=Uqa8YSxx8Gs&amp;feature=applinks">
<meta property="al:android:url" content="http://www.youtube.com/watch?v=Uqa8YSxx8Gs&amp;feature=applinks">
<meta property="al:android:app_name" content="YouTube">
<meta property="al:android:package" content="com.google.android.youtube">
<meta property="al:web:url" content="http://www.youtube.com/watch?v=Uqa8YSxx8Gs&amp;feature=applinks">

<meta property="og:type" content="video">
<meta property="og:video" content="http://www.youtube.com/v/Uqa8YSxx8Gs?version=3&amp;autohide=1">
<meta property="og:video:secure_url" content="https://www.youtube.com/v/Uqa8YSxx8Gs?version=3&amp;autohide=1">
<meta property="og:video:type" content="application/x-shockwave-flash">
<meta property="og:video:width" content="640">
<meta property="og:video:height" content="480">

<meta property="og:video:tag" content="the boondocks">
<meta property="og:video:tag" content="uncle ruckus">
<meta property="og:video:tag" content="voicemail">

<meta property="fb:app_id" content="87741124305">

<meta name="twitter:card" content="player">
<meta name="twitter:site" content="@youtube">
<meta name="twitter:url" content="http://www.youtube.com/watch?v=Uqa8YSxx8Gs">
<meta name="twitter:title" content="My Voicemail from Uncle Ruckus (Kickstarter Reward!)">
<meta name="twitter:description" content="Glenn Beck Special: http://www.kickstarter.com/projects/362353100/the-uncle-ruckus-movie">
<meta name="twitter:image" content="http://i.ytimg.com/vi/Uqa8YSxx8Gs/hqdefault.jpg">
<meta name="twitter:app:name:iphone" content="YouTube">
<meta name="twitter:app:id:iphone" content="544007664">
<meta name="twitter:app:name:ipad" content="YouTube">
<meta name="twitter:app:id:ipad" content="544007664">
<meta name="twitter:app:url:iphone" content="vnd.youtube://www.youtube.com/watch?v=Uqa8YSxx8Gs&amp;feature=applinks">
<meta name="twitter:app:url:ipad" content="vnd.youtube://www.youtube.com/watch?v=Uqa8YSxx8Gs&amp;feature=applinks">
<meta name="twitter:app:name:googleplay" content="YouTube">
<meta name="twitter:app:id:googleplay" content="com.google.android.youtube">
<meta name="twitter:app:url:googleplay" content="http://www.youtube.com/watch?v=Uqa8YSxx8Gs">
<meta name="twitter:player" content="https://www.youtube.com/embed/Uqa8YSxx8Gs">
<meta name="twitter:player:width" content="640">
<meta name="twitter:player:height" content="480">


<link rel="stylesheet" href="//s.ytimg.com/yts/cssbin/www-pageframe-vflqD31-t.css" name="www-pageframe">
<link rel="stylesheet" href="//s.ytimg.com/yts/cssbin/www-watch-transcript-vfl9-k0Vc.css" name="www-watch-transcript">

</head>    <body dir="ltr" class="  ltr    exp-flexwatch-720-mini   site-center-aligned site-as-giant-card appbar-hidden     not-nirvana-dogfood  not-yt-legacy-css  watch8    delayed-frame-styles-not-in  " id="body">

<div id="early-body"></div>
=

<button class="flip control-bar-button yt-uix-button yt-uix-button-dark-overflow-action-menu yt-uix-button-size-default yt-uix-button-has-icon yt-uix-button-empty" type="button" onclick=";return false;"  role="button" aria-pressed="false" aria-expanded="false" aria-haspopup="true" aria-activedescendant="" aria-label="Actions for the queue"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-dark-overflow-action-menu yt-sprite"></span></span><span class="yt-uix-button-arrow yt-sprite"></span><ul class="watch-queue-menu yt-uix-button-menu yt-uix-button-menu-dark-overflow-action-menu" role="menu" aria-haspopup="true" style="display: none;"><li role="menuitem" id="aria-id-27715880556"><span class="watch-queue-menu-choice overflow-menu-choice yt-uix-button-menu-item" data-action="remove-all" onclick=";return false;" >Remove all</span></li><li role="menuitem" id="aria-id-67852355095"><span class="watch-queue-menu-choice overflow-menu-choice yt-uix-button-menu-item" data-action="disconnect" onclick=";return false;" >Disconnect</span></li></ul></button>
</span>
<div class="watch-queue-controls">
<button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button prev-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Previous video"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-prev yt-sprite" title="Previous video"></span></span></button>

<button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button play-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Play"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-play yt-sprite" title="Play"></span></span></button>

<button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button pause-watch-queue-button yt-uix-button-opacity yt-uix-tooltip hid yt-uix-tooltip" type="button" onclick=";return false;" title="Pause"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-pause yt-sprite" title="Pause"></span></span></button>

<button class="yt-uix-button yt-uix-button-size-default yt-uix-button-empty yt-uix-button-has-icon control-bar-button next-watch-queue-button yt-uix-button-opacity yt-uix-tooltip yt-uix-tooltip" type="button" onclick=";return false;" title="Next video"><span class="yt-uix-button-icon-wrapper"><span class="yt-uix-button-icon yt-uix-button-icon-watch-queue-next yt-sprite" title="Next video"></span></span></button>
</div>
</div></div><div class="watch-queue-items-container yt-scrollbar-dark yt-scrollbar"><ol class="watch-queue-items-list playlist-videos-list yt-uix-scroller" data-scroll-action="yt.www.watchqueue.loadThumbnails">  <p class="yt-spinner">
<span class="yt-spinner-img yt-sprite" title="Loading icon"></span>

</body></html>
"""

youtube_oembed_status_code = 200
youtube_oembed_url = 'http://www.youtube.com/oembed?format=json&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DUqa8YSxx8Gs'
youtube_oembed_headers = {'alternate-protocol': '80:quic,p=0.01', 'x-xss-protection': '1; mode=block; report=https://www.google.com/appserve/security-bugs/log/youtube', 'x-content-type-options': 'nosniff', 'transfer-encoding': 'chunked', 'expires': 'Tue, 27 Apr 1971 19:44:06 EST', 'server': 'gwiseguy/2.0', 'cache-control': 'no-cache', 'date': 'Wed, 08 Oct 2014 22:15:43 GMT', 'x-frame-options': 'ALLOWALL', 'content-type': 'application/json', 'p3p': 'CP="This is not a P3P policy! See http://support.google.com/accounts/bin/answer.py?answer=151657&hl=en for more info."'}
youtube_oembed_text = '{"height": 344, "title": "My Voicemail from Uncle Ruckus (Kickstarter Reward!)", "author_url": "http:\\/\\/www.youtube.com\\/user\\/gasphynx", "width": 459, "provider_name": "YouTube", "author_name": "Se\\u00e1n Hayes", "thumbnail_width": 480, "provider_url": "http:\\/\\/www.youtube.com\\/", "thumbnail_height": 360, "thumbnail_url": "http:\\/\\/i.ytimg.com\\/vi\\/Uqa8YSxx8Gs\\/hqdefault.jpg", "html": "\\u003ciframe width=\\"459\\" height=\\"344\\" src=\\"http:\\/\\/www.youtube.com\\/embed\\/Uqa8YSxx8Gs?feature=oembed\\" frameborder=\\"0\\" allowfullscreen\\u003e\\u003c\\/iframe\\u003e", "type": "video", "version": "1.0"}'


def get_mock():
    ysc = youtube_status_code
    yu = youtube_url
    yc = youtube_cookies
    yt = youtube_text
    yh = youtube_headers
    yosc = youtube_oembed_status_code
    you = youtube_oembed_url
    yoh = youtube_oembed_headers
    yot = youtube_oembed_text

    mock_obj_1 = Mock()
    mock_obj_1.status_code = ysc
    mock_obj_1.url = yu
    mock_obj_1.headers = yh
    mock_obj_1.cookies = yc
    mock_obj_1.text = yt
    mock_obj_1.json = lambda: json.loads(mock_obj_1.text)

    mock_obj_2 = Mock()
    mock_obj_2.status_code = 200
    mock_obj_2.url = you
    mock_obj_2.headers = yoh
    mock_obj_2.text = yot
    mock_obj_2.json = lambda: json.loads(mock_obj_2.text)

    return [mock_obj_1, mock_obj_1, mock_obj_2]


def get_mock_no_oembed():
    mock = Mock()
    mock.status_code = youtube_status_code
    mock.url = youtube_url
    mock.cookies = youtube_cookies
    mock.text = 'youtube_text'
    mock.json = lambda: json.loads(mock.text)
    return [mock]
