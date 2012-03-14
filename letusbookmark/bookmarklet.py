# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import json
import random
import re


def _generate_id(prefix='id'):
    return prefix + str(random.randint(10000000, 99999999))


def object_bookmarklet(target_url, width=None, height=None, style=None, id=None, type='text/html'):
    """Render a bookmarklet URL that shows the resource found at `target_url` as an HTML object (like
    an iframe) embedded in the current page."""
    subst = dict(
        id=json.dumps(id or _generate_id('bookmarklet')),
        target_url=json.dumps(target_url),
        width=json.dumps(width),
        height=json.dumps(height),
        style=json.dumps(style),
        type=json.dumps(type),
    )

    href = """
    javascript:(function(){
        var d=document,
            b=d.body, 
            i=%(id)s,
            u=%(target_url)s,
            o=d.getElementById(i);
        if (o) {
            o.parentNode.removeChild(o);
        }
        else {
            var e=d.createElement('object');
            e.id=i;
            e.data=u;
            e.type=%(type)s;
            e.width=%(width)s;
            e.height=%(height)s;
            e.setAttribute("style", %(style)s);
            e.innerHTML='<a href="' + u + '">' + u + '</a>';
            b.insertBefore(e, b.firstChild);
        }
    })();
    """ % subst

    # On IE 6/7, we also need this:
    # See http://aplus.rs/web-dev/insert-html-page-into-another-html-page/
    #e.classid="clsid:25336920-03F9-11CF-8FD0-00AA00686F13";
    #<!--[if IE]>
    #<style type="text/css">html, body {border:0;overflow:visible;}</style>
    #<![endif]-->

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces for compactness


def script_bookmarklet(target_url, id=None, type='text/javascript'):
    """Render a bookmarklet URL that executes the script code found at `target_url` in the
    current page."""
    subst = dict(
        id=json.dumps(id or _generate_id('bookmarklet')),
        target_url=json.dumps(target_url),
        type=json.dumps(type),
    )

    href = """
    javascript:(function(){
        var d=document,
            b=d.body,
            i=%(id)s,
            u=%(target_url)s,
            e=d.createElement('script'),
            o=d.getElementById(i);
        if (o) o.parentNode.removeChild(o);
        e.id=i;
        e.src=u;
        e.type=%(type)s;
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces for compactness
