import pyglet, random, math
from pyglet.gl import *

# the game window
window = pyglet.window.Window(800,600,visible=False)

# labels at the end of the game
condition_label_1 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 30, x = 300, y = 350, anchor_x = "center", anchor_y = "center")
condition_label_2 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 26, x = 300, y = 300, anchor_x = "center", anchor_y = "center")
condition_label_3 = pyglet.text.Label(text = "", font_name = "Arial", font_size = 24, x = 300, y = 250, anchor_x = "center", anchor_y = "center")

# batches of sprites and lines
batch1 = pyglet.graphics.Batch() # this is for the lines
batch = pyglet.graphics.Batch()	 # this is for the sprites

# the line that divides the screen
batch1.add(2, GL_LINES, None, ('v2i', (600,0, 600,600)))

# the background texture
bg = pyglet.resource.image("grass.jpg")
bg.width, bg.height = 600, 600

# label for buns
pts = pyglet.text.Label('BUNS', font_name='Arial', font_size=15, x=700, y=575, anchor_x='center', anchor_y='center', batch=batch1)
pointcounter = pyglet.text.Label('0', font_name='Arial', font_size=24, x=700, y=540, anchor_x='center', anchor_y='center', batch=batch1)

# a function for anchoring images at the center
def center_img(img):
	img.anchor_x = img.width//2
	img.anchor_y = img.height//2

# class for the Anaconda
class Snake(pyglet.sprite.Sprite):
	def __init__(self):
		self.points = 0
		image = pyglet.resource.image('ball.png')
		image.width, image.height = 20, 40
		image.anchor_x = 10
		image.anchor_y = 30
		
		pyglet.sprite.Sprite.__init__(self, image, batch=batch)
		
		self.reset()
	
	def reset(self):
		self.x, self.y = 300,300
		self.rotation = 90
		direction = 0

		self.vx, self.vy = math.cos(direction)*100, math.sin(direction)*100

# class for a house
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
		pyglet.sprite.Sprite.__init__(self, house_image, batch=batch)
		
		self.x = random.choice([100,200,400,500])
		self.y = random.choice([100,200,400,500])
		
# class for the Humans
class Human(pyglet.sprite.Sprite):
	def __init__(self,speed):
		self.speed = speed
		#human_image = pyglet.image.SolidColorImagePattern((230,181,108,255))
		#human_image = pyglet.image.create(24, 24, human_image)
		
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
		pyglet.sprite.Sprite.__init__(self, human_image, batch=batch)
		
		self.reset();
	
	def reset(self):
		self.x, self.y = random.randint(1,11) * 50, random.randint(1,11) * 50
		
		while (house.x <= self.x <= house.x + 110) and (house.y <= self.y <= house.y + 110):
			self.x, self.y = random.randint(1,11) * 50, random.randint(1,11) * 50
		
		self.direction = random.random()*math.pi/2 + random.choice([-math.pi/4, 3*math.pi/4])
		self.vx, self.vy = math.cos(self.direction)*self.speed, math.sin(self.direction)*self.speed
	
	def die(self):
		self.speed = 0
		self.x, self.y = 1000, 1000
		population[0] -= 1

