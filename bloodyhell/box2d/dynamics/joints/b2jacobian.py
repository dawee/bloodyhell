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


class b2Jacobian(object):
    linear1: new b2Vec2(),
    angular1: null,
    linear2: new b2Vec2(),
    angular2: null,

    def SetZero(self):
        """
        TO FILL
        """
        self.linear1.SetZero() self.angular1 = 0.0
        self.linear2.SetZero() self.angular2 = 0.0

    def Set(self,x1, a1, x2, a2):
        """
        TO FILL
        """
        self.linear1.SetV(x1) self.angular1 = a1
        self.linear2.SetV(x2) self.angular2 = a2

    def Compute(self,x1, a1, x2, a2):
        """
        TO FILL
        """
        return (self.linear1.x*x1.x + self.linear1.y*x1.y) + self.angular1 * a1 + (self.linear2.x*x2.x + self.linear2.y*x2.y) + self.angular2 * a2

    def __init__(self):
        """
        TO FILL
        """
        self.linear1 = new b2Vec2()
        self.linear2 = new b2Vec2()
