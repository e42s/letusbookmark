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
    h.head.css_url('counter.css')

    with h.div(class_='counter'):
        h << h.a('-').action(self.decrement)
        h << h.span(' | ', class_='separator')
        h << h.span(self.value, class_='value')
        h << h.span(' | ', class_='separator')
        h << h.a('+').action(self.increment)

    return h.root
