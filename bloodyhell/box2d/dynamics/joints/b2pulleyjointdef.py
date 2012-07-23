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

from box2d.dynamics.joints.b2joint import b2Joint
from box2d.dynamics.joints.b2jointdef import b2JointDef
from box2d.dynamics.joints.b2pulleyjoint import b2PulleyJoint
from box2d.common.math.b2vec2 import b2Vec2


class b2PulleyJointDef(b2JointDef):

    def __init__(self):
        self.type = b2Joint.e_unknownJoint
        self.userData = None
        self.body1 = None
        self.body2 = None
        self.collideConnected = False
        self.groundPoint1 = b2Vec2()
        self.groundPoint2 = b2Vec2()
        self.anchorPoint1 = b2Vec2()
        self.anchorPoint2 = b2Vec2()
        self.type = b2Joint.e_pulleyJoint
        self.groundPoint1.Set(-1.0, 1.0)
        self.groundPoint2.Set(1.0, 1.0)
        self.anchorPoint1.Set(-1.0, 0.0)
        self.anchorPoint2.Set(1.0, 0.0)
        self.maxLength1 = 0.5 * b2PulleyJoint.b2_minPulleyLength
        self.maxLength2 = 0.5 * b2PulleyJoint.b2_minPulleyLength
        self.ratio = 1.0
        self.collideConnected = True
