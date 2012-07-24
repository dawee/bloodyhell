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

from box2d.common.math.b2mat22 import b2Mat22
from box2d.common.math.b2math import b2Math
from box2d.common.math.b2vec2 import b2Vec2
from box2d.collision.b2pair import b2Pair


class b2Shape(object):

    e_unknownShape = -1
    e_circleShape = 0
    e_boxShape = 1
    e_polyShape = 2
    e_meshShape = 3
    e_shapeTypeCount = 4

    def TestPoint(self, p):
        return False

    def GetUserData(self):
        return self.m_userData

    def GetType(self):
        return self.m_type

    def GetBody(self):
        return self.m_body

    def GetPosition(self):
        return self.m_position

    def GetRotationMatrix(self):
        return self.m_R

    def ResetProxy(self,broadPhase):
        pass

    def GetNext(self):
        return self.m_next

    def __init__(self, definition, body):
        self.m_R = b2Mat22()
        self.m_position = b2Vec2()
        self.m_userData = definition.userData
        self.m_friction = definition.friction
        self.m_restitution = definition.restitution
        self.m_body = body
        self.m_proxyId = b2Pair.b2_NoneProxy
        self.m_maxRadius = 0.0
        self.m_categoryBits = definition.categoryBits
        self.m_maskBits = definition.maskBits
        self.m_groupIndex = definition.groupIndex

    def DestroyProxy(self):
        if (self.m_proxyId != b2Pair.b2_NoneProxy):
            self.m_body.m_world.m_broadPhase.DestroyProxy(self.m_proxyId)
            self.m_proxyId = b2Pair.b2_NoneProxy

    def Synchronize(self,position1, R1, position2, R2):
        pass

    def QuickSync(self, position, R):
        pass

    def Support(self, dX, dY, out):
        pass

    def GetMaxRadius(self):
        return self.m_maxRadius

    @staticmethod
    def Create(definition, body, center):
        from box2d.collision.shapes.b2circleshape import b2CircleShape
        from box2d.collision.shapes.b2polyshape import b2PolyShape
        if definition.type == b2Shape.e_circleShape:
            return b2CircleShape(definition, body, center)
        if definition.type in [b2Shape.e_polyShape, b2Shape.e_boxShape]:
            return b2PolyShape(definition, body, center)
        return None

    @staticmethod
    def Destroy(shape):
        if (shape.m_proxyId != b2Pair.b2_NoneProxy):
            shape.m_body.m_world.m_broadPhase.DestroyProxy(shape.m_proxyId)

    @staticmethod
    def PolyMass(massData, vs, count, rho):
        center = b2Vec2()
        center.SetZero()
        area = 0.0
        I = 0.0
        pRef = b2Vec2(0.0, 0.0)
        inv3 = 1.0 / 3.0
        for i in range(count):
            p1 = pRef
            p2 = vs[i]
            p3 = vs[i+1] if i + 1 < count else vs[0]
            e1 = b2Math.SubtractVV(p2, p1)
            e2 = b2Math.SubtractVV(p3, p1)
            D = b2Math.b2CrossVV(e1, e2)
            triangleArea = 0.5 * D
            area += triangleArea
            tVec = b2Vec2()
            tVec.SetV(p1)
            tVec.Add(p2)
            tVec.Add(p3)
            tVec.Multiply(inv3*triangleArea)
            center.Add(tVec)
            px = p1.x
            py = p1.y
            ex1 = e1.x
            ey1 = e1.y
            ex2 = e2.x
            ey2 = e2.y
            intx2 = inv3 * (0.25 * (ex1*ex1 + ex2*ex1 + ex2*ex2) + (px*ex1 + px*ex2)) + 0.5*px*px
            inty2 = inv3 * (0.25 * (ey1*ey1 + ey2*ey1 + ey2*ey2) + (py*ey1 + py*ey2)) + 0.5*py*py
            I += D * (intx2 + inty2)
        massData.mass = rho * area
        center.Multiply( 1.0 / area )
        massData.center = center
        I = rho * (I - area * b2Math.b2Dot(center, center))
        massData.I = I

    @staticmethod
    def PolyCentroid(vs, count, out):
        cX = 0.0
        cY = 0.0
        area = 0.0
        pRefX = 0.0
        pRefY = 0.0
        inv3 = 1.0 / 3.0
        for i in range(count):
            p1X = pRefX
            p1Y = pRefY
            p2X = vs[i].x
            p2Y = vs[i].y
            p3X = vs[i+1].x if i + 1 < count else vs[0].x
            p3Y = vs[i+1].y if i + 1 < count else vs[0].y
            e1X = p2X - p1X
            e1Y = p2Y - p1Y
            e2X = p3X - p1X
            e2Y = p3Y - p1Y
            D = (e1X * e2Y - e1Y * e2X)
            triangleArea = 0.5 * D
            area += triangleArea
            cX += triangleArea * inv3 * (p1X + p2X + p3X)
            cY += triangleArea * inv3 * (p1Y + p2Y + p3Y)
        cX *= 1.0 / area
        cY *= 1.0 / area
        out.Set(cX, cY)
