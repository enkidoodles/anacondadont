# MODULES
import math
import random
import pyglet
from pyglet.gl import *

# WINDOW
window = pyglet.window.Window(800,600,visible=False, vsync=True)

# BATCHES
labels = pyglet.graphics.Batch()

# END GAME MESSAGE
condition_label_1 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 30, x = 300, y = 350, anchor_x = "center", anchor_y = "center", batch=labels)
condition_label_2 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 26, x = 300, y = 300, anchor_x = "center", anchor_y = "center", batch=labels)
condition_label_3 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 24, x = 300, y = 250, anchor_x = "center", anchor_y = "center", batch=labels)
pointcounter = pyglet.text.Label('0', font_name='Arial', font_size=24, x=700, y=540, anchor_x='center', anchor_y='center', batch=labels)

# SIDEBAR
buns_label = pyglet.text.Label('BUNS', font_name='Arial', font_size=15, x=700, y=575, anchor_x='center', anchor_y='center', batch=labels)

# LINES
labels.add(2, GL_LINES, None, ('v2i', (600,0, 600,600)))

# BACKGROUNDS
bg = pyglet.resource.image("grass.jpg")
bg.width, bg.height = 600, 600

# KEY STATE HANDLER
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

# INITIAL VARIABLES
states = []

# CLASSES FOR SPRITES
class Snake(pyglet.sprite.Sprite):

	def __init__(self):
	
		image = pyglet.resource.image('ball.png')
		image.width, image.height = 20, 40
		image.anchor_x = 10
		image.anchor_y = 30
		
		pyglet.sprite.Sprite.__init__(self, image)
		self.reset()
		
	def reset(self):
		
		self.points = 0
		
		self.rotation = 90
		direction = 0
		self.x, self.y = 300,300
		self.vx, self.vy = math.cos(direction)*150, math.sin(direction)*150

class House(pyglet.sprite.Sprite):
	
	def __init__(self):
		
		self.reset();
		
	def reset(self):
		
		self.a = random.randint(1,255)
		self.b = random.randint(1,255)
		self.c = random.randint(1,255)
		self.d = 255
		
		house_image = pyglet.image.SolidColorImagePattern((self.a,self.b,self.c,self.d))
		house_image = pyglet.image.create(100, 100, house_image)
		house_image.anchor_x, house_image.anchor_y = 0, 0
		
		pyglet.sprite.Sprite.__init__(self, house_image)
		
		self.x = random.choice([100,400,500])
		self.y = random.choice([100,400,500])

class Human(pyglet.sprite.Sprite):
	
	def __init__(self,speed):
		
		self.speed = speed
		
		if self.speed == 0:
			human_image = pyglet.resource.image("face" + str(random.randint(1,2)) + ".jpg")
		elif self.speed == 50:
			human_image = pyglet.resource.image("face" + str(random.randint(3,4)) + ".jpg")
		elif self.speed == 150:
			human_image = pyglet.resource.image("face" + str(random.randint(5,6)) + ".jpg")
		else:
			human_image = pyglet.resource.image("face" + str(random.randint(7,8)) + ".jpg")
		
		human_image.width, human_image.height = 24,24
		human_image.anchor_x, human_image.anchor_y = 12, 12
		
		pyglet.sprite.Sprite.__init__(self, human_image)
		self.reset();
	
	def reset(self):
	
		self.x, self.y = random.randint(1,11) * 50, random.randint(1,11) * 50
		
		while (house.x <= self.x <= house.x + 110) and (house.y <= self.y <= house.y + 110):
			self.x, self.y = random.randint(1,11) * 50, random.randint(1,11) * 50
		
		self.direction = random.random()*math.pi/2 + random.choice([-math.pi/4, 3*math.pi/4])
		self.vx, self.vy = math.cos(self.direction)*self.speed, math.sin(self.direction)*self.speed
		self.vx_holder, self.vy_holder = self.vx, self.vy
	
	def die(self):
		self.vx, self.vy = 0,0
		self.vx_holder, self.vy_holder = 0,0
		self.x, self.y = 1000, 1000
		states[0].population[0] -= 1
	
	def freeze(self):
		self.vx, self.vy = 0, 0

