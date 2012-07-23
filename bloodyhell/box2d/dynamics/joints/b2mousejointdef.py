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


class b2MouseJointDef(object):
        """
        inherit from "b2JointDef"
        """
Object.extend(b2MouseJointDef.prototype, 

    def __init__(self):
        """
        TO FILL
        """
        self.type = b2Joint.e_unknownJoint
        self.userData = null
        self.body1 = null
        self.body2 = null
        self.collideConnected = false
        self.target = new b2Vec2()
        self.type = b2Joint.e_mouseJoint
        self.maxForce = 0.0
        self.frequencyHz = 5.0
        self.dampingRatio = 0.7
        self.timeStep = 1.0 / 60.0
    target: new b2Vec2(),
    maxForce: null,
    frequencyHz: null,
    dampingRatio: null,
    timeStep: null)
