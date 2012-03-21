# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import json
import random
import re


def _generate_id(prefix='id'):
    return prefix + str(random.randint(10000000, 99999999))


class Mode:
    """What should we do when someone repeatedly click on the bookmarklet?
    Should we execute the bookmarklet action once, repeatedly, or toggle it
    on/off?"""
    Once = 0  # run only once
    Toggle = 1  # switch on/off
    Repeat = 2  # run at each click


def object_bookmarklet(target_url, mode=Mode.Once, width=None, height=None,
                       style=None, id=None, type='text/html',
                       with_location=False):
    """Render a bookmarklet URL that shows the resource found at `target_url`
    as an HTML object (like an iframe) embedded in the current page."""
    subst = dict(
        target_url=json.dumps(target_url),
        mode=json.dumps(mode),
        width=json.dumps(int(width) if width is not None else None),
        height=json.dumps(int(height) if height is not None else None),
        style=json.dumps(style),
        id=json.dumps(id or _generate_id('bookmarklet')),
        type=json.dumps(type),
        location='encodeURIComponent(location.href)' if with_location else '""'
    )

    # no content fallback since IE does not to handle it (or I can't get it to
    # work)
    href = """
    javascript:(function(){
        var d=document,
            b=d.body,
            u=%(target_url)s + %(location)s,
            m=%(mode)s,
            i=%(id)s,
            o=d.getElementById(i);
        if (o) {
            if (m==0) return;
            o.parentNode.removeChild(o);
            if (m==1) return;
        }
        var e=d.createElement('object');
        e.id=i;
        e.data=u;
        e.type=%(type)s;
        e.width=%(width)s;
        e.height=%(height)s;
        e.setAttribute("style", %(style)s);
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces


def script_bookmarklet(target_url, mode=Mode.Once, id=None,
                       type='text/javascript'):
    """Render a bookmarklet URL that executes the script code found at
    `target_url` in the current page."""
    subst = dict(
        target_url=json.dumps(target_url),
        mode=json.dumps(mode),
        id=json.dumps(id or _generate_id('bookmarklet')),
        type=json.dumps(type),
    )

    href = """
    javascript:(function(){
        var d=document,
            b=d.body,
            u=%(target_url)s,
            m=%(mode)s,
            i=%(id)s,
            o=d.getElementById(i);
        if (o) {
            if (m==0) return;
            o.parentNode.removeChild(o);
            if (m==1) return;
        }
        var e=d.createElement('script');
        e.id=i;
        e.src=u;
        e.type=%(type)s;
        b.insertBefore(e, b.firstChild);
    })();
    """ % subst

    return re.sub('\s+', ' ', href.strip())  # remove unnecessary spaces
