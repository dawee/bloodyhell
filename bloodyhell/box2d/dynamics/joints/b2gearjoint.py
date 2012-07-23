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


class b2GearJoint(object):
        """
        inherit from "b2Joint"
        """
Object.extend(b2GearJoint.prototype, 

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
        self.m_J = new b2Jacobian()
        self.m_revolute1 = null
        self.m_prismatic1 = null
        self.m_revolute2 = null
        self.m_prismatic2 = null
        coordinate1
        coordinate2
        self.m_ground1 = def.joint1.m_body1
        self.m_body1 = def.joint1.m_body2
        if (def.joint1.m_type == b2Joint.e_revoluteJoint):
            self.m_revolute1 = def.joint1
            self.m_groundAnchor1.SetV( self.m_revolute1.m_localAnchor1 )
            self.m_localAnchor1.SetV( self.m_revolute1.m_localAnchor2 )
            coordinate1 = self.m_revolute1.GetJointAngle()
        else
            self.m_prismatic1 = def.joint1
            self.m_groundAnchor1.SetV( self.m_prismatic1.m_localAnchor1 )
            self.m_localAnchor1.SetV( self.m_prismatic1.m_localAnchor2 )
            coordinate1 = self.m_prismatic1.GetJointTranslation()
        self.m_ground2 = def.joint2.m_body1
        self.m_body2 = def.joint2.m_body2
        if (def.joint2.m_type == b2Joint.e_revoluteJoint):
            self.m_revolute2 = def.joint2
            self.m_groundAnchor2.SetV( self.m_revolute2.m_localAnchor1 )
            self.m_localAnchor2.SetV( self.m_revolute2.m_localAnchor2 )
            coordinate2 = self.m_revolute2.GetJointAngle()
        else
            self.m_prismatic2 = def.joint2
            self.m_groundAnchor2.SetV( self.m_prismatic2.m_localAnchor1 )
            self.m_localAnchor2.SetV( self.m_prismatic2.m_localAnchor2 )
            coordinate2 = self.m_prismatic2.GetJointTranslation()
        self.m_ratio = def.ratio
        self.m_constant = coordinate1 + self.m_ratio * coordinate2
        self.m_impulse = 0.0

    def PrepareVelocitySolver(self):
        """
        TO FILL
        """
        g1 = self.m_ground1
        g2 = self.m_ground2
        b1 = self.m_body1
        b2 = self.m_body2
        ugX
        ugY
        rX
        rY
        tMat
        tVec
        crug
        K = 0.0
        self.m_J.SetZero()
        if (self.m_revolute1):
            self.m_J.angular1 = -1.0
            K += b1.m_invI
        else
            tMat = g1.m_R
            tVec = self.m_prismatic1.m_localXAxis1
            ugX = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
            ugY = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
            tMat = b1.m_R
            rX = tMat.col1.x * self.m_localAnchor1.x + tMat.col2.x * self.m_localAnchor1.y
            rY = tMat.col1.y * self.m_localAnchor1.x + tMat.col2.y * self.m_localAnchor1.y
            crug = rX * ugY - rY * ugX
            self.m_J.linear1.Set(-ugX, -ugY)
            self.m_J.angular1 = -crug
            K += b1.m_invMass + b1.m_invI * crug * crug
        if (self.m_revolute2):
            self.m_J.angular2 = -self.m_ratio
            K += self.m_ratio * self.m_ratio * b2.m_invI
        else
            tMat = g2.m_R
            tVec = self.m_prismatic2.m_localXAxis1
            ugX = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
            ugY = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
            tMat = b2.m_R
            rX = tMat.col1.x * self.m_localAnchor2.x + tMat.col2.x * self.m_localAnchor2.y
            rY = tMat.col1.y * self.m_localAnchor2.x + tMat.col2.y * self.m_localAnchor2.y
            crug = rX * ugY - rY * ugX
            self.m_J.linear2.Set(-self.m_ratio*ugX, -self.m_ratio*ugY)
            self.m_J.angular2 = -self.m_ratio * crug
            K += self.m_ratio * self.m_ratio * (b2.m_invMass + b2.m_invI * crug * crug)
        self.m_mass = 1.0 / K
        b1.m_linearVelocity.x += b1.m_invMass * self.m_impulse * self.m_J.linear1.x
        b1.m_linearVelocity.y += b1.m_invMass * self.m_impulse * self.m_J.linear1.y
        b1.m_angularVelocity += b1.m_invI * self.m_impulse * self.m_J.angular1
        b2.m_linearVelocity.x += b2.m_invMass * self.m_impulse * self.m_J.linear2.x
        b2.m_linearVelocity.y += b2.m_invMass * self.m_impulse * self.m_J.linear2.y
        b2.m_angularVelocity += b2.m_invI * self.m_impulse * self.m_J.angular2

    def SolveVelocityConstraints(self,step):
        """
        TO FILL
        """
        b1 = self.m_body1
        b2 = self.m_body2
        Cdot = self.m_J.Compute(    b1.m_linearVelocity, b1.m_angularVelocity,
                                        b2.m_linearVelocity, b2.m_angularVelocity)
        impulse = -self.m_mass * Cdot
        self.m_impulse += impulse
        b1.m_linearVelocity.x += b1.m_invMass * impulse * self.m_J.linear1.x
        b1.m_linearVelocity.y += b1.m_invMass * impulse * self.m_J.linear1.y
        b1.m_angularVelocity  += b1.m_invI * impulse * self.m_J.angular1
        b2.m_linearVelocity.x += b2.m_invMass * impulse * self.m_J.linear2.x
        b2.m_linearVelocity.y += b2.m_invMass * impulse * self.m_J.linear2.y
        b2.m_angularVelocity  += b2.m_invI * impulse * self.m_J.angular2

    def SolvePositionConstraints(self):
        """
        TO FILL
        """
        linearError = 0.0
        b1 = self.m_body1
        b2 = self.m_body2
        coordinate1
        coordinate2
        if (self.m_revolute1):
            coordinate1 = self.m_revolute1.GetJointAngle()
        else
            coordinate1 = self.m_prismatic1.GetJointTranslation()
        if (self.m_revolute2):
            coordinate2 = self.m_revolute2.GetJointAngle()
        else
            coordinate2 = self.m_prismatic2.GetJointTranslation()
        C = self.m_constant - (coordinate1 + self.m_ratio * coordinate2)
        impulse = -self.m_mass * C
        b1.m_position.x += b1.m_invMass * impulse * self.m_J.linear1.x
        b1.m_position.y += b1.m_invMass * impulse * self.m_J.linear1.y
        b1.m_rotation += b1.m_invI * impulse * self.m_J.angular1
        b2.m_position.x += b2.m_invMass * impulse * self.m_J.linear2.x
        b2.m_position.y += b2.m_invMass * impulse * self.m_J.linear2.y
        b2.m_rotation += b2.m_invI * impulse * self.m_J.angular2
        b1.m_R.Set(b1.m_rotation)
        b2.m_R.Set(b2.m_rotation)
        return linearError < b2Settings.b2_linearSlop
    m_ground1: null,
    m_ground2: null,
    m_revolute1: null,
    m_prismatic1: null,
    m_revolute2: null,
    m_prismatic2: null,
    m_groundAnchor1: new b2Vec2(),
    m_groundAnchor2: new b2Vec2(),
    m_localAnchor1: new b2Vec2(),
    m_localAnchor2: new b2Vec2(),
    m_J: new b2Jacobian(),
    m_constant: null,
    m_ratio: null,
    m_mass: null,
    m_impulse: null)
