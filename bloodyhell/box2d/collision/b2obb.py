"""
* Copyright (c) 2006-2007 Erin Catto http:
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of self software.
* Permission is granted to anyone to use self software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
* 1. The origin of self software must not be misrepresented you must not
* claim that you wrote the original software. If you use self software
* in a product, an acknowledgment in the product documentation would be
* appreciated but is not required.
* 2. Altered source versions must be plainly marked, and must not be
* misrepresented the original software.
* 3. This notice may not be removed or altered from any source distribution.
"""

from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2mat22 import b2Mat22


class b2OBB(object):
    R = b2Mat22()
    center = b2Vec2()
    extents = b2Vec2()

    def __init__(self):
        self.R = b2Mat22()
        self.center = b2Vec2()
        self.extents = b2Vec2()
