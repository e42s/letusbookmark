# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import random
import re

from nagare import presentation


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
            oldE = d.getElementById('%(id)s');
        if (oldE) oldE.parentNode.removeChild(oldE);
        e.id = '%(id)s';
        e.src = '%(script_url)s';
        b.appendChild(e);
    })();
    """ % dict(id=self.element_id,
               script_url=self.script_url)

    js = re.sub('\s+', ' ', js.strip())  # remove unnecessary spaces for compactness

    link = h.a(self.label,
             class_=self.link_class,
             href='javascript:%s' % js)

    if self.title:
        link.set('title', self.title)

    h << link

    return h.root
