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


class b2PulleyJoint(object):
        """
        inherit from "b2Joint"
        """
Object.extend(b2PulleyJoint.prototype, 

    def GetAnchor1(self):
        """
        TO FILL
        """
        tMat = self.m_body1.m_R
        return new b2Vec2(    self.m_body1.m_position.x + (tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y),
                            self.m_body1.m_position.y + (tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y))

    def GetAnchor2(self):
        """
        TO FILL
        """
        tMat = self.m_body2.m_R
        return new b2Vec2(    self.m_body2.m_position.x + (tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y),
                            self.m_body2.m_position.y + (tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y))

    def GetGroundPoint1(self):
        """
        TO FILL
        """
        return new b2Vec2(self.m_ground.m_position.x + self.m_groundAnchor1.x, self.m_ground.m_position.y + self.m_groundAnchor1.y)

    def GetGroundPoint2(self):
        """
        TO FILL
        """
        return new b2Vec2(self.m_ground.m_position.x + self.m_groundAnchor2.x, self.m_ground.m_position.y + self.m_groundAnchor2.y)

    def GetReactionForce(self,invTimeStep):
        """
        TO FILL
        """
        return new b2Vec2()

    def GetReactionTorque(self,invTimeStep):
        """
        TO FILL
        """
        return 0.0

    def GetLength1(self):
        """
        TO FILL
        """
        tMat
        tMat = self.m_body1.m_R
        pX = self.m_body1.m_position.x + (tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y)
        pY = self.m_body1.m_position.y + (tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y)
        dX = pX - (self.m_ground.m_position.x + self.m_groundAnchor1.x)
        dY = pY - (self.m_ground.m_position.y + self.m_groundAnchor1.y)
        return Math.sqrt(dX*dX + dY*dY)

    def GetLength2(self):
        """
        TO FILL
        """
        tMat
        tMat = self.m_body2.m_R
        pX = self.m_body2.m_position.x + (tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y)
        pY = self.m_body2.m_position.y + (tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y)
        dX = pX - (self.m_ground.m_position.x + self.m_groundAnchor2.x)
        dY = pY - (self.m_ground.m_position.y + self.m_groundAnchor2.y)
        return Math.sqrt(dX*dX + dY*dY)

    def GetRatio(self):
        """
        TO FILL
        """
        return self.m_ratio

    def __init__(self,def):
        """
        TO FILL
        """
        self.m_node1 = new b2JointNode()
        self.m_node2 = new b2JointNode()
        self.m_type = def.type
        self.m_prev = null
        self.m_next = null
        self.m_body1 = def.body1
        self.m_body2 = def.body2
        self.m_collideConnected = def.collideConnected
        self.m_islandFlag = false
        self.m_userData = def.userData
        self.m_groundAnchor1 = new b2Vec2()
        self.m_groundAnchor2 = new b2Vec2()
        self.m_localAnchor1 = new b2Vec2()
        self.m_localAnchor2 = new b2Vec2()
        self.m_u1 = new b2Vec2()
        self.m_u2 = new b2Vec2()
        tMat
        tX
        tY
        self.m_ground = self.m_body1.m_world.m_groundBody
        self.m_groundAnchor1.x = def.groundPoint1.x - self.m_ground.m_position.x
        self.m_groundAnchor1.y = def.groundPoint1.y - self.m_ground.m_position.y
        self.m_groundAnchor2.x = def.groundPoint2.x - self.m_ground.m_position.x
        self.m_groundAnchor2.y = def.groundPoint2.y - self.m_ground.m_position.y
        tMat = self.m_body1.m_R
        tX = def.anchorPoint1.x - self.m_body1.m_position.x
        tY = def.anchorPoint1.y - self.m_body1.m_position.y
        self.m_localAnchor1.x = tX*tMat.col1.x + tY*tMat.col1.y
        self.m_localAnchor1.y = tX*tMat.col2.x + tY*tMat.col2.y
        tMat = self.m_body2.m_R
        tX = def.anchorPoint2.x - self.m_body2.m_position.x
        tY = def.anchorPoint2.y - self.m_body2.m_position.y
        self.m_localAnchor2.x = tX*tMat.col1.x + tY*tMat.col1.y
        self.m_localAnchor2.y = tX*tMat.col2.x + tY*tMat.col2.y
        self.m_ratio = def.ratio
        tX = def.groundPoint1.x - def.anchorPoint1.x
        tY = def.groundPoint1.y - def.anchorPoint1.y
        d1Len = Math.sqrt(tX*tX + tY*tY)
        tX = def.groundPoint2.x - def.anchorPoint2.x
        tY = def.groundPoint2.y - def.anchorPoint2.y
        d2Len = Math.sqrt(tX*tX + tY*tY)
        length1 = b2Math.b2Max(0.5 * b2PulleyJoint.b2_minPulleyLength, d1Len)
        length2 = b2Math.b2Max(0.5 * b2PulleyJoint.b2_minPulleyLength, d2Len)
        self.m_constant = length1 + self.m_ratio * length2
        self.m_maxLength1 = b2Math.b2Clamp(def.maxLength1, length1, self.m_constant - self.m_ratio * b2PulleyJoint.b2_minPulleyLength)
        self.m_maxLength2 = b2Math.b2Clamp(def.maxLength2, length2, (self.m_constant - b2PulleyJoint.b2_minPulleyLength) / self.m_ratio)
        self.m_pulleyImpulse = 0.0
        self.m_limitImpulse1 = 0.0
        self.m_limitImpulse2 = 0.0

    def PrepareVelocitySolver(self):
        """
        TO FILL
        """
        b1 = self.m_body1
        b2 = self.m_body2
        tMat
        tMat = b1.m_R
        r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
        r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
        tMat = b2.m_R
        r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
        r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
        p1X = b1.m_position.x + r1X
        p1Y = b1.m_position.y + r1Y
        p2X = b2.m_position.x + r2X
        p2Y = b2.m_position.y + r2Y
        s1X = self.m_ground.m_position.x + self.m_groundAnchor1.x
        s1Y = self.m_ground.m_position.y + self.m_groundAnchor1.y
        s2X = self.m_ground.m_position.x + self.m_groundAnchor2.x
        s2Y = self.m_ground.m_position.y + self.m_groundAnchor2.y
        self.m_u1.Set(p1X - s1X, p1Y - s1Y)
        self.m_u2.Set(p2X - s2X, p2Y - s2Y)
        length1 = self.m_u1.Length()
        length2 = self.m_u2.Length()
        if (length1 > b2Settings.b2_linearSlop):
            self.m_u1.Multiply(1.0 / length1)
        else
            self.m_u1.SetZero()
        if (length2 > b2Settings.b2_linearSlop):
            self.m_u2.Multiply(1.0 / length2)
        else
            self.m_u2.SetZero()
        if (length1 < self.m_maxLength1):
            self.m_limitState1 = b2Joint.e_inactiveLimit
            self.m_limitImpulse1 = 0.0
        else
            self.m_limitState1 = b2Joint.e_atUpperLimit
            self.m_limitPositionImpulse1 = 0.0
        if (length2 < self.m_maxLength2):
            self.m_limitState2 = b2Joint.e_inactiveLimit
            self.m_limitImpulse2 = 0.0
        else
            self.m_limitState2 = b2Joint.e_atUpperLimit
            self.m_limitPositionImpulse2 = 0.0
        cr1u1 = r1X * self.m_u1.y - r1Y * self.m_u1.x
        cr2u2 = r2X * self.m_u2.y - r2Y * self.m_u2.x
        self.m_limitMass1 = b1.m_invMass + b1.m_invI * cr1u1 * cr1u1
        self.m_limitMass2 = b2.m_invMass + b2.m_invI * cr2u2 * cr2u2
        self.m_pulleyMass = self.m_limitMass1 + self.m_ratio * self.m_ratio * self.m_limitMass2
        self.m_limitMass1 = 1.0 / self.m_limitMass1
        self.m_limitMass2 = 1.0 / self.m_limitMass2
        self.m_pulleyMass = 1.0 / self.m_pulleyMass
        P1X = (-self.m_pulleyImpulse - self.m_limitImpulse1) * self.m_u1.x
        P1Y = (-self.m_pulleyImpulse - self.m_limitImpulse1) * self.m_u1.y
        P2X = (-self.m_ratio * self.m_pulleyImpulse - self.m_limitImpulse2) * self.m_u2.x
        P2Y = (-self.m_ratio * self.m_pulleyImpulse - self.m_limitImpulse2) * self.m_u2.y
        b1.m_linearVelocity.x += b1.m_invMass * P1X
        b1.m_linearVelocity.y += b1.m_invMass * P1Y
        b1.m_angularVelocity += b1.m_invI * (r1X * P1Y - r1Y * P1X)
        b2.m_linearVelocity.x += b2.m_invMass * P2X
        b2.m_linearVelocity.y += b2.m_invMass * P2Y
        b2.m_angularVelocity += b2.m_invI * (r2X * P2Y - r2Y * P2X)

    def SolveVelocityConstraints(self,step):
        """
        TO FILL
        """
        b1 = self.m_body1
        b2 = self.m_body2
        tMat
        tMat = b1.m_R
        r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
        r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
        tMat = b2.m_R
        r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
        r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
        v1X
        v1Y
        v2X
        v2Y
        P1X
        P1Y
        P2X
        P2Y
        Cdot
        impulse
        oldLimitImpulse
            v1X = b1.m_linearVelocity.x + (-b1.m_angularVelocity * r1Y)
            v1Y = b1.m_linearVelocity.y + (b1.m_angularVelocity * r1X)
            v2X = b2.m_linearVelocity.x + (-b2.m_angularVelocity * r2Y)
            v2Y = b2.m_linearVelocity.y + (b2.m_angularVelocity * r2X)
            Cdot = -(self.m_u1.x * v1X + self.m_u1.y * v1Y) - self.m_ratio * (self.m_u2.x * v2X + self.m_u2.y * v2Y)
            impulse = -self.m_pulleyMass * Cdot
            self.m_pulleyImpulse += impulse
            P1X = -impulse * self.m_u1.x
            P1Y = -impulse * self.m_u1.y
            P2X = -self.m_ratio * impulse * self.m_u2.x
            P2Y = -self.m_ratio * impulse * self.m_u2.y
            b1.m_linearVelocity.x += b1.m_invMass * P1X
            b1.m_linearVelocity.y += b1.m_invMass * P1Y
            b1.m_angularVelocity += b1.m_invI * (r1X * P1Y - r1Y * P1X)
            b2.m_linearVelocity.x += b2.m_invMass * P2X
            b2.m_linearVelocity.y += b2.m_invMass * P2Y
            b2.m_angularVelocity += b2.m_invI * (r2X * P2Y - r2Y * P2X)
        if (self.m_limitState1 == b2Joint.e_atUpperLimit):
            v1X = b1.m_linearVelocity.x + (-b1.m_angularVelocity * r1Y)
            v1Y = b1.m_linearVelocity.y + (b1.m_angularVelocity * r1X)
            Cdot = -(self.m_u1.x * v1X + self.m_u1.y * v1Y)
            impulse = -self.m_limitMass1 * Cdot
            oldLimitImpulse = self.m_limitImpulse1
            self.m_limitImpulse1 = b2Math.b2Max(0.0, self.m_limitImpulse1 + impulse)
            impulse = self.m_limitImpulse1 - oldLimitImpulse
            P1X = -impulse * self.m_u1.x
            P1Y = -impulse * self.m_u1.y
            b1.m_linearVelocity.x += b1.m_invMass * P1X
            b1.m_linearVelocity.y += b1.m_invMass * P1Y
            b1.m_angularVelocity += b1.m_invI * (r1X * P1Y - r1Y * P1X)
        if (self.m_limitState2 == b2Joint.e_atUpperLimit):
            v2X = b2.m_linearVelocity.x + (-b2.m_angularVelocity * r2Y)
            v2Y = b2.m_linearVelocity.y + (b2.m_angularVelocity * r2X)
            Cdot = -(self.m_u2.x * v2X + self.m_u2.y * v2Y)
            impulse = -self.m_limitMass2 * Cdot
            oldLimitImpulse = self.m_limitImpulse2
            self.m_limitImpulse2 = b2Math.b2Max(0.0, self.m_limitImpulse2 + impulse)
            impulse = self.m_limitImpulse2 - oldLimitImpulse
            P2X = -impulse * self.m_u2.x
            P2Y = -impulse * self.m_u2.y
            b2.m_linearVelocity.x += b2.m_invMass * P2X
            b2.m_linearVelocity.y += b2.m_invMass * P2Y
            b2.m_angularVelocity += b2.m_invI * (r2X * P2Y - r2Y * P2X)

    def SolvePositionConstraints(self):
        """
        TO FILL
        """
        b1 = self.m_body1
        b2 = self.m_body2
        tMat
        s1X = self.m_ground.m_position.x + self.m_groundAnchor1.x
        s1Y = self.m_ground.m_position.y + self.m_groundAnchor1.y
        s2X = self.m_ground.m_position.x + self.m_groundAnchor2.x
        s2Y = self.m_ground.m_position.y + self.m_groundAnchor2.y
        r1X
        r1Y
        r2X
        r2Y
        p1X
        p1Y
        p2X
        p2Y
        length1
        length2
        C
        impulse
        oldLimitPositionImpulse
        linearError = 0.0
            tMat = b1.m_R
            r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
            r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
            tMat = b2.m_R
            r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
            r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
            p1X = b1.m_position.x + r1X
            p1Y = b1.m_position.y + r1Y
            p2X = b2.m_position.x + r2X
            p2Y = b2.m_position.y + r2Y
            self.m_u1.Set(p1X - s1X, p1Y - s1Y)
            self.m_u2.Set(p2X - s2X, p2Y - s2Y)
            length1 = self.m_u1.Length()
            length2 = self.m_u2.Length()
            if (length1 > b2Settings.b2_linearSlop):
                self.m_u1.Multiply( 1.0 / length1 )
            else
                self.m_u1.SetZero()
            if (length2 > b2Settings.b2_linearSlop):
                self.m_u2.Multiply( 1.0 / length2 )
            else
                self.m_u2.SetZero()
            C = self.m_constant - length1 - self.m_ratio * length2
            linearError = b2Math.b2Max(linearError, Math.abs(C))
            C = b2Math.b2Clamp(C, -b2Settings.b2_maxLinearCorrection, b2Settings.b2_maxLinearCorrection)
            impulse = -self.m_pulleyMass * C
            p1X = -impulse * self.m_u1.x
            p1Y = -impulse * self.m_u1.y
            p2X = -self.m_ratio * impulse * self.m_u2.x
            p2Y = -self.m_ratio * impulse * self.m_u2.y
            b1.m_position.x += b1.m_invMass * p1X
            b1.m_position.y += b1.m_invMass * p1Y
            b1.m_rotation += b1.m_invI * (r1X * p1Y - r1Y * p1X)
            b2.m_position.x += b2.m_invMass * p2X
            b2.m_position.y += b2.m_invMass * p2Y
            b2.m_rotation += b2.m_invI * (r2X * p2Y - r2Y * p2X)
            b1.m_R.Set(b1.m_rotation)
            b2.m_R.Set(b2.m_rotation)
        if (self.m_limitState1 == b2Joint.e_atUpperLimit):
            tMat = b1.m_R
            r1X = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
            r1Y = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
            p1X = b1.m_position.x + r1X
            p1Y = b1.m_position.y + r1Y
            self.m_u1.Set(p1X - s1X, p1Y - s1Y)
            length1 = self.m_u1.Length()
            if (length1 > b2Settings.b2_linearSlop):
                self.m_u1.x *= 1.0 / length1
                self.m_u1.y *= 1.0 / length1
            else
                self.m_u1.SetZero()
            C = self.m_maxLength1 - length1
            linearError = b2Math.b2Max(linearError, -C)
            C = b2Math.b2Clamp(C + b2Settings.b2_linearSlop, -b2Settings.b2_maxLinearCorrection, 0.0)
            impulse = -self.m_limitMass1 * C
            oldLimitPositionImpulse = self.m_limitPositionImpulse1
            self.m_limitPositionImpulse1 = b2Math.b2Max(0.0, self.m_limitPositionImpulse1 + impulse)
            impulse = self.m_limitPositionImpulse1 - oldLimitPositionImpulse
            p1X = -impulse * self.m_u1.x
            p1Y = -impulse * self.m_u1.y
            b1.m_position.x += b1.m_invMass * p1X
            b1.m_position.y += b1.m_invMass * p1Y
            b1.m_rotation += b1.m_invI * (r1X * p1Y - r1Y * p1X)
            b1.m_R.Set(b1.m_rotation)
        if (self.m_limitState2 == b2Joint.e_atUpperLimit):
            tMat = b2.m_R
            r2X = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
            r2Y = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
            p2X = b2.m_position.x + r2X
            p2Y = b2.m_position.y + r2Y
            self.m_u2.Set(p2X - s2X, p2Y - s2Y)
            length2 = self.m_u2.Length()
            if (length2 > b2Settings.b2_linearSlop):
                self.m_u2.x *= 1.0 / length2
                self.m_u2.y *= 1.0 / length2
            else
                self.m_u2.SetZero()
            C = self.m_maxLength2 - length2
            linearError = b2Math.b2Max(linearError, -C)
            C = b2Math.b2Clamp(C + b2Settings.b2_linearSlop, -b2Settings.b2_maxLinearCorrection, 0.0)
            impulse = -self.m_limitMass2 * C
            oldLimitPositionImpulse = self.m_limitPositionImpulse2
            self.m_limitPositionImpulse2 = b2Math.b2Max(0.0, self.m_limitPositionImpulse2 + impulse)
            impulse = self.m_limitPositionImpulse2 - oldLimitPositionImpulse
            p2X = -impulse * self.m_u2.x
            p2Y = -impulse * self.m_u2.y
            b2.m_position.x += b2.m_invMass * p2X
            b2.m_position.y += b2.m_invMass * p2Y
            b2.m_rotation += b2.m_invI * (r2X * p2Y - r2Y * p2X)
            b2.m_R.Set(b2.m_rotation)
        return linearError < b2Settings.b2_linearSlop
    m_ground: null,
    m_groundAnchor1: new b2Vec2(),
    m_groundAnchor2: new b2Vec2(),
    m_localAnchor1: new b2Vec2(),
    m_localAnchor2: new b2Vec2(),
    m_u1: new b2Vec2(),
    m_u2: new b2Vec2(),
    m_constant: null,
    m_ratio: null,
    m_maxLength1: null,
    m_maxLength2: null,
    m_pulleyMass: null,
    m_limitMass1: null,
    m_limitMass2: null,
    m_pulleyImpulse: null,
    m_limitImpulse1: null,
    m_limitImpulse2: null,
    m_limitPositionImpulse1: null,
    m_limitPositionImpulse2: null,
    m_limitState1: 0,
    m_limitState2: 0
)
b2PulleyJoint.b2_minPulleyLength = b2Settings.b2_lengthUnitsPerMeter
