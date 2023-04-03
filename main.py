# Rights Reserved to Kynan Schubert of Noss69420@gmail.com

from ursina import *
from direct.actor.Actor import Actor
import threading
import os
app = Ursina(borderless=False)

window.size = window.fullscreen

#Player Declarations
running = True
selectedpos = []
selected = False
actor = Actor("Assets/BaseMesh_Anim.gltf")
playerSpeed = 0.001

entity.rotation_y = -90

class character(Entity):
    def __init__(self):
        super().__init__(
            model=actor,
            scale=(.003,.003,.003),
            color=color.white,
            position=(0, 0, 0),
            origin=(0,0,0),
            rotationy=-90,
            collider='box'
        )

player = character()
player.rotation_y = -90


floorX = 20
floorY = 3
floorZ = 5

spawn = (floorX/5,5,floorZ/2)
camSpawn = (floorX/5-20,10,floorZ/2-.5)

scoreboard = Text()
scoreboard.color = color.black
scoreboard.origin = (-1,-1)
scoreboard.position = (0,0)


#Set Camera and Player position
camera.world_position = camSpawn
player.world_position = spawn
player.collider = BoxCollider(player, center=Vec3(0,0,0), size=Vec3(1,1,1))

class Voxel(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            scale=(1, 1, 1),
            position = position,
            model = 'cube',
            origin = (0,0,0),
            texture = 'white_cube',
            color = color.white,
            collider= 'box'
        )

class AngeryCubes(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            scale=(1,1,1),
            position = position,
            model = 'cube',
            origin = (0,0,0),
            texture = 'white_cube',
            color = color.gray,
            collider = 'box',
        )
voxelground = []
for x in range(floorX):
    for z in range(floorZ):
        for y in range(floorY):
            voxelground.append(Voxel(position=(x,-y,z)))
bcX = round(floorX/5) - 1
bcY = 1
bcZ = floorZ
badcubes = []

for x in range(bcX):
    for z in range(bcZ):
        for y in range(bcY):
            badcubes.append(AngeryCubes(position=(floorX - x ,1,z)))

FrameAnimation3d(actor)



def cuberoll():
    score = 0
    while running:
        scoreboard.text = str(score)
        if len(badcubes) > 0:
            for y in range(10):
                for x in range(len(badcubes)):
                    badcubes[x].x -= 0.1
                    badcubes[x].rotation_z -= 90/10
                time.sleep(0.1)
            edgeCube = [entity for entity in badcubes if entity.x < -1]

            if edgeCube:
                for c in range(2):
                    for z in range(len(edgeCube)):
                        for h in range(2):
                            edgeCube[z].y -= 0.3
                            time.sleep(0.000001)
                            for m in range(len(edgeCube)):
                                edgeCube[m].y -= 0.5
                            time.sleep(0.000001)
                time.sleep(1)
                score -= len(edgeCube)
                print(score)
                for i in range(len(edgeCube)):
                    destroy(badcubes[0])
                    badcubes.pop(0)
                edgeCube.clear()

            for b in range(10):
                for a in range(len(badcubes)):
                    deletCube = [entity for entity in voxelground if entity.color == color.red]
                    if deletCube:
                        print("found")
                        print(deletCube)
                        print(badcubes)
                        if a < len(badcubes):
                            if round(badcubes[a].x) == deletCube[0].x:
                                print("found X")
                                if round(badcubes[a].z) == deletCube[0].z:
                                    print("pop")
                                    destroy(badcubes[a])
                                    badcubes.pop(a)
                                    score += 2
                                    print(score)
                if not held_keys["shift"]:
                    time.sleep(0.1)
            else:
                    time.sleep(0.1)

        else:
            time.sleep(1)
            print(score)
            print("done")
            for x in range(bcX):
                for z in range(bcZ):
                    for y in range(bcY):
                        badcubes.append(AngeryCubes(position=(floorX - x, 1, z)))



def cubeselection():
    while running:
        if held_keys['space']:
            playerpos = [entity for entity in voxelground if entity.position == (round(player.x - 0.001), 0, round(player.z))]
            selectedpos = [entity for entity in voxelground if entity.color == color.green]
            if selectedpos:
                selectedpos[0].color = color.red
                time.sleep(0.5)
                selectedpos[0].color = color.white
            else:
                playerpos[0].color = color.green
                time.sleep(0.2)

        time.sleep(0.001)

def playercontrols():
    while running:
        #Test If Player is touching anything
        playercol2 = player.intersects().entities

        #On Success
        if len(playercol2) > 0:
            #play Idle Animation named
            actor.loop("idle")

            # player + camera movement
            if held_keys['d']:
                player.z -= playerSpeed
                camera.z -= playerSpeed * 2

            if held_keys['a']:
                player.z += playerSpeed
                camera.z += playerSpeed * 2

            if held_keys['s']:
                player.x -= playerSpeed
                camera.x -= playerSpeed * 1.5
                camera.y -= playerSpeed

            if held_keys['w']:
                player.x += playerSpeed
                camera.x += playerSpeed * 1.5
                camera.y += playerSpeed

            # player rotation
            if held_keys['a'] & held_keys['w']:
                player.rotation_y = -135
            else:
                if held_keys['a']:
                    player.rotation_y = -180
                if held_keys['d']:
                    player.rotation_y = 0
                if held_keys['w']:
                    player.rotation_y = -90
                if held_keys['s']:
                    player.rotation_y = 90
            if held_keys['a'] & held_keys['s']:
                player.rotation_y = 135
            if held_keys['d'] & held_keys['w']:
                player.rotation_y = -45
            if held_keys['d'] & held_keys['s']:
                player.rotation_y = 45

            # On Enemy Collision
            if len(playercol2) > 1:
                for x in range(len(playercol2)):
                    if str(playercol2[x]) == "angery_cubes":
                        for z in range(10):
                            player.x -= playerSpeed*100
                            camera.x -= playerSpeed*100
                            camera.y -= playerSpeed*50
                            time.sleep(0.01)
        # On Failure
        else:
            player.y -= playerSpeed*4

    time.sleep(0.2)


selectcube = threading.Thread(target=cubeselection)
playercont = threading.Thread(target=playercontrols)
cubeplay = threading.Thread(target=cuberoll)


def update():

    if player.y < -10:
        camera.world_position = (player.x - 5, player.y + 5, player.z)
    if player.y < -50:
        player.world_position = spawn
        camera.world_position = camSpawn

    player.color = color.pink

    camera.look_at(player)

    time.sleep(0.0001)



selectcube.start()
playercont.start()
cubeplay.start()
app.run()
running == False