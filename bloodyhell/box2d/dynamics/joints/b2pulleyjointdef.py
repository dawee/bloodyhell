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


class b2PulleyJointDef(object):
        """
        inherit from "b2JointDef"
        """
Object.extend(b2PulleyJointDef.prototype, 

    def __init__(self):
        """
        TO FILL
        """
        self.type = b2Joint.e_unknownJoint
        self.userData = null
        self.body1 = null
        self.body2 = null
        self.collideConnected = false
        self.groundPoint1 = new b2Vec2()
        self.groundPoint2 = new b2Vec2()
        self.anchorPoint1 = new b2Vec2()
        self.anchorPoint2 = new b2Vec2()
        self.type = b2Joint.e_pulleyJoint
        self.groundPoint1.Set(-1.0, 1.0)
        self.groundPoint2.Set(1.0, 1.0)
        self.anchorPoint1.Set(-1.0, 0.0)
        self.anchorPoint2.Set(1.0, 0.0)
        self.maxLength1 = 0.5 * b2PulleyJoint.b2_minPulleyLength
        self.maxLength2 = 0.5 * b2PulleyJoint.b2_minPulleyLength
        self.ratio = 1.0
        self.collideConnected = true
    groundPoint1: new b2Vec2(),
    groundPoint2: new b2Vec2(),
    anchorPoint1: new b2Vec2(),
    anchorPoint2: new b2Vec2(),
    maxLength1: null,
    maxLength2: null,
    ratio: null)
