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


class b2PolyContact(object):
        """
        inherit from "b2Contact"
        """
Object.extend(b2PolyContact.prototype, 

    def __init__(self,s1, s2):
        """
        TO FILL
        """
        self.m_node1 = new b2ContactNode()
        self.m_node2 = new b2ContactNode()
        self.m_flags = 0
        if (!s1 or !s2):
            self.m_shape1 = null
            self.m_shape2 = null
            return
        self.m_shape1 = s1
        self.m_shape2 = s2
        self.m_manifoldCount = 0
        self.m_friction = Math.sqrt(self.m_shape1.m_friction * self.m_shape2.m_friction)
        self.m_restitution = b2Math.b2Max(self.m_shape1.m_restitution, self.m_shape2.m_restitution)
        self.m_prev = null
        self.m_next = null
        self.m_node1.contact = null
        self.m_node1.prev = null
        self.m_node1.next = null
        self.m_node1.other = null
        self.m_node2.contact = null
        self.m_node2.prev = null
        self.m_node2.next = null
        self.m_node2.other = null
        self.m0 = new b2Manifold()
        self.m_manifold = [new b2Manifold()]
        self.m_manifold[0].pointCount = 0
    m0: new b2Manifold(),

    def Evaluate(self):
        """
        TO FILL
        """
        tMani = self.m_manifold[0]
        tPoints = self.m0.points
for k in range(tMani.pointCount):
            tPoint = tPoints[k]
            tPoint0 = tMani.points[k]
            tPoint.normalImpulse = tPoint0.normalImpulse
            tPoint.tangentImpulse = tPoint0.tangentImpulse
            tPoint.id = tPoint0.id.Copy()
            """self.m0.points[k].id.features = new Features()
            self.m0.points[k].id.features.referenceFace = self.m_manifold[0].points[k].id.features.referenceFace
            self.m0.points[k].id.features.incidentEdge = self.m_manifold[0].points[k].id.features.incidentEdge
            self.m0.points[k].id.features.incidentVertex = self.m_manifold[0].points[k].id.features.incidentVertex
            self.m0.points[k].id.features.flip = self.m_manifold[0].points[k].id.features.flip"""
        self.m0.pointCount = tMani.pointCount
        b2Collision.b2CollidePoly(tMani, self.m_shape1, self.m_shape2, false)
        if (tMani.pointCount > 0):
            match = [false, false]
for i in range(tMani.pointCount):
                cp = tMani.points[ i ]
                cp.normalImpulse = 0.0
                cp.tangentImpulse = 0.0
                idKey = cp.id.key
for j in range(self.m0.pointCount):
                    if (match[j] == true):
                        continue
                    cp0 = self.m0.points[j]
                    id0 = cp0.id
                    if (id0.key == idKey):
                        match[j] = true
                        cp.normalImpulse = cp0.normalImpulse
                        cp.tangentImpulse = cp0.tangentImpulse
                        break
            self.m_manifoldCount = 1
        else
            self.m_manifoldCount = 0

    def GetManifolds(self):
        """
        TO FILL
        """
        return self.m_manifold
    m_manifold: [new b2Manifold()])
b2PolyContact.Create = function(shape1, shape2, allocator)
        return new b2PolyContact(shape1, shape2)
b2PolyContact.Destroy = function(contact, allocator)
