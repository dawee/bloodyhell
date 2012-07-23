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


class b2PrismaticJoint(object):
        """
        inherit from "b2Joint"
        """
Object.extend(b2PrismaticJoint.prototype, 

    def GetAnchor1(self):
        """
        TO FILL
        """
        b1 = self.m_body1
        tVec = new b2Vec2()
        tVec.SetV(self.m_localAnchor1)
        tVec.MulM(b1.m_R)
        tVec.Add(b1.m_position)
        return tVec

    def GetAnchor2(self):
        """
        TO FILL
        """
        b2 = self.m_body2
        tVec = new b2Vec2()
        tVec.SetV(self.m_localAnchor2)
        tVec.MulM(b2.m_R)
        tVec.Add(b2.m_position)
        return tVec

    def GetJointTranslation(self):
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
        dX = p2X - p1X
        dY = p2Y - p1Y
        tMat = b1.m_R
        ax1X = tMat.col1.x * self.m_localXAxis1.x + tMat.col2.x * self.m_localXAxis1.y
        ax1Y = tMat.col1.y * self.m_localXAxis1.x + tMat.col2.y * self.m_localXAxis1.y
        translation = ax1X*dX + ax1Y*dY
        return translation

    def GetJointSpeed(self):
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
        dX = p2X - p1X
        dY = p2Y - p1Y
        tMat = b1.m_R
        ax1X = tMat.col1.x * self.m_localXAxis1.x + tMat.col2.x * self.m_localXAxis1.y
        ax1Y = tMat.col1.y * self.m_localXAxis1.x + tMat.col2.y * self.m_localXAxis1.y
        v1 = b1.m_linearVelocity
        v2 = b2.m_linearVelocity
        w1 = b1.m_angularVelocity
        w2 = b2.m_angularVelocity
        speed = (dX*(-w1 * ax1Y) + dY*(w1 * ax1X)) + (ax1X * ((( v2.x + (-w2 * r2Y)) - v1.x) - (-w1 * r1Y)) + ax1Y * ((( v2.y + (w2 * r2X)) - v1.y) - (w1 * r1X)))
        return speed

    def GetMotorForce(self,invTimeStep):
        """
        TO FILL
        """
        return invTimeStep * self.m_motorImpulse

    def SetMotorSpeed(self,speed):
        """
        TO FILL
        """
        self.m_motorSpeed = speed

    def SetMotorForce(self,force):
        """
        TO FILL
        """
        self.m_maxMotorForce = force

    def GetReactionForce(self,invTimeStep):
        """
        TO FILL
        """
        tImp = invTimeStep * self.m_limitImpulse
        tMat
        tMat = self.m_body1.m_R
        ax1X = tImp * (tMat.col1.x * self.m_localXAxis1.x + tMat.col2.x * self.m_localXAxis1.y)
        ax1Y = tImp * (tMat.col1.y * self.m_localXAxis1.x + tMat.col2.y * self.m_localXAxis1.y)
        ay1X = tImp * (tMat.col1.x * self.m_localYAxis1.x + tMat.col2.x * self.m_localYAxis1.y)
        ay1Y = tImp * (tMat.col1.y * self.m_localYAxis1.x + tMat.col2.y * self.m_localYAxis1.y)
        return new b2Vec2(ax1X+ay1X, ax1Y+ay1Y)

    def GetReactionTorque(self,invTimeStep):
        """
        TO FILL
        """
        return invTimeStep * self.m_angularImpulse

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
        self.m_localAnchor1 = new b2Vec2()
        self.m_localAnchor2 = new b2Vec2()
        self.m_localXAxis1 = new b2Vec2()
        self.m_localYAxis1 = new b2Vec2()
        self.m_linearJacobian = new b2Jacobian()
        self.m_motorJacobian = new b2Jacobian()
        tMat
        tX
        tY
        tMat = self.m_body1.m_R
        tX = (def.anchorPoint.x - self.m_body1.m_position.x)
        tY = (def.anchorPoint.y - self.m_body1.m_position.y)
        self.m_localAnchor1.Set((tX*tMat.col1.x + tY*tMat.col1.y), (tX*tMat.col2.x + tY*tMat.col2.y))
        tMat = self.m_body2.m_R
        tX = (def.anchorPoint.x - self.m_body2.m_position.x)
        tY = (def.anchorPoint.y - self.m_body2.m_position.y)
        self.m_localAnchor2.Set((tX*tMat.col1.x + tY*tMat.col1.y), (tX*tMat.col2.x + tY*tMat.col2.y))
        tMat = self.m_body1.m_R
        tX = def.axis.x
        tY = def.axis.y
        self.m_localXAxis1.Set((tX*tMat.col1.x + tY*tMat.col1.y), (tX*tMat.col2.x + tY*tMat.col2.y))
        self.m_localYAxis1.x = -self.m_localXAxis1.y
        self.m_localYAxis1.y = self.m_localXAxis1.x
        self.m_initialAngle = self.m_body2.m_rotation - self.m_body1.m_rotation
        self.m_linearJacobian.SetZero()
        self.m_linearMass = 0.0
        self.m_linearImpulse = 0.0
        self.m_angularMass = 0.0
        self.m_angularImpulse = 0.0
        self.m_motorJacobian.SetZero()
        self.m_motorMass = 0.0
        self.m_motorImpulse = 0.0
        self.m_limitImpulse = 0.0
        self.m_limitPositionImpulse = 0.0
        self.m_lowerTranslation = def.lowerTranslation
        self.m_upperTranslation = def.upperTranslation
        self.m_maxMotorForce = def.motorForce
        self.m_motorSpeed = def.motorSpeed
        self.m_enableLimit = def.enableLimit
        self.m_enableMotor = def.enableMotor

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
        invMass1 = b1.m_invMass
        invMass2 = b2.m_invMass
        invI1 = b1.m_invI
        invI2 = b2.m_invI
        tMat = b1.m_R
        ay1X = tMat.col1.x * self.m_localYAxis1.x + tMat.col2.x * self.m_localYAxis1.y
        ay1Y = tMat.col1.y * self.m_localYAxis1.x + tMat.col2.y * self.m_localYAxis1.y
        eX = b2.m_position.x + r2X - b1.m_position.x
        eY = b2.m_position.y + r2Y - b1.m_position.y
        self.m_linearJacobian.linear1.x = -ay1X
        self.m_linearJacobian.linear1.y = -ay1Y
        self.m_linearJacobian.linear2.x = ay1X
        self.m_linearJacobian.linear2.y = ay1Y
        self.m_linearJacobian.angular1 = -(eX * ay1Y - eY * ay1X)
        self.m_linearJacobian.angular2 = r2X * ay1Y - r2Y * ay1X
        self.m_linearMass =    invMass1 + invI1 * self.m_linearJacobian.angular1 * self.m_linearJacobian.angular1 +
                        invMass2 + invI2 * self.m_linearJacobian.angular2 * self.m_linearJacobian.angular2
        self.m_linearMass = 1.0 / self.m_linearMass
        self.m_angularMass = 1.0 / (invI1 + invI2)
        if (self.m_enableLimit or self.m_enableMotor):
            tMat = b1.m_R
            ax1X = tMat.col1.x * self.m_localXAxis1.x + tMat.col2.x * self.m_localXAxis1.y
            ax1Y = tMat.col1.y * self.m_localXAxis1.x + tMat.col2.y * self.m_localXAxis1.y
            self.m_motorJacobian.linear1.x = -ax1X self.m_motorJacobian.linear1.y = -ax1Y
            self.m_motorJacobian.linear2.x = ax1X self.m_motorJacobian.linear2.y = ax1Y
            self.m_motorJacobian.angular1 = -(eX * ax1Y - eY * ax1X)
            self.m_motorJacobian.angular2 = r2X * ax1Y - r2Y * ax1X
            self.m_motorMass =    invMass1 + invI1 * self.m_motorJacobian.angular1 * self.m_motorJacobian.angular1 +
                            invMass2 + invI2 * self.m_motorJacobian.angular2 * self.m_motorJacobian.angular2
            self.m_motorMass = 1.0 / self.m_motorMass
            if (self.m_enableLimit):
                dX = eX - r1X
                dY = eY - r1Y
                jointTranslation = ax1X * dX + ax1Y * dY
                if (b2Math.b2Abs(self.m_upperTranslation - self.m_lowerTranslation) < 2.0 * b2Settings.b2_linearSlop):
                    self.m_limitState = b2Joint.e_equalLimits
                else if (jointTranslation <= self.m_lowerTranslation)
                    if (self.m_limitState != b2Joint.e_atLowerLimit):
                        self.m_limitImpulse = 0.0
                    self.m_limitState = b2Joint.e_atLowerLimit
                else if (jointTranslation >= self.m_upperTranslation)
                    if (self.m_limitState != b2Joint.e_atUpperLimit):
                        self.m_limitImpulse = 0.0
                    self.m_limitState = b2Joint.e_atUpperLimit
                else
                    self.m_limitState = b2Joint.e_inactiveLimit
                    self.m_limitImpulse = 0.0
        if (self.m_enableMotor == false):
            self.m_motorImpulse = 0.0
        if (self.m_enableLimit == false):
            self.m_limitImpulse = 0.0
        if (b2World.s_enableWarmStarting):
            P1X = self.m_linearImpulse * self.m_linearJacobian.linear1.x + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.linear1.x
            P1Y = self.m_linearImpulse * self.m_linearJacobian.linear1.y + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.linear1.y
            P2X = self.m_linearImpulse * self.m_linearJacobian.linear2.x + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.linear2.x
            P2Y = self.m_linearImpulse * self.m_linearJacobian.linear2.y + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.linear2.y
            L1 = self.m_linearImpulse * self.m_linearJacobian.angular1 - self.m_angularImpulse + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.angular1
            L2 = self.m_linearImpulse * self.m_linearJacobian.angular2 + self.m_angularImpulse + (self.m_motorImpulse + self.m_limitImpulse) * self.m_motorJacobian.angular2
            b1.m_linearVelocity.x += invMass1 * P1X
            b1.m_linearVelocity.y += invMass1 * P1Y
            b1.m_angularVelocity += invI1 * L1
            b2.m_linearVelocity.x += invMass2 * P2X
            b2.m_linearVelocity.y += invMass2 * P2Y
            b2.m_angularVelocity += invI2 * L2
        else
            self.m_linearImpulse = 0.0
            self.m_angularImpulse = 0.0
            self.m_limitImpulse = 0.0
            self.m_motorImpulse = 0.0
        self.m_limitPositionImpulse = 0.0

    def SolveVelocityConstraints(self,step):
        """
        TO FILL
        """
        b1 = self.m_body1
        b2 = self.m_body2
        invMass1 = b1.m_invMass
        invMass2 = b2.m_invMass
        invI1 = b1.m_invI
        invI2 = b2.m_invI
        oldLimitImpulse
        linearCdot = self.m_linearJacobian.Compute(b1.m_linearVelocity, b1.m_angularVelocity, b2.m_linearVelocity, b2.m_angularVelocity)
        linearImpulse = -self.m_linearMass * linearCdot
        self.m_linearImpulse += linearImpulse
        b1.m_linearVelocity.x += (invMass1 * linearImpulse) * self.m_linearJacobian.linear1.x
        b1.m_linearVelocity.y += (invMass1 * linearImpulse) * self.m_linearJacobian.linear1.y
        b1.m_angularVelocity += invI1 * linearImpulse * self.m_linearJacobian.angular1
        b2.m_linearVelocity.x += (invMass2 * linearImpulse) * self.m_linearJacobian.linear2.x
        b2.m_linearVelocity.y += (invMass2 * linearImpulse) * self.m_linearJacobian.linear2.y
        b2.m_angularVelocity += invI2 * linearImpulse * self.m_linearJacobian.angular2
        angularCdot = b2.m_angularVelocity - b1.m_angularVelocity
        angularImpulse = -self.m_angularMass * angularCdot
        self.m_angularImpulse += angularImpulse
        b1.m_angularVelocity -= invI1 * angularImpulse
        b2.m_angularVelocity += invI2 * angularImpulse
        if (self.m_enableMotor and self.m_limitState != b2Joint.e_equalLimits):
            motorCdot = self.m_motorJacobian.Compute(b1.m_linearVelocity, b1.m_angularVelocity, b2.m_linearVelocity, b2.m_angularVelocity) - self.m_motorSpeed
            motorImpulse = -self.m_motorMass * motorCdot
            oldMotorImpulse = self.m_motorImpulse
            self.m_motorImpulse = b2Math.b2Clamp(self.m_motorImpulse + motorImpulse, -step.dt * self.m_maxMotorForce, step.dt * self.m_maxMotorForce)
            motorImpulse = self.m_motorImpulse - oldMotorImpulse
            b1.m_linearVelocity.x += (invMass1 * motorImpulse) * self.m_motorJacobian.linear1.x
            b1.m_linearVelocity.y += (invMass1 * motorImpulse) * self.m_motorJacobian.linear1.y
            b1.m_angularVelocity += invI1 * motorImpulse * self.m_motorJacobian.angular1
            b2.m_linearVelocity.x += (invMass2 * motorImpulse) * self.m_motorJacobian.linear2.x
            b2.m_linearVelocity.y += (invMass2 * motorImpulse) * self.m_motorJacobian.linear2.y
            b2.m_angularVelocity += invI2 * motorImpulse * self.m_motorJacobian.angular2
        if (self.m_enableLimit and self.m_limitState != b2Joint.e_inactiveLimit):
            limitCdot = self.m_motorJacobian.Compute(b1.m_linearVelocity, b1.m_angularVelocity, b2.m_linearVelocity, b2.m_angularVelocity)
            limitImpulse = -self.m_motorMass * limitCdot
            if (self.m_limitState == b2Joint.e_equalLimits):
                self.m_limitImpulse += limitImpulse
            else if (self.m_limitState == b2Joint.e_atLowerLimit)
                oldLimitImpulse = self.m_limitImpulse
                self.m_limitImpulse = b2Math.b2Max(self.m_limitImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitImpulse - oldLimitImpulse
            else if (self.m_limitState == b2Joint.e_atUpperLimit)
                oldLimitImpulse = self.m_limitImpulse
                self.m_limitImpulse = b2Math.b2Min(self.m_limitImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitImpulse - oldLimitImpulse
            b1.m_linearVelocity.x += (invMass1 * limitImpulse) * self.m_motorJacobian.linear1.x
            b1.m_linearVelocity.y += (invMass1 * limitImpulse) * self.m_motorJacobian.linear1.y
            b1.m_angularVelocity += invI1 * limitImpulse * self.m_motorJacobian.angular1
            b2.m_linearVelocity.x += (invMass2 * limitImpulse) * self.m_motorJacobian.linear2.x
            b2.m_linearVelocity.y += (invMass2 * limitImpulse) * self.m_motorJacobian.linear2.y
            b2.m_angularVelocity += invI2 * limitImpulse * self.m_motorJacobian.angular2

    def SolvePositionConstraints(self):
        """
        TO FILL
        """
        limitC
        oldLimitImpulse
        b1 = self.m_body1
        b2 = self.m_body2
        invMass1 = b1.m_invMass
        invMass2 = b2.m_invMass
        invI1 = b1.m_invI
        invI2 = b2.m_invI
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
        dX = p2X - p1X
        dY = p2Y - p1Y
        tMat = b1.m_R
        ay1X = tMat.col1.x * self.m_localYAxis1.x + tMat.col2.x * self.m_localYAxis1.y
        ay1Y = tMat.col1.y * self.m_localYAxis1.x + tMat.col2.y * self.m_localYAxis1.y
        linearC = ay1X*dX + ay1Y*dY
        linearC = b2Math.b2Clamp(linearC, -b2Settings.b2_maxLinearCorrection, b2Settings.b2_maxLinearCorrection)
        linearImpulse = -self.m_linearMass * linearC
        b1.m_position.x += (invMass1 * linearImpulse) * self.m_linearJacobian.linear1.x
        b1.m_position.y += (invMass1 * linearImpulse) * self.m_linearJacobian.linear1.y
        b1.m_rotation += invI1 * linearImpulse * self.m_linearJacobian.angular1
        b2.m_position.x += (invMass2 * linearImpulse) * self.m_linearJacobian.linear2.x
        b2.m_position.y += (invMass2 * linearImpulse) * self.m_linearJacobian.linear2.y
        b2.m_rotation += invI2 * linearImpulse * self.m_linearJacobian.angular2
        positionError = b2Math.b2Abs(linearC)
        angularC = b2.m_rotation - b1.m_rotation - self.m_initialAngle
        angularC = b2Math.b2Clamp(angularC, -b2Settings.b2_maxAngularCorrection, b2Settings.b2_maxAngularCorrection)
        angularImpulse = -self.m_angularMass * angularC
        b1.m_rotation -= b1.m_invI * angularImpulse
        b1.m_R.Set(b1.m_rotation)
        b2.m_rotation += b2.m_invI * angularImpulse
        b2.m_R.Set(b2.m_rotation)
        angularError = b2Math.b2Abs(angularC)
        if (self.m_enableLimit and self.m_limitState != b2Joint.e_inactiveLimit):
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
            dX = p2X - p1X
            dY = p2Y - p1Y
            tMat = b1.m_R
            ax1X = tMat.col1.x * self.m_localXAxis1.x + tMat.col2.x * self.m_localXAxis1.y
            ax1Y = tMat.col1.y * self.m_localXAxis1.x + tMat.col2.y * self.m_localXAxis1.y
            translation = (ax1X*dX + ax1Y*dY)
            limitImpulse = 0.0
            if (self.m_limitState == b2Joint.e_equalLimits):
                limitC = b2Math.b2Clamp(translation, -b2Settings.b2_maxLinearCorrection, b2Settings.b2_maxLinearCorrection)
                limitImpulse = -self.m_motorMass * limitC
                positionError = b2Math.b2Max(positionError, b2Math.b2Abs(angularC))
            else if (self.m_limitState == b2Joint.e_atLowerLimit)
                limitC = translation - self.m_lowerTranslation
                positionError = b2Math.b2Max(positionError, -limitC)
                limitC = b2Math.b2Clamp(limitC + b2Settings.b2_linearSlop, -b2Settings.b2_maxLinearCorrection, 0.0)
                limitImpulse = -self.m_motorMass * limitC
                oldLimitImpulse = self.m_limitPositionImpulse
                self.m_limitPositionImpulse = b2Math.b2Max(self.m_limitPositionImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitPositionImpulse - oldLimitImpulse
            else if (self.m_limitState == b2Joint.e_atUpperLimit)
                limitC = translation - self.m_upperTranslation
                positionError = b2Math.b2Max(positionError, limitC)
                limitC = b2Math.b2Clamp(limitC - b2Settings.b2_linearSlop, 0.0, b2Settings.b2_maxLinearCorrection)
                limitImpulse = -self.m_motorMass * limitC
                oldLimitImpulse = self.m_limitPositionImpulse
                self.m_limitPositionImpulse = b2Math.b2Min(self.m_limitPositionImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitPositionImpulse - oldLimitImpulse
            b1.m_position.x += (invMass1 * limitImpulse) * self.m_motorJacobian.linear1.x
            b1.m_position.y += (invMass1 * limitImpulse) * self.m_motorJacobian.linear1.y
            b1.m_rotation += invI1 * limitImpulse * self.m_motorJacobian.angular1
            b1.m_R.Set(b1.m_rotation)
            b2.m_position.x += (invMass2 * limitImpulse) * self.m_motorJacobian.linear2.x
            b2.m_position.y += (invMass2 * limitImpulse) * self.m_motorJacobian.linear2.y
            b2.m_rotation += invI2 * limitImpulse * self.m_motorJacobian.angular2
            b2.m_R.Set(b2.m_rotation)
        return positionError <= b2Settings.b2_linearSlop and angularError <= b2Settings.b2_angularSlop
    m_localAnchor1: new b2Vec2(),
    m_localAnchor2: new b2Vec2(),
    m_localXAxis1: new b2Vec2(),
    m_localYAxis1: new b2Vec2(),
    m_initialAngle: null,
    m_linearJacobian: new b2Jacobian(),
    m_linearMass: null,
    m_linearImpulse: null,
    m_angularMass: null,
    m_angularImpulse: null,
    m_motorJacobian: new b2Jacobian(),
    m_motorMass: null,
    m_motorImpulse: null,
    m_limitImpulse: null,
    m_limitPositionImpulse: null,
    m_lowerTranslation: null,
    m_upperTranslation: null,
    m_maxMotorForce: null,
    m_motorSpeed: null,
    m_enableLimit: null,
    m_enableMotor: null,
    m_limitState: 0)
