# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

from nagare import presentation


class Alert(object):
    pass


@presentation.render_for(Alert)
def render_alert(self, h, comp, *args):
    js = "alert(document.location);"
    h << h.script(js, type='text/javascript')
    return h.root
