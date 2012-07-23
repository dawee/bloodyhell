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

from box2d.dynamics.joints.b2joint import b2Joint
from box2d.dynamics.joints.b2jointnode import b2JointNode
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2mat22 import b2Mat22
from box2d.common.math.b2math import b2Math
from box2d.common.b2settings import b2Settings


class b2MouseJoint(b2Joint):

    def GetAnchor1(self):
        return self.m_target

    def GetAnchor2(self):
        tVec = b2Math.b2MulMV(self.m_body2.m_R, self.m_localAnchor)
        tVec.Add(self.m_body2.m_position)
        return tVec

    def GetReactionForce(self,invTimeStep):
        F = b2Vec2()
        F.SetV(self.m_impulse)
        F.Multiply(invTimeStep)
        return F

    def GetReactionTorque(self,invTimeStep):
        return 0.0

    def SetTarget(self,target):
        self.m_body2.WakeUp()
        self.m_target = target

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
        self.K = b2Mat22()
        self.K1 = b2Mat22()
        self.K2 = b2Mat22()
        self.m_localAnchor = b2Vec2()
        self.m_target = b2Vec2()
        self.m_impulse = b2Vec2()
        self.m_ptpMass = b2Mat22()
        self.m_C = b2Vec2()
        self.m_target.SetV(definition.target)
        tX = self.m_target.x - self.m_body2.m_position.x
        tY = self.m_target.y - self.m_body2.m_position.y
        self.m_localAnchor.x = (tX * self.m_body2.m_R.col1.x + tY * self.m_body2.m_R.col1.y)
        self.m_localAnchor.y = (tX * self.m_body2.m_R.col2.x + tY * self.m_body2.m_R.col2.y)
        self.m_maxForce = definition.maxForce
        self.m_impulse.SetZero()
        mass = self.m_body2.m_mass
        omega = 2.0 * b2Settings.b2_pi * definition.frequencyHz
        d = 2.0 * mass * definition.dampingRatio * omega
        k = mass * omega * omega
        self.m_gamma = 1.0 / (d + definition.timeStep * k)
        self.m_beta = definition.timeStep * k / (d + definition.timeStep * k)

    def PrepareVelocitySolver(self):
        b = self.m_body2
        tMat = b.m_R
        rX = tMat.col1.x * self.m_localAnchor.x + tMat.col2.x * self.m_localAnchor.y
        rY = tMat.col1.y * self.m_localAnchor.x + tMat.col2.y * self.m_localAnchor.y
        invMass = b.m_invMass
        invI = b.m_invI
        self.K1.col1.x = invMass
        self.K1.col2.x = 0.0
        self.K1.col1.y = 0.0
        self.K1.col2.y = invMass
        self.K2.col1.x =  invI * rY * rY
        self.K2.col2.x = -invI * rX * rY
        self.K2.col1.y = -invI * rX * rY
        self.K2.col2.y =  invI * rX * rX
        self.K.SetM(self.K1)
        self.K.AddM(self.K2)
        self.K.col1.x += self.m_gamma
        self.K.col2.y += self.m_gamma
        self.K.Invert(self.m_ptpMass)
        self.m_C.x = b.m_position.x + rX - self.m_target.x
        self.m_C.y = b.m_position.y + rY - self.m_target.y
        b.m_angularVelocity *= 0.98
        PX = self.m_impulse.x
        PY = self.m_impulse.y
        b.m_linearVelocity.x += invMass * PX
        b.m_linearVelocity.y += invMass * PY
        b.m_angularVelocity += invI * (rX * PY - rY * PX)

    def SolveVelocityConstraints(self,step):
        body = self.m_body2
        tMat = body.m_R
        rX = tMat.col1.x * self.m_localAnchor.x + tMat.col2.x * self.m_localAnchor.y
        rY = tMat.col1.y * self.m_localAnchor.x + tMat.col2.y * self.m_localAnchor.y
        CdotX = body.m_linearVelocity.x + (-body.m_angularVelocity * rY)
        CdotY = body.m_linearVelocity.y + (body.m_angularVelocity * rX)
        tMat = self.m_ptpMass
        tX = CdotX + (self.m_beta * step.inv_dt) * self.m_C.x + self.m_gamma * self.m_impulse.x
        tY = CdotY + (self.m_beta * step.inv_dt) * self.m_C.y + self.m_gamma * self.m_impulse.y
        impulseX = -(tMat.col1.x * tX + tMat.col2.x * tY)
        impulseY = -(tMat.col1.y * tX + tMat.col2.y * tY)
        oldImpulseX = self.m_impulse.x
        oldImpulseY = self.m_impulse.y
        self.m_impulse.x += impulseX
        self.m_impulse.y += impulseY
        length = self.m_impulse.Length()
        if (length > step.dt * self.m_maxForce):
            self.m_impulse.Multiply(step.dt * self.m_maxForce / length)
        impulseX = self.m_impulse.x - oldImpulseX
        impulseY = self.m_impulse.y - oldImpulseY
        body.m_linearVelocity.x += body.m_invMass * impulseX
        body.m_linearVelocity.y += body.m_invMass * impulseY
        body.m_angularVelocity += body.m_invI * (rX * impulseY - rY * impulseX)

    def SolvePositionConstraints(self):
        return True