class Elsa(pyglet.sprite.Sprite):
	
	def __init__(self):
	
		elsa_image = pyglet.resource.image("bonus.png")
		elsa_image.width, elsa_image.height = 30,30
		elsa_image.anchor_x, elsa_image.anchor_y = 15, 15
		
		pyglet.sprite.Sprite.__init__(self, elsa_image)
		self.reset()
	
	def reset(self):
		
		self.x, self.y = random.randint(1,6) * 75, random.randint(1,6) * 75
		
		while (house.x <= self.x <= house.x + 110) and (house.y <= self.y <= house.y + 110):
			self.x, self.y = random.randint(1,6) * 75, random.randint(1,6) * 75
	

# CLASSES FOR GAME STATES
class PausedState():
		
	def update(self,dt):
		
		for human in states[0].humans:
			human.freeze()
		
		if keys[pyglet.window.key.SPACE]:
		
			condition_label_1.text = ""
			condition_label_2.text = ""
			condition_label_3.text = ""
			
			for human in states[0].humans:
				human.vx, human.vy = human.vx_holder, human.vy_holder

			pyglet.clock.schedule_interval(states[0].human_creator, 2.25)
			pyglet.clock.schedule_interval(states[0].bonus_creator, 15)
			states.pop()

class GameState():
	
	def __init__(self):
		
		self.snake = Snake()
		self.house = House()
		self.choice_of_speed = None
		
		global house
		house = self.house
		
		self.counter = 0
		
		self.elsa = Elsa()
		
		self.reset()

	def reset(self):
		
		self.snake.reset()
		self.house.reset()
		
		self.bonuses = []
		self.consumed_bonuses = []
		
		self.humans = [Human(0)]
		self.dead_humans = []
		
		self.population = [2]
		count = self.population[0]
		
		pointcounter.text = "0"

		pyglet.clock.schedule(self.handle_collision)
		
		
	def update(self, dt):
	
		self.vx = self.snake.vx
		self.vy = self.snake.vy	
		self.snake.x += self.vx * dt
		self.snake.y += self.vy * dt
		
		if keys[pyglet.window.key.P]:
			pyglet.clock.unschedule(self.human_creator)
			pyglet.clock.unschedule(self.bonus_creator)
			condition_label_1.text = "GAME PAUSED"
			condition_label_2.text = "PRESS SPACEBAR TO CONTINUE"
			condition_label_3.text = ""
			states.append(PausedState())
			
		if self.snake.vy == 0:
			if keys[pyglet.window.key.UP]:
				self.snake.vy = abs(self.snake.vx)
				self.snake.vx = 0
				self.snake.rotation = 0

			elif keys[pyglet.window.key.DOWN]:
				self.snake.vy = -abs(self.snake.vx)
				self.snake.vx = 0
				self.snake.rotation = 180

		elif self.snake.vx == 0:
			if keys[pyglet.window.key.LEFT]:
				self.snake.vx = -abs(self.snake.vy)
				self.snake.vy = 0
				self.snake.rotation = -90

			elif keys[pyglet.window.key.RIGHT]:
				self.snake.vx = abs(self.snake.vy)
				self.snake.vy = 0
				self.snake.rotation = 90

		if self.snake.x >= 600-10 or self.snake.x <= 10 or self.snake.y >= 600-10 or self.snake.y <= 10:
			condition_label_1.text = "GAME OVER"
			condition_label_2.text = "YOU HIT A WALL STUPID"
			condition_label_3.text = "SCORE: " + "%01d" % self.snake.points 
			
			pyglet.clock.unschedule(self.human_creator)
			pyglet.clock.unschedule(self.bonus_creator)
			pyglet.clock.unschedule(self.handle_collision)
			pyglet.clock.unschedule(self.update)
			
			self.reset()
			states.append(PausedState())

	def handle_collision(self,dt):
	
		if (self.house.x <= self.snake.x + 10) and (self.snake.x - 10 <= self.house.x + 100) and (self.house.y <= self.snake.y + 10) and (self.snake.y - 10 <= self.house.y + 100):
			
			condition_label_1.text = "GAME OVER"
			condition_label_2.text = "YOU HIT A HOUSE"
			condition_label_3.text = "SCORE: " + "%01d" % self.snake.points 
			
			pyglet.clock.unschedule(self.human_creator)
			pyglet.clock.unschedule(self.bonus_creator)
			pyglet.clock.unschedule(self.update)
			pyglet.clock.unschedule(self.handle_collision)
				
			self.reset()
			states.append(PausedState())
		
		for human in self.humans:
		
			dead = False
			
			human.x += human.vx * dt
			human.y += human.vy * dt
			
			if human.x <= 20:
				human.vx *= -1
			if human.x >= 580:
				human.vx *= -1
			if human.y <= 20:
				human.vy *= -1
			if human.y >= 580:
				human.vy *= -1

			if (self.house.x <= human.x + 12) and (human.x - 12 <= self.house.x + 100) and (self.house.y <= human.y + 12) and (human.y - 12 <= self.house.y + 100):
				if human.x + 12 >= self.house.x and not (human.x - 12 >= self.house.x + 100):
					human.vx *= -1
				elif human.x - 12 >= self.house.x + 100:
					human.vx *= -1
					
				if human.y + 12 >= self.house.y and not (human.y - 12 >= self.house.y + 100):
					human.vy *= -1
				elif human.y - 12 >= self.house.y + 100:
					human.vx *= -1
					
			if (human.x - 12 <= self.snake.x + 10) and (self.snake.x - 10 <= human.x + 12) and (human.y - 12 <= self.snake.y + 10) and (self.snake.y - 10 <= human.y + 12):
					human.die()
					dead = True
					self.snake.points += 1
					pointcounter.text = "%01d" % self.snake.points 
				
			if dead == True:
				self.dead_humans.append(self.humans.index(human))
		
		for bonus in self.bonuses:
		
			if (bonus.x - 15 <= self.snake.x + 10) and (self.snake.x - 10 <= bonus.x + 15) and (bonus.y - 15 <= self.snake.y + 10) and (self.snake.y - 10 <= bonus.y + 12):
				self.consumed_bonuses.append(self.bonuses.index(bonus))
				
				for human in self.humans:
					human.freeze()
				
				pyglet.clock.schedule_interval(self.let_it_go, 10)
				pyglet.clock.unschedule(self.bonus_creator)
				pyglet.clock.unschedule(self.human_creator)
	
	def let_it_go(self,dt):
		
		self.counter = self.counter + 1
		
		if self.counter == 1:
			pass # PUT LET IT GO MUSIC HERE, THE 10 SECOND ONE
			
		else:
			self.counter = 0
			pyglet.clock.schedule_interval(self.human_creator, 1.5)
			pyglet.clock.schedule_interval(self.bonus_creator, 3)
			pyglet.clock.unschedule(self.let_it_go)
		
	def human_creator(self,dt):

		count = self.population[0]
		
		if count > 10:
		
			pyglet.clock.unschedule(self.human_creator)
			pyglet.clock.unschedule(self.bonus_creator)
			pyglet.clock.unschedule(self.update)
			pyglet.clock.unschedule(self.handle_collision)
			
			condition_label_1.text = "GAME OVER"
			condition_label_2.text = "CIVILIZATION TOOK PLACE"
			condition_label_3.text = "SCORE: " + "%01d" % self.snake.points 
			
			self.reset()
			states.append(PausedState())
		
		else:
			if len(self.humans) <= 4:
				self.choice_of_speed = 0
			elif len(self.humans) <= 6:
				self.choice_of_speed = 50
			elif len(self.humans) <= 10:
				self.choice_of_speed = random.choice([0,50,100])
			elif len(self.humans) <= 13:
				self.choice_of_speed = 150
			elif len(self.humans) <= 16:
				self.choice_of_speed = random.choice([50,100,150])
			else:
				self.choice_of_speed = random.choice([0,50,50,150,150,150,300,300])
				
			self.humans.append(Human(self.choice_of_speed))
			self.population[0] += 1
		
	def bonus_creator(self,dt):
		
		self.bonuses = [Elsa()]
		self.bonuses[0].reset()
		self.consumed_bonuses = []
		

@window.event
def on_draw():

	window.clear()
	
	bg.blit(0,0)
	states[0].snake.draw()
	states[0].house.draw()
	
	for i in range(len(states[0].humans)):
		if i not in states[0].dead_humans:
			states[0].humans[i].draw()
	
	for i in range(len(states[0].bonuses)):
		if i not in states[0].consumed_bonuses:
			states[0].bonuses[i].draw()
		
	labels.draw()


def gen_update(dt):

	if len(states):
		states[-1].update(dt)

	else:
		pyglet.app.exit()

pyglet.clock.schedule(gen_update)

states.append(GameState())
states.append(PausedState())

window.clear()
window.flip()

window.set_visible(True)


pyglet.app.run()