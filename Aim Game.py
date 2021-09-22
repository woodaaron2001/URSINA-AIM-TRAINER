from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from playsound import playsound
start_time = time.time()

game_time  = 60

class LandObject(Entity):
    def __init__(self,position = (0,0,0),scale = (100,1,100),texture = 'white_cube'):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'cube',
            texture = texture,
            color = color.white,
            collider = 'box'
            )

class targetObject(Button):
    def __init__(self,position = (0,0,0),scale = 2):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'square',
            texture = 'archery.png',
            collider = 'circle',
            highlight_color = color.lime
            )
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
                Audio('bell.mp3')
                
class gun(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'square',
            scale = 1,
            position= Vec2((0,0)),
            texture = 'white_cube'
            )
    def active(self):
            self.position = Vec2(0.3,-0.3)
    def passive(self):
            self.position = Vec2(0.4,-0.4)

class cameraText(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            scale = (1.147,0.122,1),
            position= Vec2((0,0.1)),
            texture = 'text.png'
            )



            
class gameButton(Button):
    def __init__(self,position = (0,0,0),text = "default"):
        super().__init__(
            parent = scene,
            icon = 'sword',
            position= position,
            scale = 0.5,
            highlight_color = color.lime
            )
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                
                if self == button1:
                    popup_Text1 = Text("Kill zombies before they hit base!",position = (-0.5,0.5),scale = 2,color = color.black)
                    state = 2
                if self == button2:
                    popup_Text1 = Text("Sharpshooter: Hit the targets!",position = (-0.5,0.5),scale = 2,color = color.black)
                    state = 3
                start_time = time.time()
                popup_seconds = Text(text = game_time, position = (0.45,0.5),scale = 2,color = color.black)
                popup_text2 = Text("Seconds Left!", position = (0.5,0.5),scale = 2,color = color.black)
                destroy(button1)
                destroy(button2)
                Audio('bell.mp3')
                       
        
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
                Audio('death.mp3')



state = 0

#gun = gunCamera()

def update():

    
    global state
    if (state == 0):
        camera.x +=1 * time.dt
        
    
    if held_keys['#']:
        player = FirstPersonController(speed = 10, position = (0,35,0),fov= 150)
        destroy(introScreen)
        state += 1
        
    
    if held_keys['r']:
        camera.fov += 1
        
    if held_keys['e']:
        camera.fov -= 1
        
    if(state > 1):
        print("wow")
        popup_seconds = Text(str(60 - (time.time()-start_time)), position = (0.45,0.5),scale = 2,color = color.black)
        destroy(popup_seconds)
        
            
        
app = Ursina()


window.title = 'Aiming game'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = True



camera.fov = 120
camera.x = -20
camera.y = 30
camera.z = -40

introScreen = cameraText()
side1 = LandObject(position = (0,25,50),scale= (100,50,1),texture = 'wood.jpg')
side2 = LandObject(position = (0,25,-50),scale= (100,50,1),texture = 'wood.jpg')
side3 = LandObject(position = (50,25,0),scale= (1,50,100),texture = 'wood.jpg')
side4 = LandObject(position = (-50,25,0),scale= (1,50,100),texture = 'wood.jpg')    
floor = LandObject(position = (0,0,0),texture ='floor.jpg')
ceiling = LandObject(position = (0,50,0) )

container1 = LandObject(position = (0,1,2),scale= (3.25,30,0.5),texture = 'wood.jpg')
container2 = LandObject(position = (0,1,-2),scale= (3.25,30,0.5),texture = 'wood.jpg')
container3 = LandObject(position = (2,1,0),scale= (0.5,30,3.25),texture = 'wood.jpg')
container4 = LandObject(position = (-2,1,0),scale= (0.5,30,3.25),texture = 'wood.jpg')
containerFloor = LandObject(position = (0,15,0),scale= (5,0.5,5),texture = 'wood.jpg')

pole1 = LandObject(position = (2,1,2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole2 = LandObject(position = (-2,1,-2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole3 = LandObject(position = (-2,1,2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole4 = LandObject(position = (2,1,-2),scale= (0.5,43,0.5),texture = 'black.jpg')

Audio('mem.mp3')
top = LandObject(position = (0,22,0),scale= (5,0.5,5),texture = 'black.jpg')

target = targetObject(position =(random.uniform(-40,40),random.uniform(10,45),0))

enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))

button1 = gameButton(position  = (1,16,1.7),text = "Horde")
button2 = gameButton(position  = (-1,16,1.7),text = "Sniper")

button1.tooltip = Tooltip('Game 1: Sniper Slow shooting game with smaller targets')
button2.tooltip = Tooltip('Game 2: Hit as many targets as possible before entitys get too close to the tower')

Object = Entity(model = 'square', scale = (10,1),texture = 'text.png',position =  (20,20,20))



app.run()
