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

import math

from box2d.collision.b2pair import b2Pair
from box2d.collision.b2aabb import b2AABB
from box2d.collision.shapes.b2shape import b2Shape
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2math import b2Math
from box2d.common.math.b2mat22 import b2Mat22


class b2CircleShape(b2Shape):

    m_localPosition = b2Vec2()
    m_radius = None

    def TestPoint(self, p):
        d = b2Vec2()
        d.SetV(p)
        d.Subtract(self.m_position)
        return b2Math.b2Dot(d, d) <= self.m_radius * self.m_radius

    def __init__(self, definition, body, localCenter):
        self.m_R = b2Mat22()
        self.m_position = b2Vec2()
        self.m_userData = definition.userData
        self.m_friction = definition.friction
        self.m_restitution = definition.restitution
        self.m_body = body
        self.m_proxyId = b2Pair.b2_nullProxy
        self.m_maxRadius = 0.0
        self.m_categoryBits = definition.categoryBits
        self.m_maskBits = definition.maskBits
        self.m_groupIndex = definition.groupIndex
        self.m_localPosition = b2Vec2()
        circle = definition
        self.m_localPosition.Set(
            definition.localPosition.x - localCenter.x,
            definition.localPosition.y - localCenter.y
        )
        self.m_type = b2Shape.e_circleShape
        self.m_radius = circle.radius
        self.m_R.SetM(self.m_body.m_R)
        rX = self.m_R.col1.x * self.m_localPosition.x + self.m_R.col2.x * self.m_localPosition.y
        rY = self.m_R.col1.y * self.m_localPosition.x + self.m_R.col2.y * self.m_localPosition.y
        self.m_position.x = self.m_body.m_position.x + rX
        self.m_position.y = self.m_body.m_position.y + rY
        self.m_maxRadius = math.sqrt(rX*rX+rY*rY) + self.m_radius
        aabb = b2AABB()
        aabb.minVertex.Set(self.m_position.x - self.m_radius, self.m_position.y - self.m_radius)
        aabb.maxVertex.Set(self.m_position.x + self.m_radius, self.m_position.y + self.m_radius)
        broadPhase = self.m_body.m_world.m_broadPhase
        if (broadPhase.InRange(aabb)):
            self.m_proxyId = broadPhase.CreateProxy(aabb, self)
        else:
            self.m_proxyId = b2Pair.b2_nullProxy
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            self.m_body.Freeze()

    def Synchronize(self,position1, R1, position2, R2):
        self.m_R.SetM(R2)
        self.m_position.x = (R2.col1.x * self.m_localPosition.x + R2.col2.x * self.m_localPosition.y) + position2.x
        self.m_position.y = (R2.col1.y * self.m_localPosition.x + R2.col2.y * self.m_localPosition.y) + position2.y
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            return
        p1X = position1.x + (R1.col1.x * self.m_localPosition.x + R1.col2.x * self.m_localPosition.y)
        p1Y = position1.y + (R1.col1.y * self.m_localPosition.x + R1.col2.y * self.m_localPosition.y)
        lowerX = min(p1X, self.m_position.x)
        lowerY = min(p1Y, self.m_position.y)
        upperX = max(p1X, self.m_position.x)
        upperY = max(p1Y, self.m_position.y)
        aabb = b2AABB()
        aabb.minVertex.Set(lowerX - self.m_radius, lowerY - self.m_radius)
        aabb.maxVertex.Set(upperX + self.m_radius, upperY + self.m_radius)
        broadPhase = self.m_body.m_world.m_broadPhase
        if (broadPhase.InRange(aabb)):
            broadPhase.MoveProxy(self.m_proxyId, aabb)
        else:
            self.m_body.Freeze()

    def QuickSync(self,position, R):
        self.m_R.SetM(R)
        self.m_position.x = (R.col1.x * self.m_localPosition.x + R.col2.x * self.m_localPosition.y) + position.x
        self.m_position.y = (R.col1.y * self.m_localPosition.x + R.col2.y * self.m_localPosition.y) + position.y

    def ResetProxy(self,broadPhase):
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            return
        # proxy = broadPhase.GetProxy(self.m_proxyId)
        broadPhase.DestroyProxy(self.m_proxyId)
        # proxy = None
        aabb = b2AABB()
        aabb.minVertex.Set(self.m_position.x - self.m_radius, self.m_position.y - self.m_radius)
        aabb.maxVertex.Set(self.m_position.x + self.m_radius, self.m_position.y + self.m_radius)
        if (broadPhase.InRange(aabb)):
            self.m_proxyId = broadPhase.CreateProxy(aabb, self)
        else:
            self.m_proxyId = b2Pair.b2_nullProxy
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            self.m_body.Freeze()

    def Support(self,dX, dY, out):
        length = math.sqrt(dX*dX + dY*dY)
        dX /= length
        dY /= length
        out.Set(    self.m_position.x + self.m_radius*dX,
                    self.m_position.y + self.m_radius*dY)
