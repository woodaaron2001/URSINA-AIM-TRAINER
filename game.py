from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class LandObject(Entity):
    def __init__(self,position = (0,0,0),scale = (100,1,100)):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'cube',
            texture = 'white_cube',
            color = color.white,
            collider = 'box'
            )
    
class targetObject(Button):
    def __init__(self,position = (0,0,0)):
        super().__init__(
            parent = scene,
            position= position,
            scale = 2,
            model = 'circle',
            color = color.gray,
            collider = 'circle',
            highlight_color = color.lime
            )

class EnemyObject(Entity):
    def __init__(self,position = (0,0,0),scale = (100,1,100)):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'cube',
            texture = 'white_cube',
            color = color.white,
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

window.title = 'Aiming game'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = True

land1 = LandObject(position = (0,0,0))

land2 = LandObject(position = (0,50,0))

side1 = LandObject(position = (0,25,50),scale= (100,50,1))

side2 = LandObject(position = (0,25,-50),scale= (100,50,1))

side3 = LandObject(position = (50,25,0),scale= (1,50,100))

side4 = LandObject(position = (-50,25,0),scale= (1,50,100))    



container1 = LandObject(position = (0,1,2),scale= (3.25,2,0.5))
container1 = LandObject(position = (0,1,-2),scale= (3.25,2,0.5))
container1 = LandObject(position = (2,1,0),scale= (0.5,2,3.25))
container1 = LandObject(position = (-2,1,0),scale= (0.5,2,3.25))

pole1 = LandObject(position = (2,1,2),scale= (0.5,5,0.5))
pole2 = LandObject(position = (-2,1,-2),scale= (0.5,5,0.5))
pole3 = LandObject(position = (-2,1,2),scale= (0.5,5,0.5))
pole4 = LandObject(position = (2,1,-2),scale= (0.5,5,0.5))

top = LandObject(position = (0,5,0),scale= (1,1,1))
for x in range(20):
    target = targetObject(position =(random.uniform(-40,40),random.uniform(10,45),48))
    
player = FirstPersonController()
camera.fov = 120

app.run()
