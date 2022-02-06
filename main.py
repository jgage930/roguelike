#! usr/bin/python3.8
from tkinter import W
import pygame
from models import Player, Enemy, Coin
import random

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

def gen_wave(num:int):
	# generates a group of enemy sprites.
	my_group = pygame.sprite.Group()

	for i in range(0, num):
		x = random.randint(0, w)
		y = random.randint(0, h)

		my_group.add(Enemy((x, y), screen))

	return my_group

def gen_coins(num:int):
	my_group = pygame.sprite.Group()

	for i in range(0, num):
		x = random.randint(0, w)
		y = random.randint(0, h)

		my_group.add(Coin((x, y)))

	return my_group


# Player
player = Player((500, 500), screen)
player_group = pygame.sprite.Group(player)

# Enemies
enemy_group = gen_wave(3)

# Coins
coin_group = gen_coins(1)

# set variables
running = True

difficulty = 3

while running:
	screen.fill(white)

	# check if the enemy group is empty and generate a new wave if it is
	if not enemy_group:
		difficulty += 1
		enemy_group = gen_wave(difficulty)

		coin_group.empty()
		coin_group = gen_coins(difficulty // 2)

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
	coin_group.draw(screen)

	# check for collision
	# this returns a dict
	if pygame.sprite.groupcollide(enemy_group, player_group, False, False):
		player.damage(1)

	# TODO make check if the attack rect is htting the enemey rect and damage enemies
	for enemy in enemy_group:
		player_hitbox = player.get_hitbox()
		if player_hitbox is not None:
			if pygame.Rect.colliderect(enemy.rect, player_hitbox):
				enemy.damage(1)

		# check if the enemy is dead
		if enemy.get_health() <= 0:
			enemy_group.remove(enemy)

	# coin and player collision
	if pygame.sprite.groupcollide(coin_group, player_group, True, False):
		player.add_wealth()

	
	

	# these stay at bottom of loop
	pygame.display.update()
	clock.tick(20) 