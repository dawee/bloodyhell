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
from box2d.common.math.b2mat22 import b2Mat22
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.b2settings import b2Settings
from box2d.collision.shapes.b2shape import b2Shape
from box2d.collision.shapes.b2massdata import b2MassData


class b2Body(object):

    e_staticFlag = 0x0001
    e_frozenFlag = 0x0002
    e_islandFlag = 0x0004
    e_sleepFlag = 0x0008
    e_allowSleepFlag = 0x0010
    e_destroyFlag = 0x0020

    def SetOriginPosition(self,position, rotation):
        if (self.IsFrozen()):
            return
        self.m_rotation = rotation
        self.m_R.Set(self.m_rotation)
        self.m_position = b2Math.AddVV(position , b2Math.b2MulMV(self.m_R, self.m_center))
        self.m_position0.SetV(self.m_position)
        self.m_rotation0 = self.m_rotation
        s = self.m_shapeList
        while(s is not None):
            s.Synchronize(self.m_position, self.m_R, self.m_position, self.m_R)
            s = s.m_next
        self.m_world.m_broadPhase.Commit()

    def GetOriginPosition(self):
        return b2Math.SubtractVV(self.m_position, b2Math.b2MulMV(self.m_R, self.m_center))

    def SetCenterPosition(self,position, rotation):
        if (self.IsFrozen()):
            return
        self.m_rotation = rotation
        self.m_R.Set(self.m_rotation)
        self.m_position.SetV( position )
        self.m_position0.SetV(self.m_position)
        self.m_rotation0 = self.m_rotation
        s = self.m_shapeList
        while(s is not None):
            s.Synchronize(self.m_position, self.m_R, self.m_position, self.m_R)
            s = s.m_next
        self.m_world.m_broadPhase.Commit()

    def GetCenterPosition(self):
        return self.m_position

    def GetRotation(self):
        return self.m_rotation

    def GetRotationMatrix(self):
        return self.m_R

    def SetLinearVelocity(self,v):
        self.m_linearVelocity.SetV(v)

    def GetLinearVelocity(self):
        return self.m_linearVelocity

    def SetAngularVelocity(self,w):
        self.m_angularVelocity = w

    def GetAngularVelocity(self):
        return self.m_angularVelocity

    def ApplyForce(self,force, point):
        if (self.IsSleeping() == False):
            self.m_force.Add( force )
            self.m_torque += b2Math.b2CrossVV(b2Math.SubtractVV(point, self.m_position), force)

    def ApplyTorque(self,torque):
        if (self.IsSleeping() == False):
            self.m_torque += torque

    def ApplyImpulse(self,impulse, point):
        if (self.IsSleeping() == False):
            self.m_linearVelocity.Add( b2Math.MulFV(self.m_invMass, impulse) )
            self.m_angularVelocity += ( self.m_invI * b2Math.b2CrossVV( b2Math.SubtractVV(point, self.m_position), impulse)  )

    def GetMass(self):
        return self.m_mass

    def GetInertia(self):
        return self.m_I

    def GetWorldPoint(self,localPoint):
        return b2Math.AddVV(self.m_position , b2Math.b2MulMV(self.m_R, localPoint))

    def GetWorldVector(self,localVector):
        return b2Math.b2MulMV(self.m_R, localVector)

    def GetLocalPoint(self,worldPoint):
        return b2Math.b2MulTMV(self.m_R, b2Math.SubtractVV(worldPoint, self.m_position))

    def GetLocalVector(self,worldVector):
        return b2Math.b2MulTMV(self.m_R, worldVector)

    def IsStatic(self):
        return (self.m_flags & b2Body.e_staticFlag) == b2Body.e_staticFlag

    def IsFrozen(self):
        return (self.m_flags & b2Body.e_frozenFlag) == b2Body.e_frozenFlag

    def IsSleeping(self):
        return (self.m_flags & b2Body.e_sleepFlag) == b2Body.e_sleepFlag

    def AllowSleeping(self,flag):
        if (flag):
            self.m_flags |= b2Body.e_allowSleepFlag
        else:
            self.m_flags &= ~b2Body.e_allowSleepFlag
            self.WakeUp()

    def WakeUp(self):
        self.m_flags &= ~b2Body.e_sleepFlag
        self.m_sleepTime = 0.0

    def GetShapeList(self):
        return self.m_shapeList

    def GetContactList(self):
        return self.m_contactList

    def GetJointList(self):
        return self.m_jointList

    def GetNext(self):
        return self.m_next

    def GetUserData(self):
        return self.m_userData

    def __init__(self,bd, world):
        self.sMat0 = b2Mat22()
        self.m_position = b2Vec2()
        self.m_R = b2Mat22(0)
        self.m_position0 = b2Vec2()
        i = 0
        self.m_flags = 0
        self.m_position.SetV( bd.position )
        self.m_rotation = bd.rotation
        self.m_R.Set(self.m_rotation)
        self.m_position0.SetV(self.m_position)
        self.m_rotation0 = self.m_rotation
        self.m_world = world
        self.m_linearDamping = b2Math.b2Clamp(1.0 - bd.linearDamping, 0.0, 1.0)
        self.m_angularDamping = b2Math.b2Clamp(1.0 - bd.angularDamping, 0.0, 1.0)
        self.m_force = b2Vec2(0.0, 0.0)
        self.m_torque = 0.0
        self.m_mass = 0.0
        massDatas = range(b2Settings.b2_maxShapesPerBody)
        for i in range(b2Settings.b2_maxShapesPerBody):
            massDatas[i] = b2MassData()
        self.m_shapeCount = 0
        self.m_center = b2Vec2(0.0, 0.0)
        for i in range(b2Settings.b2_maxShapesPerBody):
            sd = bd.shapes[i]
            if (sd == None):
                break
            massData = massDatas[ i ]
            sd.ComputeMass(massData)
            self.m_mass += massData.mass
            self.m_center.x += massData.mass * (sd.localPosition.x + massData.center.x)
            self.m_center.y += massData.mass * (sd.localPosition.y + massData.center.y)
            ++self.m_shapeCount
        if (self.m_mass > 0.0):
            self.m_center.Multiply( 1.0 / self.m_mass )
            self.m_position.Add( b2Math.b2MulMV(self.m_R, self.m_center) )
        else:
            self.m_flags |= b2Body.e_staticFlag
        self.m_I = 0.0
        for i in range(self.m_shapeCount):
            sd = bd.shapes[i]
            massData = massDatas[ i ]
            self.m_I += massData.I
            r = b2Math.SubtractVV( b2Math.AddVV(sd.localPosition, massData.center), self.m_center )
            self.m_I += massData.mass * b2Math.b2Dot(r, r)
        if (self.m_mass > 0.0):
            self.m_invMass = 1.0 / self.m_mass
        else:
            self.m_invMass = 0.0
        if (self.m_I > 0.0 and bd.preventRotation == False):
            self.m_invI = 1.0 / self.m_I
        else:
            self.m_I = 0.0
            self.m_invI = 0.0
        self.m_linearVelocity = b2Math.AddVV(bd.linearVelocity, b2Math.b2CrossFV(bd.angularVelocity, self.m_center))
        self.m_angularVelocity = bd.angularVelocity
        self.m_jointList = None
        self.m_contactList = None
        self.m_prev = None
        self.m_next = None
        self.m_shapeList = None
        for i in range(self.m_shapeCount):
            sd = bd.shapes[i]
            shape = b2Shape.Create(sd, self, self.m_center)
            shape.m_next = self.m_shapeList
            self.m_shapeList = shape
        self.m_sleepTime = 0.0
        if (bd.allowSleep):
            self.m_flags |= b2Body.e_allowSleepFlag
        if (bd.isSleeping):
            self.m_flags |= b2Body.e_sleepFlag
        if ((self.m_flags & b2Body.e_sleepFlag)  or self.m_invMass == 0.0):
            self.m_linearVelocity.Set(0.0, 0.0)
            self.m_angularVelocity = 0.0
        self.m_userData = bd.userData

    def Destroy(self):
        s = self.m_shapeList
        while (s):
            s0 = s
            s = s.m_next
            b2Shape.Destroy(s0)

    def SynchronizeShapes(self):
        self.sMat0.Set(self.m_rotation0)
        s = self.m_shapeList
        while(s is not None):
            s.Synchronize(self.m_position0, self.sMat0, self.m_position, self.m_R)
            s = s.m_next

    def QuickSyncShapes(self):
        s = self.m_shapeList
        while(s is not None):
            s.QuickSync(self.m_position, self.m_R)
            s = s.m_next

    def IsConnected(self,other):
        jn = self.m_jointList
        while(jn is not None):
            if (jn.other == other):
                return jn.joint.m_collideConnected == False
            jn = jn.next
        return False

    def Freeze(self):
        self.m_flags |= b2Body.e_frozenFlag
        self.m_linearVelocity.SetZero()
        self.m_angularVelocity = 0.0
        s = self.m_shapeList
        while(s is not None):
            s.DestroyProxy()
            s = s.m_next
