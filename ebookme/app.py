# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE.txt file in this distribution for details.


from nagare import presentation, wsgi, component
import re


class EbookMe(object):
    APP_TITLE = "Ebook.me"


@presentation.render_for(EbookMe, model='head')
def render_ebookme_head(self, h, *args):
    h.head << h.head.title(self.APP_TITLE)
    h.head << h.head.meta({'http-equiv': 'Content-Type', 'content': 'text/html; charset=UTF-8'})
    h.head.css_url('/static/ebookme/screen.css')
    return h.root


@presentation.render_for(EbookMe, model='body')
def render_ebookme_body(self, h, comp, *args):
    with h.h1:
        h << self.APP_TITLE

    with h.p:
        h << "Please drop this button to your browser toolbar: "
        h << component.Component(Bookmarklet(self.host_url,
                                             self.APP_TITLE,
                                             "Drop me in your browser toolbar!"))

    return h.root


@presentation.render_for(EbookMe)
def render_ebookme(self, h, comp, *args):
    h << comp.render(h, model='head')
    h << comp.render(h, model='body')
    return h.root


# ---------------------------------------------------------------

class Bookmarklet(object):
    def __init__(self, host_url, label, title):
        self.host_url = host_url
        self.label = label
        self.title = title


@presentation.render_for(Bookmarklet)
def render_bookmarklet(self, h, comp, *args):
    full_static_url = self.host_url + h.head.static_url
    element_id = h.generate_id('ebookme')
    js = """
    (function(){
        var d=document, e=d.createElement('script'), b=d.body, l=d.location;
        e.id = "%(element_id)s";
        e.src = "%(static_url)sebookme.js";
        b.appendChild(e);
    })();
    """ % dict(element_id=element_id, static_url=full_static_url)
    js = re.sub('\s+', ' ', js.strip())
    h << h.a(self.label,
             title=self.title,
             class_='bookmarklet',
             href='javascript:%s' % js)

    return h.root

# ---------------------------------------------------------------

class EbookMeApp(wsgi.WSGIApp):
    def start_request(self, root, request, response):
        super(EbookMeApp, self).start_request(root, request, response)
        root().host_url = request.host_url


# ---------------------------------------------------------------
app = EbookMeApp(lambda * args: component.Component(EbookMe(*args)))
