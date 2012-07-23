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

from box2d.collision.shapes.b2shape import b2Shape
from box2d.collision.shapes.b2shapedef import b2ShapeDef
from box2d.common.math.b2vec2 import b2Vec2


class b2CircleDef(b2ShapeDef):

    radius = None

    def __init__(self):
        self.type = b2Shape.e_unknownShape
        self.userData = None
        self.localPosition = b2Vec2(0.0, 0.0)
        self.localRotation = 0.0
        self.friction = 0.2
        self.restitution = 0.0
        self.density = 0.0
        self.categoryBits = 0x0001
        self.maskBits = 0xFFFF
        self.groupIndex = 0
        self.type = b2Shape.e_circleShape
        self.radius = 1.0
