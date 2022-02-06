from pickle import FALSE
import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, start: tuple, screen):
		super().__init__()

		# screen to draw shapes for now
		self.screen = screen

		# load walking images
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

		# load attack images
		self.attack_up_image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/player/attack/attack_up.png')
		self.attack_down_image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/player/attack/attack_down.png')
		self.attack_right_image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/player/attack/attack_right.png')
		self.attack_left_image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/player/attack/attack_left.png')

		# image to display
		self.image = self.walkup_images[0]
		self.image = pygame.transform.scale(self.image, (70, 70))

		# hurt box
		self.rect = self.image.get_rect()

		# postion
		self.x, self.y = start

		# dimensions
		self.w = 30
		self.h = 50

		# speed
		self.speed = 10

		# direction 
		self.dir = dict.fromkeys(['u', 'd', 'l', 'r'], False)

		self.index = 0

		# sounds
		#self.walk_sound = pygame.mixer.Sound('home/jgage/Documents/Projects/roguelike/sound/walking.wav')

		# attacking variable
		self.attacking = False

		# check if holding space
		self.hold_space = False

		# hit box 
		self.hit_box = None

		# health
		self.health = 100

		# track wealth
		self.wealth = 0
		self.coin_image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/coin/coin.png')


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

		if keys[pygame.K_SPACE] and not self.hold_space:
			self.attacking = True
			self.hold_space = True
		else:
			self.hold_space = False

		self.rect.center = (self.x, self.y)

	def get_pos(self) -> tuple:
		return (self.x, self.y)

	def attack(self):
		# draws a rectangle in the direction  the player is attacking this will be used to set the hitbox
		# and sets the hitbox accordingly
		color = (255, 0, 0)

		if self.dir['d']:
			w = 70
			h = 40

			x = self.x - 35 # width / 2
			y = self.y + 35 + h
			
			self.image = self.attack_down_image

			self.hit_box = pygame.Rect(x, y, w, h)

		if self.dir['r']:
			w = 40
			h = 70

			x = self.x + 35
			y = self.y - 35

			self.image = self.attack_right_image

			self.hit_box = pygame.Rect(x, y, w, h)

		if self.dir['l']:
			w = 40
			h = 70

			x = self.x - 70
			y = self.y - 35

			self.image = self.attack_left_image

			self.hit_box = pygame.Rect(x, y, w, h)

		if self.dir['u']:
			w = 70
			h = 40

			x = self.x - 35
			y = self.y - 35 - h

			self.image = self.attack_up_image

			self.hit_box = pygame.Rect(x, y, w, h)

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
		
		# check if attacking
		if self.attacking:
			self.attack()
		else:
			# reset hit box when player is not attacking
			self.hit_box = None

		self.image = pygame.transform.scale(self.image, (70, 70))

		self.draw_hud()

	def get_hitbox(self):
		return self.hit_box

	def damage(self, amount:int):
		self.health -= amount

	def get_health(self):
		return self.health

	def add_wealth(self):
		self.wealth += 1

	def draw_hud(self):
		# draw health bar
		pygame.draw.rect(self.screen, (255, 0, 0), (20, 900, self.health * 5, 30))

		# coins
		self.screen.blit(self.coin_image, (10, 940))
		myfont = pygame.font.SysFont("Comic Sans MS", 30)
		text = myfont.render(f"x {self.wealth}", FALSE, (0, 0, 0))
		self.screen.blit(text, (30, 940))


class Enemy(pygame.sprite.Sprite):

	def __init__(self, start: tuple, screen):
		super().__init__()

		self.x, self.y = start

		self.screen = screen

		self.image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/enemies/spider.png')

		self.rect = self.image.get_rect()

		self.x, self.y = start

		self.rect.center = start

		self.speed = 2

		# health and health bar
		self.health = 10

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

		pygame.draw.rect(self.screen, (255, 0, 0), (self.x - 15, self.y - 20, self.health * 5, 8))

	def damage(self, amount:int):
		self.health -= amount

	def get_health(self):
		return self.health

class Coin(pygame.sprite.Sprite):

	def __init__(self, start:tuple) -> None:
		super().__init__()
		
		self.x, self.y = start

		self.image = pygame.image.load('/home/jgage/Documents/Projects/roguelike/art/coin/coin.png')

		self.rect = self.image.get_rect()

		self.rect.center = self.x, self.y

		self.value = 1

	def update(self) -> None:
		pass