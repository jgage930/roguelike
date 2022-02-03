import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, start: tuple, screen):
		super().__init__()

		# screen to draw shapes for now
		self.screen = screen

		# load images
		self.walkup_images = []
		for i in range(5, 10):
			image = pygame.image.load(f'/home/jgage/Documents/Projects/roguelike/art/player/walk_up/tile00{i}.png')
			self.walkup_images.append(image)

		self.walkdown_images = []
		for i in range(0, 5):
			image = pygame.image.load(f'/home/jgage/Documents/Projects/roguelike/art/player/walk_down/tile00{i}.png')
			self.walkdown_images.append(image)

		self.walkleft_images = []
		for i in range(10, 15):
			image = pygame.image.load(f'/home/jgage/Documents/Projects/roguelike/art/player/walk_left/tile0{i}.png')
			self.walkleft_images.append(image)

		self.walkright_images = []
		for i in range(15, 20):
			image = pygame.image.load(f'/home/jgage/Documents/Projects/roguelike/art/player/walk_right/tile0{i}.png')
			self.walkright_images.append(image)

		# image to display
		self.image = self.walkup_images[0]
		self.image = pygame.transform.scale(self.image, (70, 70))

		# rect
		self.rect = self.image.get_rect()

		# postion
		self.x, self.y = start

		# dimensions
		self.w = 30
		self.h = 50

		# speed
		self.speed = 8

		# direction 
		self.dir = dict.fromkeys(['u', 'd', 'l', 'r'], False)

		self.index = 0

		# sounds
		#self.walk_sound = pygame.mixer.Sound('home/jgage/Documents/Projects/roguelike/sound/walking.wav')

		# attacking variable
		self.attacking = False

	def set_dir(self, dirs:str):
		"""Sets the direction the player is facing"""
		self.dir[dirs] = True

		for key in self.dir:
			if key != dirs:
				self.dir[dirs] = False

	def get_dir(self) -> dict:
		return self.dir

	def handle_keys(self):
		"""Moves player"""
		self.attacking = False
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.dir['u'] = True
			self.dir['r'] = False
			self.dir['l'] = False
			self.dir['d'] = False

			if self.y >= self.speed:
				self.y -= self.speed
		elif keys[pygame.K_s]:
			self.dir['u'] = False
			self.dir['r'] = False
			self.dir['l'] = False
			self.dir['d'] = True

			if self.y <= 1000 - self.h - self.speed:
				self.y += self.speed
		elif keys[pygame.K_a]:
			self.dir['u'] = False
			self.dir['r'] = False
			self.dir['l'] = True
			self.dir['d'] = False

			if self.x >= self.speed:
				self.x -= self.speed
		elif keys[pygame.K_d]:
			self.dir['u'] = False
			self.dir['r'] = True
			self.dir['l'] = False
			self.dir['d'] = False

			if self.x <= 1000 - self.speed:
				self.x += self.speed

		if keys[pygame.K_SPACE]:
			self.attacking = True

		self.rect.center = (self.x, self.y)

	def get_pos(self) -> tuple:
		return (self.x, self.y)

	def attack(self):
		# draws a rectangle in the direction  the player is attacking this will be used to set the hitbox
		color = (255, 0, 0)

		if self.dir['d']:
			w = 70
			h = 20

			x = self.x - 35 # width / 2
			y = self.y + 35 + h
			pygame.draw.rect(self.screen, color, (x, y, w, h))

		if self.dir['r']:
			w = 20
			h = 70

			x = self.x + 35
			y = self.y - 35
			pygame.draw.rect(self.screen, color, (x, y, w, h))

		if self.dir['l']:
			w = 20
			h = 70

			x = self.x - 70
			y = self.y - 35
			pygame.draw.rect(self.screen, color, (x, y, w, h))

		if self.dir['u']:
			w = 70
			h = 20

			x = self.x - 35
			y = self.y - 35 - h
			pygame.draw.rect(self.screen, color, (x, y, w, h))

	def update(self):
		# get direction
		dir = self.get_dir()

		if dir['u']:
			self.index += 1
			if self.index >= len(self.walkup_images):
				self.index = 0

			self.image = self.walkup_images[self.index]

		if dir['l']:
			self.index += 1

			if self.index >= len(self.walkleft_images):
				self.index = 0

			self.image = self.walkleft_images[self.index]

		if dir['r']:
			self.index += 1
			if self.index >= len(self.walkright_images):
				self.index = 0

			self.image = self.walkright_images[self.index]

		if dir['d']:
			self.index += 1
			if self.index >= len(self.walkdown_images):
				self.index = 0

			self.image = self.walkdown_images[self.index]

		self.image = pygame.transform.scale(self.image, (70, 70))
		
		# check if attacking
		if self.attacking:
			self.attack()

		print(self.attacking)

class Enemy(pygame.sprite.Sprite):

	def __init__(self, start: tuple):
		super().__init__()

		self.image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/enemies/spider.png')

		self.rect = self.image.get_rect()

		self.x, self.y = start

		self.rect.center = start

		self.speed = 2

	def update(self, target:tuple):
		"""Moves the enemy towards the target"""
		tar_x, tar_y = target

		y_diff = self.y - tar_y
		x_diff = self.x - tar_x

		if x_diff > 0:
			self.x += self.speed * -1
		else:
			self.x += self.speed

		if y_diff < 0:
			self.y -= self.speed * -1
		else:
			self.y -= self.speed

		self.rect.center = (self.x, self.y)

