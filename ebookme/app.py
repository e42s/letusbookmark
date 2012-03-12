# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import urlparse

from nagare import presentation, component, wsgi

from ebookme.bookmarklet import bookmarklet, js_bookmarklet


class EbookMe(object):
    APP_TITLE = "Ebook.me"


@presentation.render_for(EbookMe, model='head')
def render_ebookme_head(self, h, *args):
    h.head << h.head.title(self.APP_TITLE)
    h.head << h.head.meta({'http-equiv': 'Content-Type', 'content': 'text/html; charset=UTF-8'})
    h.head.css_url('screen.css')
    return h.root


@presentation.render_for(EbookMe, model='body')
def render_ebookme_body(self, h, comp, *args):
    with h.h1:
        h << self.APP_TITLE

    with h.p:
        h << "Please drop these buttons in your browser toolbar:"

        with h.ul(class_='buttons'):
            with h.li:
                page_url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.html')
                page_href = bookmarklet(page_url, width='500', height='50')
                h << h.a('%s Object' % self.APP_TITLE,
                         title="Drop me in your browser toolbar!",
                         class_='bookmarklet',
                         href=page_href)

            with h.li:
                script_url = urlparse.urljoin(self.host_url, h.head.static_url + 'bookmarklet.js')
                js_href = js_bookmarklet(script_url)
                h << h.a('%s JS' % self.APP_TITLE,
                         title="Drop me in your browser toolbar!",
                         class_='bookmarklet',
                         href=js_href)

    return h.root


@presentation.render_for(EbookMe)
def render_ebookme(self, h, comp, *args):
    h << comp.render(h, model='head')
    h << comp.render(h, model='body')
    return h.root


# ---------------------------------------------------------------

class EbookMeApp(wsgi.WSGIApp):
    def start_request(self, root, request, response):
        super(EbookMeApp, self).start_request(root, request, response)
        root().host_url = request.host_url


# ---------------------------------------------------------------
app = EbookMeApp(lambda * args: component.Component(EbookMe(*args)))
