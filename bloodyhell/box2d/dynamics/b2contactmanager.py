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

from box2d.collision.b2paircallback import b2PairCallback
from box2d.dynamics.contacts.b2nullcontact import b2NullContact
from box2d.dynamics.contacts.b2contact import b2Contact


class b2ContactManager(b2PairCallback):

    def __init__(self):
        self.m_NoneContact = b2NullContact()
        self.m_world = None
        self.m_destroyImmediate = False

    def PairAdded(self,proxyUserData1, proxyUserData2):
        shape1 = proxyUserData1
        shape2 = proxyUserData2
        body1 = shape1.m_body
        body2 = shape2.m_body
        if (body1.IsStatic() and body2.IsStatic()):
            return self.m_NoneContact
        if (shape1.m_body == shape2.m_body):
            return self.m_NoneContact
        if (body2.IsConnected(body1)):
            return self.m_NoneContact
        if (self.m_world.m_filter != None and self.m_world.m_filter.ShouldCollide(shape1, shape2) == False):
            return self.m_NoneContact
        if (body2.m_invMass == 0.0):
            tempShape = shape1
            shape1 = shape2
            shape2 = tempShape
            tempBody = body1
            body1 = body2
            body2 = tempBody
        contact = b2Contact.Create(shape1, shape2, self.m_world.m_blockAllocator)
        if (contact == None):
            return self.m_NoneContact
        else:
            contact.m_prev = None
            contact.m_next = self.m_world.m_contactList
            if (self.m_world.m_contactList != None):
                self.m_world.m_contactList.m_prev = contact
            self.m_world.m_contactList = contact
            self.m_world.m_contactCount += 1
        return contact

    def PairRemoved(self,proxyUserData1, proxyUserData2, pairUserData):
        if (pairUserData == None):
            return
        c = pairUserData
        if (c != self.m_NoneContact):
            if (self.m_destroyImmediate == True):
                self.DestroyContact(c)
                c = None
            else:
                c.m_flags |= b2Contact.e_destroyFlag

    def DestroyContact(self,c):
        if (c.m_prev):
            c.m_prev.m_next = c.m_next
        if (c.m_next):
            c.m_next.m_prev = c.m_prev
        if (c == self.m_world.m_contactList):
            self.m_world.m_contactList = c.m_next
        if (c.GetManifoldCount() > 0):
            body1 = c.m_shape1.m_body
            body2 = c.m_shape2.m_body
            node1 = c.m_node1
            node2 = c.m_node2
            body1.WakeUp()
            body2.WakeUp()
            if (node1.prev):
                node1.prev.next = node1.next
            if (node1.next):
                node1.next.prev = node1.prev
            if (node1 == body1.m_contactList):
                body1.m_contactList = node1.next
            node1.prev = None
            node1.next = None
            if (node2.prev):
                node2.prev.next = node2.next
            if (node2.next):
                node2.next.prev = node2.prev
            if (node2 == body2.m_contactList):
                body2.m_contactList = node2.next
            node2.prev = None
            node2.next = None
        b2Contact.Destroy(c, self.m_world.m_blockAllocator)
        self.m_world.m_contactCount -= 1

    def CleanContactList(self):
        c = self.m_world.m_contactList
        while (c != None):
            c0 = c
            c = c.m_next
            if (c0.m_flags & b2Contact.e_destroyFlag):
                self.DestroyContact(c0)
                c0 = None

    def Collide(self):
        c = self.m_world.m_contactList
        while(c != None):
            if (c.m_shape1.m_body.IsSleeping() and c.m_shape2.m_body.IsSleeping()):
                c = c.m_next
                continue
            oldCount = c.GetManifoldCount()
            c.Evaluate()
            newCount = c.GetManifoldCount()
            if (oldCount == 0 and newCount > 0):
                body1 = c.m_shape1.m_body
                body2 = c.m_shape2.m_body
                node1 = c.m_node1
                node2 = c.m_node2
                node1.contact = c
                node1.other = body2
                node1.prev = None
                node1.next = body1.m_contactList
                if (node1.next != None):
                    node1.next.prev = c.m_node1
                body1.m_contactList = c.m_node1
                node2.contact = c
                node2.other = body1
                node2.prev = None
                node2.next = body2.m_contactList
                if (node2.next != None):
                    node2.next.prev = node2
                body2.m_contactList = node2
            elif (oldCount > 0 and newCount == 0):
                body1 = c.m_shape1.m_body
                body2 = c.m_shape2.m_body
                node1 = c.m_node1
                node2 = c.m_node2
                if (node1.prev):
                    node1.prev.next = node1.next
                if (node1.next):
                    node1.next.prev = node1.prev
                if (node1 == body1.m_contactList):
                    body1.m_contactList = node1.next
                node1.prev = None
                node1.next = None
                if (node2.prev):
                    node2.prev.next = node2.next
                if (node2.next):
                    node2.next.prev = node2.prev
                if (node2 == body2.m_contactList):
                    body2.m_contactList = node2.next
                node2.prev = None
                node2.next = None
            c = c.m_next

