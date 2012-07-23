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

from box2d.dynamics.joints.b2jointnode import b2JointNode


class b2Joint(object):

    e_unknownJoint = 0
    e_revoluteJoint = 1
    e_prismaticJoint = 2
    e_distanceJoint = 3
    e_pulleyJoint = 4
    e_mouseJoint = 5
    e_gearJoint = 6
    e_inactiveLimit = 0
    e_atLowerLimit = 1
    e_atUpperLimit = 2
    e_equalLimits = 3

    def GetType(self):
        return self.m_type

    def GetAnchor1(self):
        return None

    def GetAnchor2(self):
        return None

    def GetReactionForce(self, invTimeStep):
        return None

    def GetReactionTorque(self, invTimeStep):
        return 0.0

    def GetBody1(self):
        return self.m_body1

    def GetBody2(self):
        return self.m_body2

    def GetNext(self):
        return self.m_next

    def GetUserData(self):
        return self.m_userData

    def __init__(self, definition):
        self.m_node1 = b2JointNode()
        self.m_node2 = b2JointNode()
        self.m_type = definition.type
        self.m_prev = None
        self.m_next = None
        self.m_body1 = definition.body1
        self.m_body2 = definition.body2
        self.m_collideConnected = definition.collideConnected
        self.m_islandFlag = False
        self.m_userData = definition.userData

    def PrepareVelocitySolver(self):
        pass

    def SolveVelocityConstraints(self, step):
        pass

    def PreparePositionSolver(self):
        pass

    def SolvePositionConstraints(self):
        return False

    @staticmethod
    def Create(definition, allocator):
        from box2d.dynamics.joints.b2distancejoint import b2DistanceJoint
        from box2d.dynamics.joints.b2mousejoint import b2MouseJoint
        from box2d.dynamics.joints.b2prismaticjoint import b2PrismaticJoint
        from box2d.dynamics.joints.b2revolutejoint import b2RevoluteJoint
        from box2d.dynamics.joints.b2pulleyjoint import b2PulleyJoint
        from box2d.dynamics.joints.b2gearjoint import b2GearJoint
        joint = None
        if definition.type == b2Joint.e_distanceJoint:
            joint = b2DistanceJoint(definition)
        if definition.type == b2Joint.e_mouseJoint:
            joint = b2MouseJoint(definition)
        if definition.type == b2Joint.e_prismaticJoint:
            joint = b2PrismaticJoint(definition)
        if definition.type == b2Joint.e_revoluteJoint:
            joint = b2RevoluteJoint(definition)
        if definition.type == b2Joint.e_pulleyJoint:
            joint = b2PulleyJoint(definition)
        if definition.type == b2Joint.e_gearJoint:
            joint = b2GearJoint(definition)
        return joint

    @staticmethod
    def Destroy(joint, allocator):
        pass
