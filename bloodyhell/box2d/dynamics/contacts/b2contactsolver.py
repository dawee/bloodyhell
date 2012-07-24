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

from box2d.dynamics.contacts.b2contactconstraint import b2ContactConstraint
from box2d.common.b2settings import b2Settings
from box2d.common.math.b2math import b2Math


class b2ContactSolver(object):

    def __init__(self,contacts, contactCount, allocator):
        self.m_constraints = []
        self.m_allocator = allocator
        i = 0
        self.m_constraintCount = 0
        for i in range(contactCount):
            self.m_constraintCount += contacts[i].GetManifoldCount()
        for i in range(self.m_constraintCount):
            self.m_constraints.append(b2ContactConstraint())
        count = 0
        for i in range(contactCount):
            contact = contacts[i]
            b1 = contact.m_shape1.m_body
            b2 = contact.m_shape2.m_body
            manifoldCount = contact.GetManifoldCount()
            manifolds = contact.GetManifolds()
            friction = contact.m_friction
            restitution = contact.m_restitution
            v1X = b1.m_linearVelocity.x
            v1Y = b1.m_linearVelocity.y
            v2X = b2.m_linearVelocity.x
            v2Y = b2.m_linearVelocity.y
            w1 = b1.m_angularVelocity
            w2 = b2.m_angularVelocity
            for j in range(manifoldCount):
                manifold = manifolds[ j ]
                normalX = manifold.normal.x
                normalY = manifold.normal.y
                c = self.m_constraints[ count ]
                c.body1 = b1
                c.body2 = b2
                c.manifold = manifold
                c.normal.x = normalX
                c.normal.y = normalY
                c.pointCount = manifold.pointCount
                c.friction = friction
                c.restitution = restitution
                for k in range(c.pointCount):
                    cp = manifold.points[ k ]
                    ccp = c.points[ k ]
                    ccp.normalImpulse = cp.normalImpulse
                    ccp.tangentImpulse = cp.tangentImpulse
                    ccp.separation = cp.separation
                    r1X = cp.position.x - b1.m_position.x
                    r1Y = cp.position.y - b1.m_position.y
                    r2X = cp.position.x - b2.m_position.x
                    r2Y = cp.position.y - b2.m_position.y
                    tVec = ccp.localAnchor1
                    tMat = b1.m_R
                    tVec.x = r1X * tMat.col1.x + r1Y * tMat.col1.y
                    tVec.y = r1X * tMat.col2.x + r1Y * tMat.col2.y
                    tVec = ccp.localAnchor2
                    tMat = b2.m_R
                    tVec.x = r2X * tMat.col1.x + r2Y * tMat.col1.y
                    tVec.y = r2X * tMat.col2.x + r2Y * tMat.col2.y
                    r1Sqr = r1X * r1X + r1Y * r1Y
                    r2Sqr = r2X * r2X + r2Y * r2Y
                    rn1 = r1X*normalX + r1Y*normalY
                    rn2 = r2X*normalX + r2Y*normalY
                    kNormal = b1.m_invMass + b2.m_invMass
                    kNormal += b1.m_invI * (r1Sqr - rn1 * rn1) + b2.m_invI * (r2Sqr - rn2 * rn2)
                    ccp.normalMass = 1.0 / kNormal
                    tangentX = normalY
                    tangentY = -normalX
                    rt1 = r1X*tangentX + r1Y*tangentY
                    rt2 = r2X*tangentX + r2Y*tangentY
                    kTangent = b1.m_invMass + b2.m_invMass
                    kTangent += b1.m_invI * (r1Sqr - rt1 * rt1) + b2.m_invI * (r2Sqr - rt2 * rt2)
                    ccp.tangentMass = 1.0 /  kTangent
                    ccp.velocityBias = 0.0
                    if (ccp.separation > 0.0):
                        ccp.velocityBias = -60.0 * ccp.separation
                    tX = v2X + (-w2*r2Y) - v1X - (-w1*r1Y)
                    tY = v2Y + (w2*r2X) - v1Y - (w1*r1X)
                    vRel = c.normal.x*tX + c.normal.y*tY
                    if (vRel < -b2Settings.b2_velocityThreshold):
                        ccp.velocityBias += -c.restitution * vRel
                count += 1

    def PreSolve(self):
        for i in range(self.m_constraintCount):
            c = self.m_constraints[ i ]
            b1 = c.body1
            b2 = c.body2
            invMass1 = b1.m_invMass
            invI1 = b1.m_invI
            invMass2 = b2.m_invMass
            invI2 = b2.m_invI
            normalX = c.normal.x
            normalY = c.normal.y
            tangentX = normalY
            tangentY = -normalX
            j = 0
            tCount = 0
            from box2d.dynamics.b2world import b2World
            if (b2World.s_enableWarmStarting):
                tCount = c.pointCount
                for j in range(tCount):
                    ccp = c.points[ j ]
                    PX = ccp.normalImpulse*normalX + ccp.tangentImpulse*tangentX
                    PY = ccp.normalImpulse*normalY + ccp.tangentImpulse*tangentY
                    tMat = b1.m_R
                    tVec = ccp.localAnchor1
                    r1X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                    r1Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                    tMat = b2.m_R
                    tVec = ccp.localAnchor2
                    r2X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                    r2Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                    b1.m_angularVelocity -= invI1 * (r1X * PY - r1Y * PX)
                    b1.m_linearVelocity.x -= invMass1 * PX
                    b1.m_linearVelocity.y -= invMass1 * PY
                    b2.m_angularVelocity += invI2 * (r2X * PY - r2Y * PX)
                    b2.m_linearVelocity.x += invMass2 * PX
                    b2.m_linearVelocity.y += invMass2 * PY
                    ccp.positionImpulse = 0.0
            else:
                tCount = c.pointCount
                for j in range(tCount):
                    ccp2 = c.points[ j ]
                    ccp2.normalImpulse = 0.0
                    ccp2.tangentImpulse = 0.0
                    ccp2.positionImpulse = 0.0

    def SolveVelocityConstraints(self):
        for i in range(self.m_constraintCount):
            c = self.m_constraints[ i ]
            b1 = c.body1
            b2 = c.body2
            b1_angularVelocity = b1.m_angularVelocity
            b1_linearVelocity = b1.m_linearVelocity
            b2_angularVelocity = b2.m_angularVelocity
            b2_linearVelocity = b2.m_linearVelocity
            invMass1 = b1.m_invMass
            invI1 = b1.m_invI
            invMass2 = b2.m_invMass
            invI2 = b2.m_invI
            normalX = c.normal.x
            normalY = c.normal.y
            tangentX = normalY
            tangentY = -normalX
            tCount = c.pointCount
            for j in range(tCount):
                ccp = c.points[ j ]
                tMat = b1.m_R
                tVec = ccp.localAnchor1
                r1X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                r1Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                tMat = b2.m_R
                tVec = ccp.localAnchor2
                r2X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                r2Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                dvX = b2_linearVelocity.x + (-b2_angularVelocity * r2Y) - b1_linearVelocity.x - (-b1_angularVelocity * r1Y)
                dvY = b2_linearVelocity.y + (b2_angularVelocity * r2X) - b1_linearVelocity.y - (b1_angularVelocity * r1X)
                vn = dvX * normalX + dvY * normalY
                mLambda = -ccp.normalMass * (vn - ccp.velocityBias)
                newImpulse = b2Math.b2Max(ccp.normalImpulse + mLambda, 0.0)
                mLambda = newImpulse - ccp.normalImpulse
                PX = mLambda * normalX
                PY = mLambda * normalY
                b1_linearVelocity.x -= invMass1 * PX
                b1_linearVelocity.y -= invMass1 * PY
                b1_angularVelocity -= invI1 * (r1X * PY - r1Y * PX)
                b2_linearVelocity.x += invMass2 * PX
                b2_linearVelocity.y += invMass2 * PY
                b2_angularVelocity += invI2 * (r2X * PY - r2Y * PX)
                ccp.normalImpulse = newImpulse
                dvX = b2_linearVelocity.x + (-b2_angularVelocity * r2Y) - b1_linearVelocity.x - (-b1_angularVelocity * r1Y)
                dvY = b2_linearVelocity.y + (b2_angularVelocity * r2X) - b1_linearVelocity.y - (b1_angularVelocity * r1X)
                vt = dvX*tangentX + dvY*tangentY
                mLambda = ccp.tangentMass * (-vt)
                maxFriction = c.friction * ccp.normalImpulse
                newImpulse = b2Math.b2Clamp(ccp.tangentImpulse + mLambda, -maxFriction, maxFriction)
                mLambda = newImpulse - ccp.tangentImpulse
                PX = mLambda * tangentX
                PY = mLambda * tangentY
                b1_linearVelocity.x -= invMass1 * PX
                b1_linearVelocity.y -= invMass1 * PY
                b1_angularVelocity -= invI1 * (r1X * PY - r1Y * PX)
                b2_linearVelocity.x += invMass2 * PX
                b2_linearVelocity.y += invMass2 * PY
                b2_angularVelocity += invI2 * (r2X * PY - r2Y * PX)
                ccp.tangentImpulse = newImpulse
            b1.m_angularVelocity = b1_angularVelocity
            b2.m_angularVelocity = b2_angularVelocity

    def SolvePositionConstraints(self,beta):
        minSeparation = 0.0
        for i in range(self.m_constraintCount):
            c = self.m_constraints[ i ]
            b1 = c.body1
            b2 = c.body2
            b1_position = b1.m_position
            b1_rotation = b1.m_rotation
            b2_position = b2.m_position
            b2_rotation = b2.m_rotation
            invMass1 = b1.m_invMass
            invI1 = b1.m_invI
            invMass2 = b2.m_invMass
            invI2 = b2.m_invI
            normalX = c.normal.x
            normalY = c.normal.y
            # tangentX = normalY
            # tangentY = -normalX
            tCount = c.pointCount
            for j in range(tCount):
                ccp = c.points[ j ]
                tMat = b1.m_R
                tVec = ccp.localAnchor1
                r1X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                r1Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                tMat = b2.m_R
                tVec = ccp.localAnchor2
                r2X = tMat.col1.x * tVec.x + tMat.col2.x * tVec.y
                r2Y = tMat.col1.y * tVec.x + tMat.col2.y * tVec.y
                p1X = b1_position.x + r1X
                p1Y = b1_position.y + r1Y
                p2X = b2_position.x + r2X
                p2Y = b2_position.y + r2Y
                dpX = p2X - p1X
                dpY = p2Y - p1Y
                separation = (dpX*normalX + dpY*normalY) + ccp.separation
                minSeparation = b2Math.b2Min(minSeparation, separation)
                C = beta * b2Math.b2Clamp(separation + b2Settings.b2_linearSlop, -b2Settings.b2_maxLinearCorrection, 0.0)
                dImpulse = -ccp.normalMass * C
                impulse0 = ccp.positionImpulse
                ccp.positionImpulse = b2Math.b2Max(impulse0 + dImpulse, 0.0)
                dImpulse = ccp.positionImpulse - impulse0
                impulseX = dImpulse * normalX
                impulseY = dImpulse * normalY
                b1_position.x -= invMass1 * impulseX
                b1_position.y -= invMass1 * impulseY
                b1_rotation -= invI1 * (r1X * impulseY - r1Y * impulseX)
                b1.m_R.Set(b1_rotation)
                b2_position.x += invMass2 * impulseX
                b2_position.y += invMass2 * impulseY
                b2_rotation += invI2 * (r2X * impulseY - r2Y * impulseX)
                b2.m_R.Set(b2_rotation)
            b1.m_rotation = b1_rotation
            b2.m_rotation = b2_rotation
        return minSeparation >= -b2Settings.b2_linearSlop

    def PostSolve(self):
        for i in range(self.m_constraintCount):
            c = self.m_constraints[ i ]
            m = c.manifold
            for j in range(c.pointCount):
                mPoint = m.points[j]
                cPoint = c.points[j]
                mPoint.normalImpulse = cPoint.normalImpulse
                mPoint.tangentImpulse = cPoint.tangentImpulse
