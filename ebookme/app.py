# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE.txt file in this distribution for details.


from nagare import presentation


class EbookMe(object):
    pass


@presentation.render_for(EbookMe)
def render(self, h, *args):
    h << "Hello world!"

    return h.root


# ---------------------------------------------------------------
app = EbookMe
