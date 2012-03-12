# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import json
import random
import re


def _generate_id(prefix='id'):
    return prefix + str(random.randint(10000000, 99999999))


def bookmarklet(target_url, width=None, height=None, element_id=None):
    """Render a bookmarklet URL that show the page found at `target_url` as an HTML object (like
    an iframe) embedded in the current page"""
    element_id = element_id or _generate_id('bookmarklet')

    subst = dict(
        element_id=json.dumps(element_id),
        target_url=json.dumps(target_url),
        width=json.dumps(width),
        height=json.dumps(height),
    )

    href = """
    javascript:(function(){
        var d=document,
            b=d.body, 
            i=%(element_id)s,
            u=%(target_url)s,
            e=d.createElement('object'),
            o=d.getElementById(i);
        if (o) o.parentNode.removeChild(o);
        e.id=i;
        e.data=u;
        e.type="text/html";
        e.width=%(width)s;
        e.height=%(height)s;
        e.innerHTML='<a href="' + u + '">' + u + '</a>';
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    # On IE 6/7, we also need this:
    # See http://aplus.rs/web-dev/insert-html-page-into-another-html-page/
    #e.classid="clsid:25336920-03F9-11CF-8FD0-00AA00686F13";
    #<!--[if IE]>
    #<style type="text/css">html, body {border:0;overflow:visible;}</style>
    #<![endif]-->

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces for compactness


def js_bookmarklet(target_url, element_id=None):
    """Render a bookmarklet URL that executes the javascript code found at `target_url` in the
    current page."""
    element_id = element_id or _generate_id('bookmarklet')

    subst = dict(
        element_id=json.dumps(element_id),
        target_url=json.dumps(target_url),
    )

    href = """
    javascript:(function(){
        var d=document,
            b=d.body,
            i=%(element_id)s,
            u=%(target_url)s,
            e=d.createElement('script'),
            o=d.getElementById(i);
        if (o) o.parentNode.removeChild(o);
        e.id=i;
        e.src=u;
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces for compactness
