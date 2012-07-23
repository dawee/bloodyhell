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
from box2d.common.b2settings import b2Settings
from box2d.common.math import b2Math
from box2d.collision.shapes.b2shape import b2Shape


class b2ShapeDef(object):

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

    def ComputeMass(self, massData):
        massData.center = b2Vec2(0.0, 0.0)
        if (self.density == 0.0):
            massData.mass = 0.0
            massData.center.Set(0.0, 0.0)
            massData.I = 0.0
        if self.type == b2Shape.e_circleShape:
            circle = self
            massData.mass = self.density * b2Settings.b2_pi * circle.radius * circle.radius
            massData.center.Set(0.0, 0.0)
            massData.I = 0.5 * (massData.mass) * circle.radius * circle.radius
        elif self.type == b2Shape.e_boxShape:
            box = self
            massData.mass = 4.0 * self.density * box.extents.x * box.extents.y
            massData.center.Set(0.0, 0.0)
            massData.I = massData.mass / 3.0 * b2Math.b2Dot(box.extents, box.extents)
        elif self.type == b2Shape.e_polyShape:
            poly = self
            b2Shape.PolyMass(massData, poly.vertices, poly.vertexCount, self.density)
        else:
            massData.mass = 0.0
            massData.center.Set(0.0, 0.0)
            massData.I = 0.0
