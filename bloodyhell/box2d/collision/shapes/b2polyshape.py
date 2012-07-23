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

import sys
import math

from box2d.collision.b2aabb import b2AABB
from box2d.collision.shapes.b2shape import b2Shape
from box2d.collision.b2obb import b2OBB
from box2d.collision.b2pair import b2Pair
from box2d.common.math.b2mat22 import b2Mat22
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2math import b2Math
from box2d.common.b2settings import b2Settings


class b2PolyShape(b2Shape):

    syncAABB = b2AABB()
    syncMat = b2Mat22()
    m_localCentroid = b2Vec2()
    m_localOBB = b2OBB()
    m_vertices = None
    m_coreVertices = None
    m_vertexCount = 0
    m_normals = None
    tempVec = b2Vec2()
    tAbsR = b2Mat22()

    def TestPoint(self,p):
        pLocal = b2Vec2()
        pLocal.SetV(p)
        pLocal.Subtract(self.m_position)
        pLocal.MulTM(self.m_R)
        for i in range(self.m_vertexCount):
            tVec = b2Vec2()
            tVec.SetV(pLocal)
            tVec.Subtract(self.m_vertices[i])
            dot = b2Math.b2Dot(self.m_normals[i], tVec)
            if (dot > 0.0):
                return False
        return True

    def __init__(self, definition, body, newOrigin):
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
        self.syncAABB = b2AABB()
        self.syncMat = b2Mat22()
        self.m_localCentroid = b2Vec2()
        self.m_localOBB = b2OBB()
        i = 0
        aabb = b2AABB()
        self.m_vertices = range(b2Settings.b2_maxPolyVertices)
        self.m_coreVertices = range(b2Settings.b2_maxPolyVertices)
        self.m_normals = range(b2Settings.b2_maxPolyVertices)
        self.m_type = b2Shape.e_polyShape
        localR = b2Mat22(definition.localRotation)
        if (definition.type == b2Shape.e_boxShape):
            self.m_localCentroid.x = definition.localPosition.x - newOrigin.x
            self.m_localCentroid.y = definition.localPosition.y - newOrigin.y
            box = definition
            self.m_vertexCount = 4
            hX = box.extents.x
            hY = box.extents.y
            hcX = max(0.0, hX - 2.0 * b2Settings.b2_linearSlop)
            hcY = max(0.0, hY - 2.0 * b2Settings.b2_linearSlop)
            tVec = self.m_vertices[0] = b2Vec2()
            tVec.x = localR.col1.x * hX + localR.col2.x * hY
            tVec.y = localR.col1.y * hX + localR.col2.y * hY
            tVec = self.m_vertices[1] = b2Vec2()
            tVec.x = localR.col1.x * -hX + localR.col2.x * hY
            tVec.y = localR.col1.y * -hX + localR.col2.y * hY
            tVec = self.m_vertices[2] = b2Vec2()
            tVec.x = localR.col1.x * -hX + localR.col2.x * -hY
            tVec.y = localR.col1.y * -hX + localR.col2.y * -hY
            tVec = self.m_vertices[3] = b2Vec2()
            tVec.x = localR.col1.x * hX + localR.col2.x * -hY
            tVec.y = localR.col1.y * hX + localR.col2.y * -hY
            tVec = self.m_coreVertices[0] = b2Vec2()
            tVec.x = localR.col1.x * hcX + localR.col2.x * hcY
            tVec.y = localR.col1.y * hcX + localR.col2.y * hcY
            tVec = self.m_coreVertices[1] = b2Vec2()
            tVec.x = localR.col1.x * -hcX + localR.col2.x * hcY
            tVec.y = localR.col1.y * -hcX + localR.col2.y * hcY
            tVec = self.m_coreVertices[2] = b2Vec2()
            tVec.x = localR.col1.x * -hcX + localR.col2.x * -hcY
            tVec.y = localR.col1.y * -hcX + localR.col2.y * -hcY
            tVec = self.m_coreVertices[3] = b2Vec2()
            tVec.x = localR.col1.x * hcX + localR.col2.x * -hcY
            tVec.y = localR.col1.y * hcX + localR.col2.y * -hcY
        else:
            poly = definition
            self.m_vertexCount = poly.vertexCount
            b2Shape.PolyCentroid(poly.vertices, poly.vertexCount, b2PolyShape.tempVec)
            centroidX = b2PolyShape.tempVec.x
            centroidY = b2PolyShape.tempVec.y
            self.m_localCentroid.x = definition.localPosition.x + (localR.col1.x * centroidX + localR.col2.x * centroidY) - newOrigin.x
            self.m_localCentroid.y = definition.localPosition.y + (localR.col1.y * centroidX + localR.col2.y * centroidY) - newOrigin.y
            for i in range(self.m_vertexCount):
                self.m_vertices[i] = b2Vec2()
                self.m_coreVertices[i] = b2Vec2()
                hX = poly.vertices[i].x - centroidX
                hY = poly.vertices[i].y - centroidY
                self.m_vertices[i].x = localR.col1.x * hX + localR.col2.x * hY
                self.m_vertices[i].y = localR.col1.y * hX + localR.col2.y * hY
                uX = self.m_vertices[i].x
                uY = self.m_vertices[i].y
                length = math.sqrt(uX*uX + uY*uY)
                if (length > -sys.maxint):
                    uX *= 1.0 / length
                    uY *= 1.0 / length
                self.m_coreVertices[i].x = self.m_vertices[i].x - 2.0 * b2Settings.b2_linearSlop * uX
                self.m_coreVertices[i].y = self.m_vertices[i].y - 2.0 * b2Settings.b2_linearSlop * uY
        minVertexX = sys.maxint
        minVertexY = sys.maxint
        maxVertexX = -sys.maxint
        maxVertexY = -sys.maxint
        self.m_maxRadius = 0.0
        for i in range(self.m_vertexCount):
            v = self.m_vertices[i]
            minVertexX = min(minVertexX, v.x)
            minVertexY = min(minVertexY, v.y)
            maxVertexX = max(maxVertexX, v.x)
            maxVertexY = max(maxVertexY, v.y)
            self.m_maxRadius = max(self.m_maxRadius, v.Length())
        self.m_localOBB.R.SetIdentity()
        self.m_localOBB.center.Set((minVertexX + maxVertexX) * 0.5, (minVertexY + maxVertexY) * 0.5)
        self.m_localOBB.extents.Set((maxVertexX - minVertexX) * 0.5, (maxVertexY - minVertexY) * 0.5)
        i1 = 0
        i2 = 0
        for i in range(self.m_vertexCount):
            self.m_normals[i] =  b2Vec2()
            i1 = i
            i2 = i + 1 if i + 1 < self.m_vertexCount else 0
            self.m_normals[i].x = self.m_vertices[i2].y - self.m_vertices[i1].y
            self.m_normals[i].y = -(self.m_vertices[i2].x - self.m_vertices[i1].x)
            self.m_normals[i].Normalize()
        for i in range(self.m_vertexCount):
            i1 = i
            i2 = i + 1 if i + 1 < self.m_vertexCount else 0
        self.m_R.SetM(self.m_body.m_R)
        self.m_position.x = self.m_body.m_position.x + (self.m_R.col1.x * self.m_localCentroid.x + self.m_R.col2.x * self.m_localCentroid.y)
        self.m_position.y = self.m_body.m_position.y + (self.m_R.col1.y * self.m_localCentroid.x + self.m_R.col2.y * self.m_localCentroid.y)
        b2PolyShape.tAbsR.col1.x = self.m_R.col1.x * self.m_localOBB.R.col1.x + self.m_R.col2.x * self.m_localOBB.R.col1.y
        b2PolyShape.tAbsR.col1.y = self.m_R.col1.y * self.m_localOBB.R.col1.x + self.m_R.col2.y * self.m_localOBB.R.col1.y
        b2PolyShape.tAbsR.col2.x = self.m_R.col1.x * self.m_localOBB.R.col2.x + self.m_R.col2.x * self.m_localOBB.R.col2.y
        b2PolyShape.tAbsR.col2.y = self.m_R.col1.y * self.m_localOBB.R.col2.x + self.m_R.col2.y * self.m_localOBB.R.col2.y
        b2PolyShape.tAbsR.Abs()
        hX = b2PolyShape.tAbsR.col1.x * self.m_localOBB.extents.x + b2PolyShape.tAbsR.col2.x * self.m_localOBB.extents.y
        hY = b2PolyShape.tAbsR.col1.y * self.m_localOBB.extents.x + b2PolyShape.tAbsR.col2.y * self.m_localOBB.extents.y
        positionX = self.m_position.x + (self.m_R.col1.x * self.m_localOBB.center.x + self.m_R.col2.x * self.m_localOBB.center.y)
        positionY = self.m_position.y + (self.m_R.col1.y * self.m_localOBB.center.x + self.m_R.col2.y * self.m_localOBB.center.y)
        aabb.minVertex.x = positionX - hX
        aabb.minVertex.y = positionY - hY
        aabb.maxVertex.x = positionX + hX
        aabb.maxVertex.y = positionY + hY
        broadPhase = self.m_body.m_world.m_broadPhase
        if (broadPhase.InRange(aabb)):
            self.m_proxyId = broadPhase.CreateProxy(aabb, self)
        else:
            self.m_proxyId = b2Pair.b2_nullProxy
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            self.m_body.Freeze()

    def Synchronize(self,position1, R1, position2, R2):
        self.m_R.SetM(R2)
        self.m_position.x = self.m_body.m_position.x + (R2.col1.x * self.m_localCentroid.x + R2.col2.x * self.m_localCentroid.y)
        self.m_position.y = self.m_body.m_position.y + (R2.col1.y * self.m_localCentroid.x + R2.col2.y * self.m_localCentroid.y)
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            return
        else:
            v1 = R1.col1
            v2 = R1.col2
            v3 = self.m_localOBB.R.col1
            v4 = self.m_localOBB.R.col2
            self.syncMat.col1.x = v1.x * v3.x + v2.x * v3.y
            self.syncMat.col1.y = v1.y * v3.x + v2.y * v3.y
            self.syncMat.col2.x = v1.x * v4.x + v2.x * v4.y
            self.syncMat.col2.y = v1.y * v4.x + v2.y * v4.y
        self.syncMat.Abs()
        hX = self.m_localCentroid.x + self.m_localOBB.center.x
        hY = self.m_localCentroid.y + self.m_localOBB.center.y
        centerX = position1.x + (R1.col1.x * hX + R1.col2.x * hY)
        centerY = position1.y + (R1.col1.y * hX + R1.col2.y * hY)
        hX = self.syncMat.col1.x * self.m_localOBB.extents.x + self.syncMat.col2.x * self.m_localOBB.extents.y
        hY = self.syncMat.col1.y * self.m_localOBB.extents.x + self.syncMat.col2.y * self.m_localOBB.extents.y
        self.syncAABB.minVertex.x = centerX - hX
        self.syncAABB.minVertex.y = centerY - hY
        self.syncAABB.maxVertex.x = centerX + hX
        self.syncAABB.maxVertex.y = centerY + hY
        v1 = R2.col1
        v2 = R2.col2
        v3 = self.m_localOBB.R.col1
        v4 = self.m_localOBB.R.col2
        self.syncMat.col1.x = v1.x * v3.x + v2.x * v3.y
        self.syncMat.col1.y = v1.y * v3.x + v2.y * v3.y
        self.syncMat.col2.x = v1.x * v4.x + v2.x * v4.y
        self.syncMat.col2.y = v1.y * v4.x + v2.y * v4.y
        self.syncMat.Abs()
        hX = self.m_localCentroid.x + self.m_localOBB.center.x
        hY = self.m_localCentroid.y + self.m_localOBB.center.y
        centerX = position2.x + (R2.col1.x * hX + R2.col2.x * hY)
        centerY = position2.y + (R2.col1.y * hX + R2.col2.y * hY)
        hX = self.syncMat.col1.x * self.m_localOBB.extents.x + self.syncMat.col2.x * self.m_localOBB.extents.y
        hY = self.syncMat.col1.y * self.m_localOBB.extents.x + self.syncMat.col2.y * self.m_localOBB.extents.y
        self.syncAABB.minVertex.x = min(self.syncAABB.minVertex.x, centerX - hX)
        self.syncAABB.minVertex.y = min(self.syncAABB.minVertex.y, centerY - hY)
        self.syncAABB.maxVertex.x = max(self.syncAABB.maxVertex.x, centerX + hX)
        self.syncAABB.maxVertex.y = max(self.syncAABB.maxVertex.y, centerY + hY)
        broadPhase = self.m_body.m_world.m_broadPhase
        if (broadPhase.InRange(self.syncAABB)):
            broadPhase.MoveProxy(self.m_proxyId, self.syncAABB)
        else:
            self.m_body.Freeze()

    def QuickSync(self,position, R):
        self.m_R.SetM(R)
        self.m_position.x = position.x + (R.col1.x * self.m_localCentroid.x + R.col2.x * self.m_localCentroid.y)
        self.m_position.y = position.y + (R.col1.y * self.m_localCentroid.x + R.col2.y * self.m_localCentroid.y)

    def ResetProxy(self,broadPhase):
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            return
        #proxy = broadPhase.GetProxy(self.m_proxyId)
        broadPhase.DestroyProxy(self.m_proxyId)
        #proxy = None
        R = b2Math.b2MulMM(self.m_R, self.m_localOBB.R)
        absR = b2Math.b2AbsM(R)
        h = b2Math.b2MulMV(absR, self.m_localOBB.extents)
        position = b2Math.b2MulMV(self.m_R, self.m_localOBB.center)
        position.Add(self.m_position)
        aabb = b2AABB()
        aabb.minVertex.SetV(position)
        aabb.minVertex.Subtract(h)
        aabb.maxVertex.SetV(position)
        aabb.maxVertex.Add(h)
        if (broadPhase.InRange(aabb)):
            self.m_proxyId = broadPhase.CreateProxy(aabb, self)
        else:
            self.m_proxyId = b2Pair.b2_nullProxy
        if (self.m_proxyId == b2Pair.b2_nullProxy):
            self.m_body.Freeze()

    def Support(self,dX, dY, out):
        dLocalX = (dX*self.m_R.col1.x + dY*self.m_R.col1.y)
        dLocalY = (dX*self.m_R.col2.x + dY*self.m_R.col2.y)
        bestIndex = 0
        bestValue = (self.m_coreVertices[0].x * dLocalX + self.m_coreVertices[0].y * dLocalY)
        for i in range(self.m_vertexCount):
            value = (self.m_coreVertices[i].x * dLocalX + self.m_coreVertices[i].y * dLocalY)
            if (value > bestValue):
                bestIndex = i
                bestValue = value
        out.Set(    self.m_position.x + (self.m_R.col1.x * self.m_coreVertices[bestIndex].x + self.m_R.col2.x * self.m_coreVertices[bestIndex].y),
                    self.m_position.y + (self.m_R.col1.y * self.m_coreVertices[bestIndex].x + self.m_R.col2.y * self.m_coreVertices[bestIndex].y))
