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

from box2d.common.math.b2math import b2Math
from box2d.dynamics.worldlistener import b2WorldListener
from box2d.dynamics.b2island import b2Island
from box2d.dynamics.b2contactmanager import b2ContactManager
from box2d.dynamics.contacts.b2contact import b2Contact
from box2d.dynamics.b2timestep import b2TimeStep
from box2d.dynamics.b2collisionfilter import b2CollisionFilter
from box2d.dynamics.b2bodydef import b2BodyDef
from box2d.dynamics.b2body import b2Body
from box2d.dynamics.joints.b2joint import b2Joint
from box2d.collision.b2broadphase import b2BroadPhase


class b2World(object):

    s_enablePositionCorrection = 1
    s_enableWarmStarting = 1

    def __init__(self, worldAABB, gravity, doSleep):
        self.step = b2TimeStep()
        self.m_contactManager = b2ContactManager()
        self.m_listener = None
        self.m_filter = b2CollisionFilter.b2_defaultFilter
        self.m_bodyList = None
        self.m_contactList = None
        self.m_jointList = None
        self.m_bodyCount = 0
        self.m_contactCount = 0
        self.m_jointCount = 0
        self.m_bodyDestroyList = None
        self.m_allowSleep = doSleep
        self.m_gravity = gravity
        self.m_contactManager.m_world = self
        self.m_broadPhase = b2BroadPhase(worldAABB, self.m_contactManager)
        bd = b2BodyDef()
        self.m_groundBody = self.CreateBody(bd)

    def SetListener(self, listener):
        self.m_listener = listener

    def SetFilter(self, filter):
        self.m_filter = filter

    def CreateBody(self, definition):
        b = b2Body(definition, self)
        b.m_prev = None
        b.m_next = self.m_bodyList
        if (self.m_bodyList):
            self.m_bodyList.m_prev = b
        self.m_bodyList = b
        ++self.m_bodyCount
        return b

    def DestroyBody(self, b):
        if (b.m_flags & b2Body.e_destroyFlag):
            return
        if (b.m_prev):
            b.m_prev.m_next = b.m_next
        if (b.m_next):
            b.m_next.m_prev = b.m_prev
        if (b == self.m_bodyList):
            self.m_bodyList = b.m_next
        b.m_flags |= b2Body.e_destroyFlag
        --self.m_bodyCount
        b.m_prev = None
        b.m_next = self.m_bodyDestroyList
        self.m_bodyDestroyList = b

    def CleanBodyList(self):
        self.m_contactManager.m_destroyImmediate = True
        b = self.m_bodyDestroyList
        while (b):
            b0 = b
            b = b.m_next
            jn = b0.m_jointList
            while (jn):
                jn0 = jn
                jn = jn.next
                if (self.m_listener):
                    self.m_listener.NotifyJointDestroyed(jn0.joint)
                self.DestroyJoint(jn0.joint)
            b0.Destroy()
        self.m_bodyDestroyList = None
        self.m_contactManager.m_destroyImmediate = False

    def CreateJoint(self, definition):
        j = b2Joint.Create(definition, self.m_blockAllocator)
        j.m_prev = None
        j.m_next = self.m_jointList
        if (self.m_jointList):
            self.m_jointList.m_prev = j
        self.m_jointList = j
        ++self.m_jointCount
        j.m_node1.joint = j
        j.m_node1.other = j.m_body2
        j.m_node1.prev = None
        j.m_node1.next = j.m_body1.m_jointList
        if (j.m_body1.m_jointList):
            j.m_body1.m_jointList.prev = j.m_node1
        j.m_body1.m_jointList = j.m_node1
        j.m_node2.joint = j
        j.m_node2.other = j.m_body1
        j.m_node2.prev = None
        j.m_node2.next = j.m_body2.m_jointList
        if (j.m_body2.m_jointList):
            j.m_body2.m_jointList.prev = j.m_node2
        j.m_body2.m_jointList = j.m_node2
        if (definition.collideConnected == False):
            b = definition.body1 if definition.body1.m_shapeCount < definition.body2.m_shapeCount else definition.body2
            s = b.m_shapeList
            while(s):
                s.ResetProxy(self.m_broadPhase)
                s = s.m_next
        return j

    def DestroyJoint(self,j):
        collideConnected = j.m_collideConnected
        if (j.m_prev):
            j.m_prev.m_next = j.m_next
        if (j.m_next):
            j.m_next.m_prev = j.m_prev
        if (j == self.m_jointList):
            self.m_jointList = j.m_next
        body1 = j.m_body1
        body2 = j.m_body2
        body1.WakeUp()
        body2.WakeUp()
        if (j.m_node1.prev):
            j.m_node1.prev.next = j.m_node1.next
        if (j.m_node1.next):
            j.m_node1.next.prev = j.m_node1.prev
        if (j.m_node1 == body1.m_jointList):
            body1.m_jointList = j.m_node1.next
        j.m_node1.prev = None
        j.m_node1.next = None
        if (j.m_node2.prev):
            j.m_node2.prev.next = j.m_node2.next
        if (j.m_node2.next):
            j.m_node2.next.prev = j.m_node2.prev
        if (j.m_node2 == body2.m_jointList):
            body2.m_jointList = j.m_node2.next
        j.m_node2.prev = None
        j.m_node2.next = None
        b2Joint.Destroy(j, self.m_blockAllocator)
        --self.m_jointCount
        if (collideConnected == False):
            b = body1 if body1.m_shapeCount < body2.m_shapeCount else body2
            s = b.m_shapeList
            while(s):
                s.ResetProxy(self.m_broadPhase)
                s = s.m_next

    def GetGroundBody(self):
        return self.m_groundBody

    def Step(self,dt, iterations):
        self.step.dt = dt
        self.step.iterations = iterations
        if (dt > 0.0):
            self.step.inv_dt = 1.0 / dt
        else:
            self.step.inv_dt = 0.0
        self.m_positionIterationCount = 0
        self.m_contactManager.CleanContactList()
        self.CleanBodyList()
        self.m_contactManager.Collide()
        island = b2Island(self.m_bodyCount, self.m_contactCount, self.m_jointCount, self.m_stackAllocator)
        b = self.m_bodyList
        while(b is not None):
            b.m_flags &= ~b2Body.e_islandFlag
            b = b.m_next
        c = self.m_contactList
        while(c is not None):
            c.m_flags &= ~b2Contact.e_islandFlag
            c = c.m_next
        j = self.m_jointList
        while(j != None):
            j.m_islandFlag = False
            j = j.m_next
        # stackSize = self.m_bodyCount
        stack = range(self.m_bodyCount)
        for k in range(self.m_bodyCount):
            stack[k] = None
        seed = self.m_bodyList
        while(seed != None):
            if (seed.m_flags & (b2Body.e_staticFlag | b2Body.e_islandFlag | b2Body.e_sleepFlag | b2Body.e_frozenFlag)):
                 seed = seed.m_next
                 continue
            island.Clear()
            stackCount = 0
            stackCount += 1
            stack[stackCount] = seed
            seed.m_flags |= b2Body.e_islandFlag
            while (stackCount > 0):
                stackCount -= 1
                b = stack[stackCount]
                island.AddBody(b)
                b.m_flags &= ~b2Body.e_sleepFlag
                if (b.m_flags & b2Body.e_staticFlag):
                    continue
                cn = b.m_contactList
                while(cn is not None):
                    if (cn.contact.m_flags & b2Contact.e_islandFlag):
                        cn = cn.next
                        continue
                    island.AddContact(cn.contact)
                    cn.contact.m_flags |= b2Contact.e_islandFlag
                    other = cn.other
                    if (other.m_flags & b2Body.e_islandFlag):
                        cn = cn.next
                        continue
                    stackCount += 1
                    stack[stackCount] = other
                    other.m_flags |= b2Body.e_islandFlag
                    cn = cn.next
                jn = b.m_jointList
                while(jn is not None):
                    if (jn.joint.m_islandFlag == True):
                        jn = jn.next
                        continue
                    island.AddJoint(jn.joint)
                    jn.joint.m_islandFlag = True
                    other = jn.other
                    if (other.m_flags & b2Body.e_islandFlag):
                        jn = jn.next
                        continue
                    stackCount += 1
                    stack[stackCount] = other
                    other.m_flags |= b2Body.e_islandFlag
                    jn = jn.next
            island.Solve(self.step, self.m_gravity)
            self.m_positionIterationCount = b2Math.b2Max(self.m_positionIterationCount, b2Island.m_positionIterationCount)
            if (self.m_allowSleep):
                island.UpdateSleep(dt)
            for i in range(island.m_bodyCount):
                b = island.m_bodies[i]
                if (b.m_flags & b2Body.e_staticFlag):
                    b.m_flags &= ~b2Body.e_islandFlag
                if (b.IsFrozen() and self.m_listener):
                    response = self.m_listener.NotifyBoundaryViolated(b)
                    if (response == b2WorldListener.b2_destroyBody):
                        self.DestroyBody(b)
                        b = None
                        island.m_bodies[i] = None
            seed = seed.m_next
        self.m_broadPhase.Commit()

    def Query(self,aabb, shapes, maxCount):
        results = []
        count = self.m_broadPhase.QueryAABB(aabb, results, maxCount)
        for i in range(count):
            shapes[i] = results[i]
        return count

    def GetBodyList(self):
        return self.m_bodyList

    def GetJointList(self):
        return self.m_jointList

    def GetContactList(self):
        return self.m_contactList
