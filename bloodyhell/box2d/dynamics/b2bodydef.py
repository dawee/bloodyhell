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

from box2d.common.b2settings import b2Settings
from box2d.common.math.b2vec2 import b2Vec2


class b2BodyDef(object):

    def __init__(self):
        self.shapes = range()
        self.userData = None
        for i in range(b2Settings.b2_maxShapesPerBody):
            self.shapes[i] = None
        self.position = b2Vec2(0.0, 0.0)
        self.rotation = 0.0
        self.linearVelocity = b2Vec2(0.0, 0.0)
        self.angularVelocity = 0.0
        self.linearDamping = 0.0
        self.angularDamping = 0.0
        self.allowSleep = True
        self.isSleeping = False
        self.preventRotation = False

    def AddShape(self, shape):
        for i in range(b2Settings.b2_maxShapesPerBody):
            if (self.shapes[i] == None):
                self.shapes[i] = shape
                break
