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


class b2AABB(object):

    def IsValid(self):
        dX = self.maxVertex.x
        dY = self.maxVertex.y
        dX = self.maxVertex.x
        dY = self.maxVertex.y
        dX -= self.minVertex.x
        dY -= self.minVertex.y
        valid = dX >= 0.0 and dY >= 0.0
        valid = valid and self.minVertex.IsValid() and self.maxVertex.IsValid()
        return valid

    def __init__(self):
        self.minVertex = b2Vec2()
        self.maxVertex = b2Vec2()
