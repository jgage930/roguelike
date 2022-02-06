#! usr/bin/python3.8
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
enemy1 = Enemy((100, 100), screen)
enemy2 = Enemy((400, 100), screen)
enemy3 = Enemy((800, 800), screen)
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

	# check for collision
	# this returns a dict
	if pygame.sprite.groupcollide(enemy_group, player_group, False, False):
		player.damage(1)

	# TODO make check if the attack rect is htting the enemey rect and damage enemies
	for enemy in enemy_group:
		player_hitbox = player.get_hitbox()
		if player_hitbox is not None:
			if pygame.Rect.colliderect(enemy.rect, player_hitbox):
				print("hit")
				enemy.damage(1)

		# check if the enemy is dead
		if enemy.get_health() <= 0:
			enemy_group.remove(enemy)

	
	

	# these stay at bottom of loop
	pygame.display.update()
	clock.tick(20) 