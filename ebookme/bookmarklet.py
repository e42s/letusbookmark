# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE.txt file in this distribution for details.

import random
import re

from nagare import presentation


class JsBookmarklet(object):
    def __init__(self, script_url, label, title, element_id=None):
        self.script_url = script_url
        self.label = label
        self.title = title
        self.element_id = element_id or self.generate_id()

    @staticmethod
    def generate_id(prefix='bookmarklet'):
        return prefix + str(random.randint(10000000, 99999999))


@presentation.render_for(JsBookmarklet)
def render_bookmarklet(self, h, comp, *args):
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

    h << h.a(self.label,
             title=self.title,
             class_='bookmarklet',
             href='javascript:%s' % js)

    return h.root


# ---------------------------------------------------------------

#    content_url = ...
#    js = """
#    (function(){
#        var d=document,
#            b=d.body, 
#            e=d.createElement('iframe');
#        e.src = '%s';
#        b.appendChild(e);
#    })();
#    """ % content_url
