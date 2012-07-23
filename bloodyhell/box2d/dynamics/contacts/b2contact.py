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
import  math

from box2d.collision.shapes.b2shape import b2Shape
from box2d.dynamics.contacts.b2contactnode import b2ContactNode
from box2d.dynamics.contacts.b2contactregister import b2ContactRegister
from box2d.dynamics.contacts.b2circlecontact import b2CircleContact
from box2d.dynamics.contacts.b2polycontact import b2PolyContact
from box2d.dynamics.contacts.b2polyandcirclecontact import b2PolyAndCircleContact
from box2d.common.math.b2math import b2Math


class b2Contact(object):

    s_registers = None
    s_initialized = False
    e_islandFlag = 0x0001
    e_destroyFlag = 0x0002

    def GetManifolds(self):
        return None

    def GetManifoldCount(self):
        return self.m_manifoldCount

    def GetNext(self):
        return self.m_next

    def GetShape1(self):
        return self.m_shape1

    def GetShape2(self):
        return self.m_shape2

    def __init__(self,s1, s2):
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

    @staticmethod
    def AddType(createFcn, destroyFcn, type1, type2):
        b2Contact.s_registers[type1][type2].createFcn = createFcn
        b2Contact.s_registers[type1][type2].destroyFcn = destroyFcn
        b2Contact.s_registers[type1][type2].primary = True
        if (type1 != type2):
            b2Contact.s_registers[type2][type1].createFcn = createFcn
            b2Contact.s_registers[type2][type1].destroyFcn = destroyFcn
            b2Contact.s_registers[type2][type1].primary = False

    @staticmethod
    def InitializeRegisters():
        b2Contact.s_registers = range(b2Shape.e_shapeTypeCount)
        for i in range(b2Shape.e_shapeTypeCount):
            b2Contact.s_registers[i] = range(b2Shape.e_shapeTypeCount)
            for j in range(b2Shape.e_shapeTypeCount):
                b2Contact.s_registers[i][j] = b2ContactRegister()
        b2Contact.AddType(b2CircleContact.Create, b2CircleContact.Destroy, b2Shape.e_circleShape, b2Shape.e_circleShape)
        b2Contact.AddType(b2PolyAndCircleContact.Create, b2PolyAndCircleContact.Destroy, b2Shape.e_polyShape, b2Shape.e_circleShape)
        b2Contact.AddType(b2PolyContact.Create, b2PolyContact.Destroy, b2Shape.e_polyShape, b2Shape.e_polyShape)


    @staticmethod
    def Create(shape1, shape2, allocator):
        if (b2Contact.s_initialized == False):
            b2Contact.InitializeRegisters()
            b2Contact.s_initialized = True
        type1 = shape1.m_type
        type2 = shape2.m_type
        createFcn = b2Contact.s_registers[type1][type2].createFcn
        if (createFcn):
            if (b2Contact.s_registers[type1][type2].primary):
                return createFcn(shape1, shape2, allocator)
            else:
                c = createFcn(shape2, shape1, allocator)
                for i in range(c.GetManifoldCount()):
                    m = c.GetManifolds()[ i ]
                    m.normal = m.normal.Negative()
                return c
        else:
            return None

    @staticmethod
    def Destroy(contact, allocator):
        if (contact.GetManifoldCount() > 0):
            contact.m_shape1.m_body.WakeUp()
            contact.m_shape2.m_body.WakeUp()
        type1 = contact.m_shape1.m_type
        type2 = contact.m_shape2.m_type
        destroyFcn = b2Contact.s_registers[type1][type2].destroyFcn
        destroyFcn(contact, allocator)
