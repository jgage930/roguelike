#! usr/bin/python
import pygame
from models import Player, Enemy

# set window size
size = w, h = (1000, 1000)

# screen and clock
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# colors
white = (255, 255, 255)
black = (0, 0, 0)

# start pygame
pygame.init()

# start mixer
pygame.mixer.init()

# Player
player = Player((500, 500), screen)
player_group = pygame.sprite.Group(player)

# Enemies
enemy1 = Enemy((100, 100))
enemy2 = Enemy((400, 100))
enemy3 = Enemy((800, 800))
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy1)
enemy_group.add(enemy2)
enemy_group.add(enemy3)

# set variables
running = True

while running:
	screen.fill(white)
	# handle events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	player.handle_keys()

	# update sprites
	player_group.update()
	enemy_group.update(player.get_pos())


	# draw sprites
	player_group.draw(screen)
	enemy_group.draw(screen)

	# these stay at bottom of loop
	pygame.display.update()
	clock.tick(30) 