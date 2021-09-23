from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from playsound import playsound
start_time = time.time()

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
                    state.hordeMode()
            destroy(button1)
            destroy(button2)  
            Audio('bell.mp3')

class Player(Entity):
    def __init__(self,**kwargs):
        camera.fov = 120
        camera.x = -20
        camera.y = 30
        camera.z = -40
        self.controller = camera
        super().__init__(parent = self.controller)

        self.Text= Entity(
         parent = camera.ui,
            model = 'cube',
            scale = (1.147,0.5,1),
            position= Vec2((0,0.1)),
            texture = 'text.png',
            visibile = True
         )
        self.hand_gun = Entity(
              parent = self.controller,
              scale = 0.1,
              position = Vec3(0.6,-0.5,1.4),
              rotation = Vec3(0,170,0),
              model = 'cube',
              texture = 'white_cube',
              visible = True)

        self.handKnife = Entity(
              parent = self.controller,
              scale = 0.3,
              position = Vec3(0.6,-1,1.4),
              rotation = Vec3(0,170,0),
              model = 'cube',
              texture = 'white_cube',
              visible = False,
              color = color.red
              )
          
        self.weapons = [self.hand_gun,self.handKnife]
        self.current = 0
        self.switch_weapon()

    def input(self,key):
        if key == 'scroll up':
            self.current = self.current + 1 %2
            self.switch_weapon()
        if key == '#':
            state.updateState(1)
            state.chooseOption()
            self.controller = FirstPersonController(speed = 10, position = (0,35,0))
            self.controller.fov = 200
            self.hand_gun.enabled == True
            self.Text.fade_out(0,duration = .5)
            
            
        if key == 'left mouse down' and self.current == 0:
            Audio('gun.mp3')
            Bullet(model = 'sphere',
                   color= color.black,
                   scale = 0.1,
                   position = self.controller.camera_pivot.world_position,
                   rotation = self.controller.camera_pivot.world_rotation)

    def update(self):
        if state.state == 0:
            camera.x +=2 * time.dt
        if held_keys['e']:
            camera.fov += 1
        if held_keys['r']:
            camera.fov -= 1
        #self.controller.camera_pivot.y = 2-held_keys['left control']
        
            
    def switch_weapon(self):
        for i,v in enumerate(self.weapons):
             if i == self.current:
                 v.fade_in(1,duration =.1)
             else:
                 v.fade_out(1,duration =.1)
            

class Bullet(Entity):
    def __init__ (self,speed = 300, lifetime = 5, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()
    def update(self):
        ray = raycast(self.world_position, self.forward,distance = self.speed*time.dt)
        if not ray.hit and time.time() - self.start < self.lifetime:
            self.world_position +=self.forward * self.speed * time.dt
        else:
            
            if str(ray.entity) == 'render/scene/enemy_object':
                destroy(ray.entity)
                Audio('death.mp3')
            destroy(self)
                
                
           
        
class State:
    def __init__(self,state):
        self.state = state
        self.hitpoints = 19
        self.entitys = []
        

    def updateState(self,state):
        self.state = state

    def introScreen(self):
        for x in range (20):
            enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))
            self.entitys.append(enemy)
    def chooseOption(self):
        for x in range (len(self.entitys)):
            destroy(self.entitys[x])

    def hordeMode(self):
          for x in range (len(self.entitys)):
            enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))
            self.entitys.append(enemy)
    def loseMode(self):
        print("You lose")
        for x in range (len(self.entitys)):
            destroy(self.entitys[x])

        
class EnemyObject(Button):
    def __init__(self,position = (0,0,0),scale = 1,mode = 'random'):

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
        self.mode = mode
        
    def update(self):
        if state.state == 4:
            self.x += random.uniform(-0.25,0.25)
            self.z += random.uniform(-0.25,0.25)
        else:
            if self.x > 0:
                self.x -= 0.1
            if self.x < 0:
                self.x += 0.1
            if self.z > 0:
                self.z -= 0.1
            if self.z < 0:
                self.z += 0.1
            if self.x < 4.0:
                if self.x > -4.0:
                    if self.z > -4.0:
                        if self.z < 4.0:
                            state.hitpoints -= 1
                            print(state.hitpoints)
                            destroy(self)

            
class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = 'sky_texture',
			scale = 200,
			double_sided = True)
app = Ursina()

state = State(0)
state.introScreen()

PlayerT = Player()
side1 = LandObject(position = (0,25,50),scale= (100,50,1),texture = 'wall.jpg')
side2 = LandObject(position = (0,25,-50),scale= (100,50,1),texture = 'wall.jpg')
side3 = LandObject(position = (50,25,0),scale= (1,50,100),texture = 'wall.jpg')
side4 = LandObject(position = (-50,25,0),scale= (1,50,100),texture = 'wall.jpg')    
floor = LandObject(position = (0,0,0),texture ='floor.jpg')
#ceiling = LandObject(position = (0,50,0),texture = 'sky.jpg' )

container1 = LandObject(position = (0,1,2),scale= (3.25,30,0.5),texture = 'wood.jpg')
container2 = LandObject(position = (0,1,-2),scale= (3.25,30,0.5),texture = 'wood.jpg')
container3 = LandObject(position = (2,1,0),scale= (0.5,30,3.25),texture = 'wood.jpg')
container4 = LandObject(position = (-2,1,0),scale= (0.5,30,3.25),texture = 'wood.jpg')
containerFloor = LandObject(position = (0,15,0),scale= (5,0.5,5),texture = 'wood.jpg')

pole1 = LandObject(position = (2,1,2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole2 = LandObject(position = (-2,1,-2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole3 = LandObject(position = (-2,1,2),scale= (0.5,43,0.5),texture = 'black.jpg')
pole4 = LandObject(position = (2,1,-2),scale= (0.5,43,0.5),texture = 'black.jpg')
top = LandObject(position = (0,22,0),scale= (5,0.5,5),texture = 'black.jpg')

Sky = Sky()


button1 = gameButton(position  = (1,16,1.7),text = "Horde")
button2 = gameButton(position  = (-1,16,1.7),text = "Sniper")

button1.tooltip = Tooltip('Game 1: Sniper Slow shooting game with smaller targets')
button2.tooltip = Tooltip('Game 2: Hit as many targets as possible before entitys get too close to the tower')

app.run()
