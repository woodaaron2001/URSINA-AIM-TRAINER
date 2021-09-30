from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from playsound import playsound

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
                if self == button2:
                    state.sharpShooter()
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
              scale = 0.4,
              position = Vec3(0.6,-0.5,1.4),
              rotation = Vec3(0,270,0),
              model = 'ak_47.blend',
              texture = 'black.jpg',
              visible = True)

        self.handKnife = Entity(
              parent = self.controller,
              scale = (0.1,1,1),
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
        if key == 't' and state.state != 0:
            self.controller = FirstPersonController(speed = 10, position = (0,18,0))
        if key == '#' and state.state == 0:
            state.updateState(1)
            state.chooseOption()
            self.controller = FirstPersonController(speed = 10, position = (0,18,0))
            self.controller.fov = 200
            PlayerT.hand_gun.fade_in(1,1)
            self.hand_gun.enabled == True
            self.Text.fade_out(0,duration = .5)
            
            
        if key == 'left mouse down' and self.current == 0 and state.state != 0:
            Audio('gun.mp3')
            self.hand_gun.position = Vec3(0.6,-0.4,1.4)
            Bullet(model = 'cube',
                   color= color.black,
                   scale = 0.1,
                   position = self.controller.camera_pivot.world_position,
                   rotation = self.controller.camera_pivot.world_rotation)
            

    def update(self):
        global timerText,start_time,timer
        if state.state == 0:
            camera.x +=2 * time.dt
        if held_keys['e']:
            camera.fov += 1
        if held_keys['r']:
            camera.fov -= 1
        if state.state == 3 or state.state == 4:
            destroy(timerText)
            timer =  (60-(time.time()-start_time))
            timerText = Text(text = f'Time remaining {timer:.2f}',background = True,position = (-0.5,0.45,0))
        if timer < 0.2 and (state.state == 3 or state.state == 4):
            state.winMode()
        if  state.hitpoints  == 0 and state.state == 3:
            state.loseMode()
        
            
    def switch_weapon(self):
        for i,v in enumerate(self.weapons):
             if i == self.current:
                 v.fade_in(1,duration =.1)
             else:
                 v.fade_out(1,duration =.1)
            

class Bullet(Entity):
    
    def __init__ (self,speed = 20, lifetime = 5, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()
    def update(self):
        
        ray = raycast(self.world_position, self.forward,distance = self.speed)
        if not ray.hit and time.time() - self.start < self.lifetime:
            self.world_position +=self.forward * self.speed
        else:
            
            if str(ray.entity) == 'render/scene/enemy_object':
                destroy(ray.entity)
                state.entitys.remove(ray.entity)
                Audio('death.mp3')
            if str(ray.entity) == 'render/scene/target_object':
                global hitPointText
                destroy(ray.entity)
                state.hitpoints += 1
                state.entitys.remove(ray.entity)
                hitPointText.y =-2
                hitPointText = Text(text = f'SCORE: {state.hitpoints}',background =True,position = (-0.1,-0.45,0))
                Audio('bell.mp3')
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

        self.entitys.clear()
    def sharpShooter(self):
        global uiText,timerText,hitPointText,timer,start_time
        self.state = 4
        self.hitpoints = 0
        timer = 60
        start_time = time.time()
        uiText.y =-2
        hitPointText.y =-2
        timerText.y =-2
        uiText = Text(text = f'HIT AS MANY TARGETS BEFORE TIME RUNS OUT',background = True,position = (0,0.45,0))
        hitPointText = Text(text = f'SCORE: {self.hitpoints}',background =True,position = (-0.1,-0.45,0))
        timerText = Text(text = f'Time remaining {timer}',background = True,position = (-0.45,0.45,0))

        for x in range (10):
            target = TargetObject(position =(random.uniform(-40,40),random.uniform(3,40),48))
            self.entitys.append(target)
        
    def hordeMode(self):
        global uiText,timerText,hitPointText,timer,start_time
        self.hitpoints = 20
        
        timer = 60
        start_time = time.time()
        
        self.state = 3
        uiText.y =-2
        hitPointText.y =-2
        timerText.y =-2
        uiText = Text(text = f'DEFEND THE TOWER BEFORE HITPOINTS RUN OUT',background = True,position = (0,0.45,0))
        hitPointText = Text(text = f'Hitpoints: {self.hitpoints}',background =True,position = (-0.1,-0.45,0))
        timerText = Text(text = f'Time remaining {timer}',background = True,position = (-0.45,0.45,0))

        for x in range (10):
            enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))
            self.entitys.append(enemy)
    def loseMode(self):
        global uiText,timerText,hitPointText,timer,start_time,button1,button2
        for x in range (len(self.entitys)):
            destroy(self.entitys[x])
        state.entitys.clear()
            
        self.state = 5
        uiText.y -= 2
        hitPointText.y -= 2
        timerText.y -= 2
        print("In lost")
        uiText = Text(text = f'YOU LOST!!! CLICK ANOTHER BUTTON TO PLAY AGAIN',background = True,position = (-0.2,0.45,0))

        button1 = gameButton(position  = (1,16,1.7),text = "Horde")
        button2 = gameButton(position  = (-1,16,1.7),text = "Sniper")
        button1.tooltip = Tooltip('Game 1: Sniper Slow shooting game with smaller targets')
        button2.tooltip = Tooltip('Game 2: Hit as many targets as possible before entitys get too close to the tower')

    
        
    def winMode(self):
        global uiText,timerText,hitPointText,timer,start_time, button1,button2
        self.state = 5
        uiText.y -= 2
        hitPointText.y -= 2
        timerText.y -= 2
        
        uiText = Text(text = f'YOU WON!!! CLICK ANOTHER BUTTON TO PLAY AGAIN',background = True,position = (-0.2,0.45,0))

        button1 = gameButton(position  = (1,16,1.7),text = "Horde")
        button2 = gameButton(position  = (-1,16,1.7),text = "Sniper")
        button1.tooltip = Tooltip('Game 1: Sniper Slow shooting game with smaller targets')
        button2.tooltip = Tooltip('Game 2: Hit as many targets as possible before entitys get too close to the tower')
        
        for x in range (len(self.entitys)):
            destroy(self.entitys[x])
        state.entitys.clear()

