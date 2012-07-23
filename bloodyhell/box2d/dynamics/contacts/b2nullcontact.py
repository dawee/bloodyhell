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

import math

from box2d.dynamics.contacts.b2contactnode import b2ContactNode
from box2d.dynamics.contacts.b2contact import b2Contact
from box2d.common.math.b2math import b2Math


class b2NullContact(b2Contact):

    def __init__(self,s1=None, s2=None):
        self.m_node1 = b2ContactNode()
        self.m_node2 = b2ContactNode()
        self.m_flags = 0
        if (not s1 or not s2):
            self.m_shape1 = None
            self.m_shape2 = None
            return
        self.m_shape1 = s1
        self.m_shape2 = s2
        self.m_manifoldCount = 0
        self.m_friction = math.sqrt(self.m_shape1.m_friction * self.m_shape2.m_friction)
        self.m_restitution = b2Math.b2Max(self.m_shape1.m_restitution, self.m_shape2.m_restitution)
        self.m_prev = None
        self.m_next = None
        self.m_node1.contact = None
        self.m_node1.prev = None
        self.m_node1.next = None
        self.m_node1.other = None
        self.m_node2.contact = None
        self.m_node2.prev = None
        self.m_node2.next = None
        self.m_node2.other = None

    def Evaluate(self):
        pass

    def GetManifolds(self):
        return None