# a function for handling collision between the snake and humans or snake and houses
def handle_collision(dt):
	for human in humans:
	
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

		if (house.x <= human.x + 12) and (human.x - 12 <= house.x + 100) and (house.y <= human.y + 12) and (human.y - 12 <= house.y + 100):
			if human.x + 12 >= house.x - 0 and not (human.x + 12 >= house.x + 100):
				human.vx *= -1
			elif human.x + 12 >= house.x + 100:
				human.vx *= -1
				
			if human.y + 12 >= house.y - 0 and not (human.y + 12 >= house.y + 100):
				human.vy *= -1
			elif human.y + 12 >= house.y + 100:
				human.vx *= -1
				
		if (house.x <= snake.x + 10) and (snake.x - 10 <= house.x + 100) and (house.y <= snake.y + 10) and (snake.y - 10 <= house.y + 100):
			if snake.x + 10 >= house.x - 0 and not (snake.x + 12 >= house.x + 100):
				condition_label_1.text = "GAME OVER"
				condition_label_2.text = "YOU HIT A HOUSE"
				condition_label_3.text = "SCORE: " + "%01d" % snake.points 
				pyglet.clock.unschedule(handle_collision)
				pyglet.clock.unschedule(human_creator)
				pyglet.clock.unschedule(handle_snake)
			elif snake.x + 12 >= house.x + 100:
				condition_label_1.text = "GAME OVER"
				condition_label_2.text = "YOU HIT A HOUSE"
				condition_label_3.text = "SCORE: " + "%01d" % snake.points 
				pyglet.clock.unschedule(handle_collision)
				pyglet.clock.unschedule(human_creator)
				pyglet.clock.unschedule(handle_snake)

			if snake.y + 10 >= house.y - 0 and not (snake.y + 12 >= house.y + 100):
				condition_label_1.text = "GAME OVER"
				condition_label_2.text = "YOU HIT A HOUSE"
				condition_label_3.text = "SCORE: " + "%01d" % snake.points 
				pyglet.clock.unschedule(handle_collision)
				pyglet.clock.unschedule(human_creator)
				pyglet.clock.unschedule(handle_snake)
			elif snake.y + 12 >= house.y + 100:
				condition_label_1.text = "GAME OVER"
				condition_label_2.text = "YOU HIT A HOUSE"
				condition_label_3.text = "SCORE: " + "%01d" % snake.points 
				pyglet.clock.unschedule(handle_collision)
				pyglet.clock.unschedule(human_creator)
				pyglet.clock.unschedule(handle_snake)

		if (human.x - 12 <= snake.x + 10) and (snake.x - 10 <= human.x + 12) and (human.y - 12 <= snake.y + 10) and (snake.y - 10 <= human.y + 12):
			if snake.x + 10 >= human.x - 12 and not (snake.x + 10 >= human.x - 12):
				human.die()
				dead = True
				snake.points += 1
				pointcounter.text = "%01d" % snake.points 
			elif snake.x + 10 >= human.x - 12:
				human.die()
				dead = True
				snake.points += 1
				pointcounter.text = "%01d" % snake.points 

			if snake.y + 10 >= human.y - 12 and not (snake.y + 10 >= human.y - 12):
				human.die()
				dead = True
				snake.points += 1
				pointcounter.text = "%01d" % snake.points 
			elif snake.y + 10 >= human.y - 12:
				human.die()
				dead = True
				snake.points += 1
				pointcounter.text = "%01d" % snake.points
		
		if dead == True:
			dead_humans.append(humans.index(human))

# a function that creates humans on the screen every 2.5 secs
def human_creator(dt):

	count = population[0]
	
	if count > 10:
		condition_label_1.text = "GAME OVER"
		condition_label_2.text = "CIVILIZATION TOOK PLACE"
		condition_label_3.text = "SCORE: " + "%01d" % snake.points 
		pyglet.clock.unschedule(handle_collision)
		pyglet.clock.unschedule(human_creator)
		pyglet.clock.unschedule(handle_snake)

	if len(humans) <= 4:
		choice_of_speed = 0
	elif len(humans) <= 6:
		choice_of_speed = 50
	elif len(humans) <= 10:
		choice_of_speed = random.choice([0,50,100])
	elif len(humans) <= 13:
		choice_of_speed = 150
	elif len(humans) <= 16:
		choice_of_speed = random.choice([50,100,150])
	else:
		choice_of_speed = random.choice([0,50,50,150,150,150,300,300])
		
	humans.append(Human(choice_of_speed))
	population[0] += 1

@window.event
def on_draw():
	window.clear()
	
	bg.blit(0,0)
	
	house.draw()
	
	
	for i in xrange(0,len(humans)):
		if i not in dead_humans:
			humans[i].draw()
		
	condition_label_1.draw()
	condition_label_2.draw()
	condition_label_3.draw()
	snake.draw()
	batch1.draw()
		
def handle_snake(dt):
	
	vx = snake.vx
	vy = snake.vy	
	snake.x += vx * dt
	snake.y += vy * dt
	
	if snake.vy == 0:
		if keys[pyglet.window.key.UP]:
			snake.vy = abs(snake.vx)
			snake.vx = 0
			snake.rotation = 0

		elif keys[pyglet.window.key.DOWN]:
			snake.vy = -abs(snake.vx)
			snake.vx = 0
			snake.rotation = 180

	elif snake.vx == 0:
		if keys[pyglet.window.key.LEFT]:
			snake.vx = -abs(snake.vy)
			snake.vy = 0
			snake.rotation = -90

		elif keys[pyglet.window.key.RIGHT]:
			snake.vx = abs(snake.vy)
			snake.vy = 0
			snake.rotation = 90

	if snake.x >= 600-10 or snake.x <= 10 or snake.y >= 600-10 or snake.y <= 10:
		condition_label_1.text = "GAME OVER"
		condition_label_2.text = "YOU HIT A WALL STUPID"
		condition_label_3.text = "SCORE: " + "%01d" % snake.points 
		pyglet.clock.unschedule(handle_collision)
		pyglet.clock.unschedule(human_creator)
		pyglet.clock.unschedule(handle_snake)

house = House()
speed_choices = [0,50,150,300]
population = [2]
humans = [Human(0)]
dead_humans = []
window.set_visible(True)
pyglet.clock.schedule(handle_collision)
pyglet.clock.schedule_interval(human_creator, 2.25)
snake = Snake();
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
pyglet.clock.schedule(handle_snake)


pyglet.app.run()