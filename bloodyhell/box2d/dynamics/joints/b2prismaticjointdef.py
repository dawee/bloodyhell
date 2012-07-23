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


class b2PrismaticJointDef(object):
        """
        inherit from "b2JointDef"
        """
Object.extend(b2PrismaticJointDef.prototype, 

    def __init__(self):
        """
        TO FILL
        """
        self.type = b2Joint.e_unknownJoint
        self.userData = null
        self.body1 = null
        self.body2 = null
        self.collideConnected = false
        self.type = b2Joint.e_prismaticJoint
        self.anchorPoint = new b2Vec2(0.0, 0.0)
        self.axis = new b2Vec2(0.0, 0.0)
        self.lowerTranslation = 0.0
        self.upperTranslation = 0.0
        self.motorForce = 0.0
        self.motorSpeed = 0.0
        self.enableLimit = false
        self.enableMotor = false
    anchorPoint: null,
    axis: null,
    lowerTranslation: null,
    upperTranslation: null,
    motorForce: null,
    motorSpeed: null,
    enableLimit: null,
    enableMotor: null)
