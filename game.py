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
    def __init__(self,position = (0,0,0),scale = 2):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'circle',
            color = color.red,
            collider = 'circle',
            highlight_color = color.lime
            )

class gameButton(Button):
    def __init__(self,position = (0,0,0),text = "default"):
        super().__init__(
            parent = scene,
            icon = 'sword',
            position= position,
            scale = 0.5,
            color = color.gray,
            collider = 'circle',
            highlight_color = color.lime
            )
        def input(self,key):
            if self.hovered:
                if key == 'left mouse down':
                    text = Text(text = "fuck" ,scale = 10, position = (1,1,1))
        
class EnemyObject(Button):
    def __init__(self,position = (0,0,0),scale = (1,5,1)):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'cube',
            texture = 'white_cube',
            color = color.red,
            collider = 'box',
            highlight_color = color.blue
            )
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)



def update():
    if held_keys['r']:
        camera.fov += 1
    if held_keys['e']:
        camera.fov -= 1
        
app = Ursina()

window.title = 'Aiming game'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = True

side1 = LandObject(position = (0,25,50),scale= (100,50,1))
side2 = LandObject(position = (0,25,-50),scale= (100,50,1))
side3 = LandObject(position = (50,25,0),scale= (1,50,100))
side4 = LandObject(position = (-50,25,0),scale= (1,50,100))    
floor = LandObject(position = (0,0,0) )
ceiling = LandObject(position = (0,100,0) )

container1 = LandObject(position = (0,1,2),scale= (3.25,1.5,0.5))
container1 = LandObject(position = (0,1,-2),scale= (3.25,1.5,0.5))
container1 = LandObject(position = (2,1,0),scale= (0.5,1.5,3.25))
container1 = LandObject(position = (-2,1,0),scale= (0.5,1.5,3.25))

pole1 = LandObject(position = (2,1,2),scale= (0.5,7.5,0.5))
pole2 = LandObject(position = (-2,1,-2),scale= (0.5,7.5,0.5))
pole3 = LandObject(position = (-2,1,2),scale= (0.5,7.5,0.5))
pole4 = LandObject(position = (2,1,-2),scale= (0.5,7.5,0.5))


top = LandObject(position = (0,5,0),scale= (5,.5,5))

for x in range(20):
    target = targetObject(position =(random.uniform(-40,40),random.uniform(10,45),48))

for x in range(20):
    enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))

button1 = gameButton(position  = (1,1.25,1.7),text = "Horde")
button2 = gameButton(position  = (-1,1.25,1.7),text = "Sniper")
player = FirstPersonController()


camera.fov = 120

app.run()
