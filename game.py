from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class PlayerMonke(Entity):
    def __init__(self):
        super().__init__(
            model = 'quad',
            texture = '/monke.png',
            
            )

class LandObject(Entity):
    def __init__(self,position = (0,0,0)):
        super().__init__(
            parent = scene,
            position= position,
            scale = 0.5,
            model = 'cube',
            texture = 'white_cube',
            color = color.white,
            collider = 'box'
            )
class RopeObject(Entity):
    def __init__(self,position = (5,5,5)):
        super().__init__(
            parent = scene,
            position= position,
            model = 'cube',
            color = color.green,
            collider = 'box'
            )

def update():
    if held_keys['r']:
        camera.fov += 1
    if held_keys['e']:
        camera.fov -= 1
    if held_keys['f']:
        Rope = RopeObject()

        #create a swing/robe object which originates at players origin and 

        
app = Ursina()

window.title = 'Monke'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = True

#use some noise calculation for generating a random terrain 
for z in range(30):
    for x in range(30):
        land = LandObject(position = (x/2,random.uniform(0,0.5),z/2))
        
        

player = FirstPersonController()
camera.fov = 120

app.run()
