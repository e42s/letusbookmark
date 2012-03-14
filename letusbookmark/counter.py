# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

from nagare import presentation


class Counter(object):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1


@presentation.render_for(Counter)
def render_counter(self, h, comp, *args):
    # we use a CSS reset to prevent the host page styles to leak in our component
    h.head.css_url('http://yui.yahooapis.com/2.9.0/build/reset/reset-min.css')
    # component specific CSS
    h.head.css_url('counter.css')

    with h.div(class_='counter'):
        h << h.a('-').action(self.decrement)
        h << h.span(' | ', class_='separator')
        h << h.span(self.value, class_='value')
        h << h.span(' | ', class_='separator')
        h << h.a('+').action(self.increment)

    js = """
    if (window.console) {
        console.log("Location: " + window.parent.location);
    }
    """
    h << h.script(js, type='text/javascript')

    return h.root