class TargetObject(Button):
    def __init__(self,position = (0,0,0),scale = 4,mode = 'random'):

        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'circle',
            texture = 'archery.png',
            collider = 'box',
            highlight_color = color.black
            )
        self.mode = mode
        
    def update(self):
        global hitPointText



        if state.state == 4:
            if len(state.entitys) < 10:
                enemy = TargetObject(position =(random.uniform(-40,40),random.uniform(3,40),48))
                state.entitys.append(enemy)


                                
        
class EnemyObject(Button):
    def __init__(self,position = (0,0,0),scale = 1,mode = 'random'):

        super().__init__(
            parent = scene,
            position= position,
            scale = scale,
            model = 'sphere',
            texture = 'black.jpg',
            color = color.black,
            collider = 'box'
            )
        self.mode = mode
        
    def update(self):
        global hitPointText



        if state.state == 3:
            if len(state.entitys) < 10:
                enemy = EnemyObject(position =(random.uniform(-40,40),2.5,random.uniform(0,50)))
                state.entitys.append(enemy)

       # print(len(state.entitys))
        if state.state == 4:
            self.x += random.uniform(-0.01,0.01)
            self.z += random.uniform(-0.01,0.01)
        else:
            if self.x > 0:
                self.x -= 0.03
            if self.x < 0:
                self.x += 0.03
            if self.z > 0:
                self.z -= 0.03
            if self.z < 0:
                self.z += 0.03
            if self.x < 4.0:
                if self.x > -4.0:
                    if self.z > -4.0:
                        if self.z < 4.0:
                            
                            state.hitpoints -= 1
                            destroy(self)
                            state.entitys.remove(self)
                            if(state.state != 0):
                                hitPointText.y =-2
                                hitPointText = Text(text = f'Hitpoints: {state.hitpoints}',background =True,position = (-0.1,-0.45,0))
                                

            
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
timer = 60
start_time = 0
PlayerT = Player()
PlayerT.hand_gun.fade_out(0,0.001)
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

timer = 0

uiText = Text(text = "")
timerText= Text(text = "")
hitPointText = Text(text = "")

button1 = gameButton(position  = (1,16,1.7),text = "Horde")
button2 = gameButton(position  = (-1,16,1.7),text = "Sniper")

button1.tooltip = Tooltip('Game 1: Sniper Slow shooting game with smaller targets')
button2.tooltip = Tooltip('Game 2: Hit as many targets as possible before entitys get too close to the tower')

Audio('background.wav',loop = True)
app.run()
