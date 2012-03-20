# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import urlparse

from nagare import presentation, component, wsgi

from letusbookmark.bookmarklet import object_bookmarklet, script_bookmarklet, Mode
from letusbookmark.counter import Counter


class LetUsBookmark(object):
    APP_TITLE = "Let Us Bookmark"

    def __init__(self):
        self.counter = component.Component(Counter())


@presentation.render_for(LetUsBookmark, model='head')
def render_let_us_bookmark_head(self, h, *args):
    h.head << h.head.title(self.APP_TITLE)
    h.head << h.head.meta({'http-equiv': 'Content-Type', 'content': 'text/html; charset=UTF-8'})
    h.head.css_url('app.css')
    return h.root


@presentation.render_for(LetUsBookmark, model='body')
def render_let_us_bookmark_body(self, h, comp, *args):
    with h.h1:
        h << self.APP_TITLE

    with h.p:
        h << "Please drop these bookmarklets in your browser toolbar:"

    with h.ul(class_='buttons'):
        with h.li:
            url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.html')
            href = object_bookmarklet(url, mode=Mode.Once)
            h << h.a('Lorem Ipsum',
                     title="Drop me in your browser toolbar!",
                     class_='bookmarklet',
                     href=href)

        with h.li:
            url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.js')
            href = script_bookmarklet(url, mode=Mode.Repeat)
            h << h.a('Location',
                     title="Drop me in your browser toolbar!",
                     class_='bookmarklet',
                     href=href)

        with h.li:
            url = self.application_url + '/location?url='
            style = "width: 100%; height: 30px;"
            href = object_bookmarklet(url, with_location=True, mode=Mode.Toggle, style=style)
            h << h.a('Location2',
                     title="Drop me in your browser toolbar!",
                     class_='bookmarklet',
                     href=href)

        with h.li:
            url = self.application_url + '/counter'
            style = "position: fixed; top: 10px; right: 10px; z-index: 16777271;"
            href = object_bookmarklet(url, mode=Mode.Toggle, width=120, height=46, style=style)
            h << h.a('Counter',
                     title="Drop me in your browser toolbar!",
                     class_='bookmarklet',
                     href=href)

    return h.root


@presentation.render_for(LetUsBookmark)
def render_let_us_bookmark(self, h, comp, *args):
    h << comp.render(h, model='head')
    h << comp.render(h, model='body')
    return h.root


@presentation.init_for(LetUsBookmark, "url == ('counter',)")
def init_render_let_us_bookmark_counter(self, url, comp, *args):
    comp.becomes(Counter())


@presentation.init_for(LetUsBookmark, "url == ('location',)")
def init_render_let_us_bookmark_alert(self, url, comp, http_method, request):
    # The referrer information is lost when we call an HTTP URL from a HTTPS one
    # Also, depending on the browser privacy settings, the referrer information
    # may not be sent at all. So we can't rely on it.
    #origin_url = request.referrer
    origin_url = request.params['url']
    comp.becomes(Location(origin_url))


# ---------------------------------------------------------------

class Location(object):
    def __init__(self, url):
        self.url = url


@presentation.render_for(Location)
def render_location(self, h, comp, *args):
    h << "You are here: %s" % self.url
    return h.root


# ---------------------------------------------------------------

class LetUsBookmarkApp(wsgi.WSGIApp):
    def start_request(self, root, request, response):
        super(LetUsBookmarkApp, self).start_request(root, request, response)
        root().host_url = request.host_url
        root().application_url = request.application_url


# ---------------------------------------------------------------
app = LetUsBookmarkApp(lambda * args: component.Component(LetUsBookmark(*args)))
