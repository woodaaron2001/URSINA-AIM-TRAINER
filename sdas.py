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
            texture = 'texts.png'
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
            self.controller = FirstPersonController(speed = 10, position = (0,35,0))
            self.controller.fov = 200
            self.hand_gun.visible == True
            
        if key == 'left mouse down' and self.current == 0:
            Audio('gun.mp3')
            Bullet(model = 'sphere',
                   color= color.black,
                   scale = 0.1,
                   position = self.controller.camera_pivot.world_position,
                   rotation = self.controller.camera_pivot.world_rotation)

    def update(self):
        if state.state == 0:
            camera.x +=1 * time.dt
            
        #self.controller.camera_pivot.y = 2-held_keys['left control']
        
            
    def switch_weapon(self):
        for i,v in enumerate(self.weapons):
             if i == self.current:
                 v.visible == True
             else:
                v.visible == False
            

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

            destroy(self)
            if ray.entity == EnemyObject:
               destroy(ray.entity)
               print("wow")
                
                
           
        
class State:
    def __init__(self,state):
        self.state = state

    def updateState(self,state):
        self.state = state

        
class EnemyObject(Button):
    def __init__(self,position = (0,0,0),scale = 1):
        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'cube',
            texture = 'white_cube',
            color = color.white,
            collider = 'box',
            highlight_color = color.blue
            )
    def update(self):
        if self.x > 0:
            self.x -= 0.1
        if self.x < 0:
            self.x += 0.1
        if self.z > 0:
            self.z -= 0.1
        if self.z < 0:
            self.z += 0.1            


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
print(state.state)
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

for x in range (500):
    enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))
    

app.run()
