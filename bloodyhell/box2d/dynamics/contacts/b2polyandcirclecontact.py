﻿"""
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


class b2PolyAndCircleContact(object):
        """
        inherit from "b2Contact"
        """
Object.extend(b2PolyAndCircleContact.prototype, 

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
        self.m_manifold = [new b2Manifold()]
        b2Settings.b2Assert(self.m_shape1.m_type == b2Shape.e_polyShape)
        b2Settings.b2Assert(self.m_shape2.m_type == b2Shape.e_circleShape)
        self.m_manifold[0].pointCount = 0
        self.m_manifold[0].points[0].normalImpulse = 0.0
        self.m_manifold[0].points[0].tangentImpulse = 0.0

    def Evaluate(self):
        """
        TO FILL
        """
        b2Collision.b2CollidePolyAndCircle(self.m_manifold[0], self.m_shape1, self.m_shape2, false)
        if (self.m_manifold[0].pointCount > 0):
            self.m_manifoldCount = 1
        else
            self.m_manifoldCount = 0

    def GetManifolds(self):
        """
        TO FILL
        """
        return self.m_manifold
    m_manifold: [new b2Manifold()])
b2PolyAndCircleContact.Create = function(shape1, shape2, allocator)
        return new b2PolyAndCircleContact(shape1, shape2)
b2PolyAndCircleContact.Destroy = function(contact, allocator)