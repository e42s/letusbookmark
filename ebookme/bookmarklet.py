# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import json
import random
import re
import urlparse

from nagare import presentation, component


def _generate_id(prefix='id'):
    return prefix + str(random.randint(10000000, 99999999))


class JsBookmarklet(object):
    def __init__(self, script_url, label, title=None, element_id=None, link_class='bookmarklet'):
        self.script_url = script_url
        self.label = label
        self.title = title
        self.element_id = element_id or _generate_id('bookmarklet')
        self.link_class = link_class


@presentation.render_for(JsBookmarklet)
def render_js_bookmarklet(self, h, comp, *args):
    js = """
    (function(){
        var d = document,
            b = d.body,
            e = d.createElement('script'),
            oldE = d.getElementById(%(id)s);
        if (oldE) oldE.parentNode.removeChild(oldE);
        e.id = %(id)s;
        e.src = %(script_url)s;
        b.appendChild(e);
    })();
    """ % dict(id=json.dumps(self.element_id),
               script_url=json.dumps(self.script_url))

    js = re.sub('\s+', ' ', js.strip())  # remove unnecessary spaces for compactness

    link = h.a(self.label,
               class_=self.link_class,
               href='javascript:%s' % js)

    if self.title:
        link.set('title', self.title)

    h << link

    return h.root


# ---------------------------------------------------------------

class Bookmarklet(object):
    """Render a Bookmarklet, i.e. a link that can be put in your browser bookmarks/favorites which shows
    the `target` component as an HTML object (like an iframe) in the current page."""

    def __init__(self, target, host_url, label, title=None, width=None, height=None, element_id=None,
                 link_class='bookmarklet'):
        self.target = target if isinstance(target, component.Component) else component.Component(target)
        self.host_url = host_url
        self.label = label
        self.title = title
        self.width = width
        self.height = height
        self.element_id = element_id or _generate_id('bookmarklet')
        self.link_class = link_class


@presentation.render_for(Bookmarklet)
def render_bookmarklet(self, h, comp, *args):
    # See http://aplus.rs/web-dev/insert-html-page-into-another-html-page/
    # See http://intranation.com/test-cases/object-vs-iframe/

    target_url = urlparse.urljoin(self.host_url, 'static/ebookme/test.html')

    subst = dict(
        id=self.element_id,
        target_url=target_url,
        width=self.width,
        height=self.height,
    )

    js = """
    (function(){
        var d=document,
            b=d.body, 
            e=d.createElement('object');
            oldE=d.getElementById('%(id)s');
        if (oldE) oldE.parentNode.removeChild(oldE);
        e.id="%(id)s";
        e.data="%(target_url)s";
        e.type="text/html";
        e.width="%(width)s";
        e.height="%(height)s";
        e.innerHTML='<a href="%(target_url)s">%(target_url)s</a>';
        b.appendChild(e);
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    # On IE 6/7, we also need this:
    #e.classid="clsid:25336920-03F9-11CF-8FD0-00AA00686F13";
    #<!--[if IE]>
    #<style type="text/css">html, body {border:0;overflow:visible;}</style>
    #<![endif]-->

    js = re.sub('\s+', ' ', js.strip())  # remove unnecessary spaces for compactness

    link = h.a(self.label,
               class_=self.link_class,
               href='javascript:%s' % js)

    if self.title:
        link.set('title', self.title)

    h << link

    return h.root
