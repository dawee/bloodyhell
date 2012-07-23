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


class b2Joint(object):

    def GetType(self):
        """
        TO FILL
        """
        return self.m_type

    def GetAnchor1(self):
        """
        TO FILL
        """
return null
,    GetAnchor2: function()
return null

    def GetReactionForce(self,invTimeStep):
        """
        TO FILL
        """
return null
,    GetReactionTorque: function(invTimeStep)
return 0.0

    def GetBody1(self):
        """
        TO FILL
        """
        return self.m_body1

    def GetBody2(self):
        """
        TO FILL
        """
        return self.m_body2

    def GetNext(self):
        """
        TO FILL
        """
        return self.m_next

    def GetUserData(self):
        """
        TO FILL
        """
        return self.m_userData

    def __init__(self,def):
        """
        TO FILL
        """
        self.m_node1 = new b2JointNode()
        self.m_node2 = new b2JointNode()
        self.m_type = def.type
        self.m_prev = null
        self.m_next = null
        self.m_body1 = def.body1
        self.m_body2 = def.body2
        self.m_collideConnected = def.collideConnected
        self.m_islandFlag = false
        self.m_userData = def.userData

    def PrepareVelocitySolver(self):
        """
        TO FILL
        """
,    SolveVelocityConstraints: function(step)

    def PreparePositionSolver(self):
        """
        TO FILL
        """
,    SolvePositionConstraints: function()
return false
    m_type: 0,
    m_prev: null,
    m_next: null,
    m_node1: new b2JointNode(),
    m_node2: new b2JointNode(),
    m_body1: null,
    m_body2: null,
    m_islandFlag: null,
    m_collideConnected: null,
    m_userData: null
b2Joint.Create = function(def, allocator)
        joint = null
        switch (def.type)
        case b2Joint.e_distanceJoint:
                joint = new b2DistanceJoint(def)
            break
        case b2Joint.e_mouseJoint:
                joint = new b2MouseJoint(def)
            break
        case b2Joint.e_prismaticJoint:
                joint = new b2PrismaticJoint(def)
            break
        case b2Joint.e_revoluteJoint:
                joint = new b2RevoluteJoint(def)
            break
        case b2Joint.e_pulleyJoint:
                joint = new b2PulleyJoint(def)
            break
        case b2Joint.e_gearJoint:
                joint = new b2GearJoint(def)
            break
        default:
            break
        return joint
b2Joint.Destroy = function(joint, allocator)
        """joint->~b2Joint()
        switch (joint.m_type)
        case b2Joint.e_distanceJoint:
            allocator->Free(joint, sizeof(b2DistanceJoint))
            break
        case b2Joint.e_mouseJoint:
            allocator->Free(joint, sizeof(b2MouseJoint))
            break
        case b2Joint.e_prismaticJoint:
            allocator->Free(joint, sizeof(b2PrismaticJoint))
            break
        case b2Joint.e_revoluteJoint:
            allocator->Free(joint, sizeof(b2RevoluteJoint))
            break
        case b2Joint.e_pulleyJoint:
            allocator->Free(joint, sizeof(b2PulleyJoint))
            break
        case b2Joint.e_gearJoint:
            allocator->Free(joint, sizeof(b2GearJoint))
            break
        default:
            b2Assert(false)
            break
        """
b2Joint.e_unknownJoint = 0
b2Joint.e_revoluteJoint = 1
b2Joint.e_prismaticJoint = 2
b2Joint.e_distanceJoint = 3
b2Joint.e_pulleyJoint = 4
b2Joint.e_mouseJoint = 5
b2Joint.e_gearJoint = 6
b2Joint.e_inactiveLimit = 0
b2Joint.e_atLowerLimit = 1
b2Joint.e_atUpperLimit = 2
b2Joint.e_equalLimits = 3
