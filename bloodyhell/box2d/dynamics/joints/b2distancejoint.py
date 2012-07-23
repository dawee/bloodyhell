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

from box2d.dynamics.joints.b2joint import b2Joint
from box2d.dynamics.joints.b2jointnode import b2JointNode
from box2d.dynamics.b2world import b2World
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2math import b2Math
from box2d.common.b2settings import b2Settings


class b2DistanceJoint(b2Joint):

    def __init__(self, definition):
        self.m_node1 = b2JointNode()
        self.m_node2 = b2JointNode()
        self.m_type = definition.type
        self.m_prev = None
        self.m_next = None
        self.m_body1 = definition.body1
        self.m_body2 = definition.body2
        self.m_collideConnected = definition.collideConnected
        self.m_islandFlag = False
        self.m_userData = definition.userData
        self.m_localAnchor1 = b2Vec2()
        self.m_localAnchor2 = b2Vec2()
        self.m_u = b2Vec2()
        tMat = self.m_body1.m_R
        tX = definition.anchorPoint1.x - self.m_body1.m_position.x
        tY = definition.anchorPoint1.y - self.m_body1.m_position.y
        self.m_localAnchor1.x = tX*tMat.col1.x + tY*tMat.col1.y
        self.m_localAnchor1.y = tX*tMat.col2.x + tY*tMat.col2.y
        tMat = self.m_body2.m_R
        tX = definition.anchorPoint2.x - self.m_body2.m_position.x
        tY = definition.anchorPoint2.y - self.m_body2.m_position.y
        self.m_localAnchor2.x = tX*tMat.col1.x + tY*tMat.col1.y
        self.m_localAnchor2.y = tX*tMat.col2.x + tY*tMat.col2.y
        tX = definition.anchorPoint2.x - definition.anchorPoint1.x
        tY = definition.anchorPoint2.y - definition.anchorPoint1.y
        self.m_length = math.sqrt(tX*tX + tY*tY)
        self.m_impulse = 0.0

    def PrepareVelocitySolver(self):
        tMat = self.m_body1.m_R
        r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
        r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
        tMat = self.m_body2.m_R
        r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
        r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
        self.m_u.x = self.m_body2.m_position.x + r2X - self.m_body1.m_position.x - r1X
        self.m_u.y = self.m_body2.m_position.y + r2Y - self.m_body1.m_position.y - r1Y
        length = math.sqrt(self.m_u.x*self.m_u.x + self.m_u.y*self.m_u.y)
        if (length > b2Settings.b2_linearSlop):
            self.m_u.Multiply( 1.0 / length )
        else:
            self.m_u.SetZero()
        cr1u = (r1X * self.m_u.y - r1Y * self.m_u.x)
        cr2u = (r2X * self.m_u.y - r2Y * self.m_u.x)
        self.m_mass = self.m_body1.m_invMass + self.m_body1.m_invI * cr1u * cr1u + self.m_body2.m_invMass + self.m_body2.m_invI * cr2u * cr2u
        self.m_mass = 1.0 / self.m_mass
        if (b2World.s_enableWarmStarting):
            PX = self.m_impulse * self.m_u.x
            PY = self.m_impulse * self.m_u.y
            self.m_body1.m_linearVelocity.x -= self.m_body1.m_invMass * PX
            self.m_body1.m_linearVelocity.y -= self.m_body1.m_invMass * PY
            self.m_body1.m_angularVelocity -= self.m_body1.m_invI * (r1X * PY - r1Y * PX)
            self.m_body2.m_linearVelocity.x += self.m_body2.m_invMass * PX
            self.m_body2.m_linearVelocity.y += self.m_body2.m_invMass * PY
            self.m_body2.m_angularVelocity += self.m_body2.m_invI * (r2X * PY - r2Y * PX)
        else:
            self.m_impulse = 0.0

    def SolveVelocityConstraints(self,step):
        tMat = self.m_body1.m_R
        r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
        r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
        tMat = self.m_body2.m_R
        r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
        r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
        v1X = self.m_body1.m_linearVelocity.x + (-self.m_body1.m_angularVelocity * r1Y)
        v1Y = self.m_body1.m_linearVelocity.y + (self.m_body1.m_angularVelocity * r1X)
        v2X = self.m_body2.m_linearVelocity.x + (-self.m_body2.m_angularVelocity * r2Y)
        v2Y = self.m_body2.m_linearVelocity.y + (self.m_body2.m_angularVelocity * r2X)
        Cdot = (self.m_u.x * (v2X - v1X) + self.m_u.y * (v2Y - v1Y))
        impulse = -self.m_mass * Cdot
        self.m_impulse += impulse
        PX = impulse * self.m_u.x
        PY = impulse * self.m_u.y
        self.m_body1.m_linearVelocity.x -= self.m_body1.m_invMass * PX
        self.m_body1.m_linearVelocity.y -= self.m_body1.m_invMass * PY
        self.m_body1.m_angularVelocity -= self.m_body1.m_invI * (r1X * PY - r1Y * PX)
        self.m_body2.m_linearVelocity.x += self.m_body2.m_invMass * PX
        self.m_body2.m_linearVelocity.y += self.m_body2.m_invMass * PY
        self.m_body2.m_angularVelocity += self.m_body2.m_invI * (r2X * PY - r2Y * PX)

    def SolvePositionConstraints(self):
        tMat = self.m_body1.m_R
        r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
        r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
        tMat = self.m_body2.m_R
        r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
        r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
        dX = self.m_body2.m_position.x + r2X - self.m_body1.m_position.x - r1X
        dY = self.m_body2.m_position.y + r2Y - self.m_body1.m_position.y - r1Y
        length = math.sqrt(dX*dX + dY*dY)
        dX /= length
        dY /= length
        C = length - self.m_length
        C = b2Math.b2Clamp(C, -b2Settings.b2_maxLinearCorrection, b2Settings.b2_maxLinearCorrection)
        impulse = -self.m_mass * C
        self.m_u.Set(dX, dY)
        PX = impulse * self.m_u.x
        PY = impulse * self.m_u.y
        self.m_body1.m_position.x -= self.m_body1.m_invMass * PX
        self.m_body1.m_position.y -= self.m_body1.m_invMass * PY
        self.m_body1.m_rotation -= self.m_body1.m_invI * (r1X * PY - r1Y * PX)
        self.m_body2.m_position.x += self.m_body2.m_invMass * PX
        self.m_body2.m_position.y += self.m_body2.m_invMass * PY
        self.m_body2.m_rotation += self.m_body2.m_invI * (r2X * PY - r2Y * PX)
        self.m_body1.m_R.Set(self.m_body1.m_rotation)
        self.m_body2.m_R.Set(self.m_body2.m_rotation)
        return b2Math.b2Abs(C) < b2Settings.b2_linearSlop

    def GetAnchor1(self):
        return b2Math.AddVV(self.m_body1.m_position , b2Math.b2MulMV(self.m_body1.m_R, self.m_localAnchor1))

    def GetAnchor2(self):
        return b2Math.AddVV(self.m_body2.m_position , b2Math.b2MulMV(self.m_body2.m_R, self.m_localAnchor2))

    def GetReactionForce(self,invTimeStep):
        F = b2Vec2()
        F.SetV(self.m_u)
        F.Multiply(self.m_impulse * invTimeStep)
        return F

    def GetReactionTorque(self,invTimeStep):
        return 0.0
