# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import urlparse

from nagare import presentation, component, wsgi

from letusbookmark.bookmarklet import object_bookmarklet, script_bookmarklet
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
        h << "Please drop these buttons in your browser toolbar:"

        with h.ul(class_='buttons'):
            with h.li:
                object_url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.html')
                object_href = object_bookmarklet(object_url, width='500', height='50')
                h << h.a('Object Bookmarklet',
                         title="Drop me in your browser toolbar!",
                         class_='bookmarklet',
                         href=object_href)

            with h.li:
                script_url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.js')
                script_href = script_bookmarklet(script_url)
                h << h.a('JS Bookmarklet',
                         title="Drop me in your browser toolbar!",
                         class_='bookmarklet',
                         href=script_href)

            with h.li:
                object_url = ''
                object_href = object_bookmarklet(object_url, width='500', height='50')
                h << h.a('Counter Bookmarklet',
                         title="Drop me in your browser toolbar!",
                         class_='bookmarklet',
                         href=object_href)

    return h.root


@presentation.render_for(LetUsBookmark)
def render_let_us_bookmark(self, h, comp, *args):
    h << comp.render(h, model='head')
    h << comp.render(h, model='body')
    return h.root


# ---------------------------------------------------------------

class LetUsBookmarkApp(wsgi.WSGIApp):
    def start_request(self, root, request, response):
        super(LetUsBookmarkApp, self).start_request(root, request, response)
        root().host_url = request.host_url


# ---------------------------------------------------------------
app = LetUsBookmarkApp(lambda * args: component.Component(LetUsBookmark(*args)))
