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


class b2RevoluteJoint(object):
        """
        inherit from "b2Joint"
        """
Object.extend(b2RevoluteJoint.prototype, 

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

    def GetJointAngle(self):
        """
        TO FILL
        """
        return self.m_body2.m_rotation - self.m_body1.m_rotation

    def GetJointSpeed(self):
        """
        TO FILL
        """
        return self.m_body2.m_angularVelocity - self.m_body1.m_angularVelocity

    def GetMotorTorque(self,invTimeStep):
        """
        TO FILL
        """
        return  invTimeStep * self.m_motorImpulse

    def SetMotorSpeed(self,speed):
        """
        TO FILL
        """
        self.m_motorSpeed = speed

    def SetMotorTorque(self,torque):
        """
        TO FILL
        """
        self.m_maxMotorTorque = torque

    def GetReactionForce(self,invTimeStep):
        """
        TO FILL
        """
        tVec = self.m_ptpImpulse.Copy()
        tVec.Multiply(invTimeStep)
        return tVec

    def GetReactionTorque(self,invTimeStep):
        """
        TO FILL
        """
        return invTimeStep * self.m_limitImpulse

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
        self.K = new b2Mat22()
        self.K1 = new b2Mat22()
        self.K2 = new b2Mat22()
        self.K3 = new b2Mat22()
        self.m_localAnchor1 = new b2Vec2()
        self.m_localAnchor2 = new b2Vec2()
        self.m_ptpImpulse = new b2Vec2()
        self.m_ptpMass = new b2Mat22()
        tMat
        tX
        tY
        tMat = self.m_body1.m_R
        tX = def.anchorPoint.x - self.m_body1.m_position.x
        tY = def.anchorPoint.y - self.m_body1.m_position.y
        self.m_localAnchor1.x = tX * tMat.col1.x + tY * tMat.col1.y
        self.m_localAnchor1.y = tX * tMat.col2.x + tY * tMat.col2.y
        tMat = self.m_body2.m_R
        tX = def.anchorPoint.x - self.m_body2.m_position.x
        tY = def.anchorPoint.y - self.m_body2.m_position.y
        self.m_localAnchor2.x = tX * tMat.col1.x + tY * tMat.col1.y
        self.m_localAnchor2.y = tX * tMat.col2.x + tY * tMat.col2.y
        self.m_intialAngle = self.m_body2.m_rotation - self.m_body1.m_rotation
        self.m_ptpImpulse.Set(0.0, 0.0)
        self.m_motorImpulse = 0.0
        self.m_limitImpulse = 0.0
        self.m_limitPositionImpulse = 0.0
        self.m_lowerAngle = def.lowerAngle
        self.m_upperAngle = def.upperAngle
        self.m_maxMotorTorque = def.motorTorque
        self.m_motorSpeed = def.motorSpeed
        self.m_enableLimit = def.enableLimit
        self.m_enableMotor = def.enableMotor
    K: new b2Mat22(),
    K1: new b2Mat22(),
    K2: new b2Mat22(),
    K3: new b2Mat22(),

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
        self.K1.col1.x = invMass1 + invMass2    self.K1.col2.x = 0.0
        self.K1.col1.y = 0.0                    self.K1.col2.y = invMass1 + invMass2
        self.K2.col1.x =  invI1 * r1Y * r1Y    self.K2.col2.x = -invI1 * r1X * r1Y
        self.K2.col1.y = -invI1 * r1X * r1Y    self.K2.col2.y =  invI1 * r1X * r1X
        self.K3.col1.x =  invI2 * r2Y * r2Y    self.K3.col2.x = -invI2 * r2X * r2Y
        self.K3.col1.y = -invI2 * r2X * r2Y    self.K3.col2.y =  invI2 * r2X * r2X
        self.K.SetM(self.K1)
        self.K.AddM(self.K2)
        self.K.AddM(self.K3)
        self.K.Invert(self.m_ptpMass)
        self.m_motorMass = 1.0 / (invI1 + invI2)
        if (self.m_enableMotor == false):
            self.m_motorImpulse = 0.0
        if (self.m_enableLimit):
            jointAngle = b2.m_rotation - b1.m_rotation - self.m_intialAngle
            if (b2Math.b2Abs(self.m_upperAngle - self.m_lowerAngle) < 2.0 * b2Settings.b2_angularSlop):
                self.m_limitState = b2Joint.e_equalLimits
            else if (jointAngle <= self.m_lowerAngle)
                if (self.m_limitState != b2Joint.e_atLowerLimit):
                    self.m_limitImpulse = 0.0
                self.m_limitState = b2Joint.e_atLowerLimit
            else if (jointAngle >= self.m_upperAngle)
                if (self.m_limitState != b2Joint.e_atUpperLimit):
                    self.m_limitImpulse = 0.0
                self.m_limitState = b2Joint.e_atUpperLimit
            else
                self.m_limitState = b2Joint.e_inactiveLimit
                self.m_limitImpulse = 0.0
        else
            self.m_limitImpulse = 0.0
        if (b2World.s_enableWarmStarting):
            b1.m_linearVelocity.x -= invMass1 * self.m_ptpImpulse.x
            b1.m_linearVelocity.y -= invMass1 * self.m_ptpImpulse.y
            b1.m_angularVelocity -= invI1 * ((r1X * self.m_ptpImpulse.y - r1Y * self.m_ptpImpulse.x) + self.m_motorImpulse + self.m_limitImpulse)
            b2.m_linearVelocity.x += invMass2 * self.m_ptpImpulse.x
            b2.m_linearVelocity.y += invMass2 * self.m_ptpImpulse.y
            b2.m_angularVelocity += invI2 * ((r2X * self.m_ptpImpulse.y - r2Y * self.m_ptpImpulse.x) + self.m_motorImpulse + self.m_limitImpulse)
        else
            self.m_ptpImpulse.SetZero()
            self.m_motorImpulse = 0.0
            self.m_limitImpulse = 0.0
        self.m_limitPositionImpulse = 0.0

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
        oldLimitImpulse
        ptpCdotX = b2.m_linearVelocity.x + (-b2.m_angularVelocity * r2Y) - b1.m_linearVelocity.x - (-b1.m_angularVelocity * r1Y)
        ptpCdotY = b2.m_linearVelocity.y + (b2.m_angularVelocity * r2X) - b1.m_linearVelocity.y - (b1.m_angularVelocity * r1X)
        ptpImpulseX = -(self.m_ptpMass.col1.x * ptpCdotX + self.m_ptpMass.col2.x * ptpCdotY)
        ptpImpulseY = -(self.m_ptpMass.col1.y * ptpCdotX + self.m_ptpMass.col2.y * ptpCdotY)
        self.m_ptpImpulse.x += ptpImpulseX
        self.m_ptpImpulse.y += ptpImpulseY
        b1.m_linearVelocity.x -= b1.m_invMass * ptpImpulseX
        b1.m_linearVelocity.y -= b1.m_invMass * ptpImpulseY
        b1.m_angularVelocity -= b1.m_invI * (r1X * ptpImpulseY - r1Y * ptpImpulseX)
        b2.m_linearVelocity.x += b2.m_invMass * ptpImpulseX
        b2.m_linearVelocity.y += b2.m_invMass * ptpImpulseY
        b2.m_angularVelocity += b2.m_invI * (r2X * ptpImpulseY - r2Y * ptpImpulseX)
        if (self.m_enableMotor and self.m_limitState != b2Joint.e_equalLimits):
            motorCdot = b2.m_angularVelocity - b1.m_angularVelocity - self.m_motorSpeed
            motorImpulse = -self.m_motorMass * motorCdot
            oldMotorImpulse = self.m_motorImpulse
            self.m_motorImpulse = b2Math.b2Clamp(self.m_motorImpulse + motorImpulse, -step.dt * self.m_maxMotorTorque, step.dt * self.m_maxMotorTorque)
            motorImpulse = self.m_motorImpulse - oldMotorImpulse
            b1.m_angularVelocity -= b1.m_invI * motorImpulse
            b2.m_angularVelocity += b2.m_invI * motorImpulse
        if (self.m_enableLimit and self.m_limitState != b2Joint.e_inactiveLimit):
            limitCdot = b2.m_angularVelocity - b1.m_angularVelocity
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
            b1.m_angularVelocity -= b1.m_invI * limitImpulse
            b2.m_angularVelocity += b2.m_invI * limitImpulse

    def SolvePositionConstraints(self):
        """
        TO FILL
        """
        oldLimitImpulse
        limitC
        b1 = self.m_body1
        b2 = self.m_body2
        positionError = 0.0
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
        ptpCX = p2X - p1X
        ptpCY = p2Y - p1Y
        positionError = Math.sqrt(ptpCX*ptpCX + ptpCY*ptpCY)
        invMass1 = b1.m_invMass
        invMass2 = b2.m_invMass
        invI1 = b1.m_invI
        invI2 = b2.m_invI
        self.K1.col1.x = invMass1 + invMass2    self.K1.col2.x = 0.0
        self.K1.col1.y = 0.0                    self.K1.col2.y = invMass1 + invMass2
        self.K2.col1.x =  invI1 * r1Y * r1Y    self.K2.col2.x = -invI1 * r1X * r1Y
        self.K2.col1.y = -invI1 * r1X * r1Y    self.K2.col2.y =  invI1 * r1X * r1X
        self.K3.col1.x =  invI2 * r2Y * r2Y        self.K3.col2.x = -invI2 * r2X * r2Y
        self.K3.col1.y = -invI2 * r2X * r2Y        self.K3.col2.y =  invI2 * r2X * r2X
        self.K.SetM(self.K1)
        self.K.AddM(self.K2)
        self.K.AddM(self.K3)
        self.K.Solve(b2RevoluteJoint.tImpulse, -ptpCX, -ptpCY)
        impulseX = b2RevoluteJoint.tImpulse.x
        impulseY = b2RevoluteJoint.tImpulse.y
        b1.m_position.x -= b1.m_invMass * impulseX
        b1.m_position.y -= b1.m_invMass * impulseY
        b1.m_rotation -= b1.m_invI * (r1X * impulseY - r1Y * impulseX)
        b1.m_R.Set(b1.m_rotation)
        b2.m_position.x += b2.m_invMass * impulseX
        b2.m_position.y += b2.m_invMass * impulseY
        b2.m_rotation += b2.m_invI * (r2X * impulseY - r2Y * impulseX)
        b2.m_R.Set(b2.m_rotation)
        angularError = 0.0
        if (self.m_enableLimit and self.m_limitState != b2Joint.e_inactiveLimit):
            angle = b2.m_rotation - b1.m_rotation - self.m_intialAngle
            limitImpulse = 0.0
            if (self.m_limitState == b2Joint.e_equalLimits):
                limitC = b2Math.b2Clamp(angle, -b2Settings.b2_maxAngularCorrection, b2Settings.b2_maxAngularCorrection)
                limitImpulse = -self.m_motorMass * limitC
                angularError = b2Math.b2Abs(limitC)
            else if (self.m_limitState == b2Joint.e_atLowerLimit)
                limitC = angle - self.m_lowerAngle
                angularError = b2Math.b2Max(0.0, -limitC)
                limitC = b2Math.b2Clamp(limitC + b2Settings.b2_angularSlop, -b2Settings.b2_maxAngularCorrection, 0.0)
                limitImpulse = -self.m_motorMass * limitC
                oldLimitImpulse = self.m_limitPositionImpulse
                self.m_limitPositionImpulse = b2Math.b2Max(self.m_limitPositionImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitPositionImpulse - oldLimitImpulse
            else if (self.m_limitState == b2Joint.e_atUpperLimit)
                limitC = angle - self.m_upperAngle
                angularError = b2Math.b2Max(0.0, limitC)
                limitC = b2Math.b2Clamp(limitC - b2Settings.b2_angularSlop, 0.0, b2Settings.b2_maxAngularCorrection)
                limitImpulse = -self.m_motorMass * limitC
                oldLimitImpulse = self.m_limitPositionImpulse
                self.m_limitPositionImpulse = b2Math.b2Min(self.m_limitPositionImpulse + limitImpulse, 0.0)
                limitImpulse = self.m_limitPositionImpulse - oldLimitImpulse
            b1.m_rotation -= b1.m_invI * limitImpulse
            b1.m_R.Set(b1.m_rotation)
            b2.m_rotation += b2.m_invI * limitImpulse
            b2.m_R.Set(b2.m_rotation)
        return positionError <= b2Settings.b2_linearSlop and angularError <= b2Settings.b2_angularSlop
    m_localAnchor1: new b2Vec2(),
    m_localAnchor2: new b2Vec2(),
    m_ptpImpulse: new b2Vec2(),
    m_motorImpulse: null,
    m_limitImpulse: null,
    m_limitPositionImpulse: null,
    m_ptpMass: new b2Mat22(),
    m_motorMass: null,
    m_intialAngle: null,
    m_lowerAngle: null,
    m_upperAngle: null,
    m_maxMotorTorque: null,
    m_motorSpeed: null,
    m_enableLimit: null,
    m_enableMotor: null,
    m_limitState: 0)
b2RevoluteJoint.tImpulse = new b2Vec2()
