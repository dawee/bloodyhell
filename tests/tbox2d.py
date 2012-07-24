import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from bloodyhell.box2d.collision.b2aabb import b2AABB
from bloodyhell.box2d.collision.shapes.b2boxdef import b2BoxDef
from bloodyhell.box2d.dynamics.b2world import b2World
from bloodyhell.box2d.dynamics.b2bodydef import b2BodyDef

from bloodyhell.box2d.common.math.b2vec2 import b2Vec2


def createBox(world):
    sd = b2BoxDef()
    sd.density = 1.0
    sd.extents.Set(10, 10)
    bd = b2BodyDef()
    bd.AddShape(sd)
    bd.position.Set(0.0, 10.0)
    return world.CreateBody(bd)


def createGround(world):
    groundSd = b2BoxDef()
    groundSd.extents.Set(1000, 10)
    groundBd = b2BodyDef()
    groundBd.AddShape(groundSd)
    groundBd.position.Set(0, -10)
    return world.CreateBody(groundBd)


def run():
    worldAABB = b2AABB()
    worldAABB.minVertex.Set(-1000, -1000)
    worldAABB.maxVertex.Set(1000, 1000)
    gravity = b2Vec2(0, -9.8)
    world = b2World(worldAABB, gravity, True)
    createGround(world)
    box = createBox(world)
    for index in range(50):
        world.Step(0.04, 1)
        print box.GetCenterPosition().x, box.GetCenterPosition().y

if __name__ == '__main__':
    run()
