import sys
import pygame
from background import Background
from settings import Settings
from ships import xWing
from bullet import Bullet
from enemy import Enemy
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Reakcja na naciśnięcie klawisza"""
	if event.key == pygame.K_RIGHT:
		#Przesunięcie statku w prawą strone
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		#Przesunięcie statku w prawą strone
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		#Utworzenie nowego pocisku i dodanie go do grupy pocisków
		fire_bullet('left', ai_settings, screen, ship, bullets)
		fire_bullet('right', ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
	"""Reakcja na zwolnienie klawisza"""
	if event.key == pygame.K_RIGHT:
		#Przesunięcie statku w prawą strone
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		#Przesunięcie statku w prawą strone
		ship.moving_left = False
			
def check_events(ai_settings, screen, stats, sb, play_button, ship, enemies, bullets):
	"""Reakcja na zdarzenia generowane przez klawiature i mysz"""
	for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, ai_settings, screen, ship, bullets)
			elif event.type == pygame.KEYUP:
				check_keyup_events(event, ship)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, ship, enemies, bullets, play_button):
	"""Uaktualnienie obrazów na ekranie i przejście do nowej pętli"""
	screen.fill(ai_settings.bg_color)
	screen.blit(ai_settings.bg.image, ai_settings.bg.rect)
	
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	enemies.draw(screen)
	sb.show_score()
	
	if not stats.game_active:
		play_button.draw_button()
	
	#Wyświetlenie ostatnio zmodyfikowanego ekranu.
		
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, enemies, bullets):
	"""Uaktualnienie pocisków oraz usuwanie tych które wyszły za ekran"""
	bullets.update()
		
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_enemy_collision(ai_settings, screen, stats, sb, ship, enemies, bullets)

def check_bullet_enemy_collision(ai_settings, screen, stats, sb, ship, enemies, bullets):
	collision = pygame.sprite.groupcollide(bullets, enemies, True, True)
	
	if collision:
		for enemies in collision.values():
			stats.score += ai_settings.enemy_points * len(enemies)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(enemies) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, enemies)

def fire_bullet(side, ai_settings, screen, ship, bullets):
	"""Utworzenie nowego pocisku jeśni nie przekroczono limitu pocisków"""
	if (len(bullets) < ai_settings.bullets_allowed):	
			new_bullet = Bullet(side, ai_settings, screen, ship)
			bullets.add(new_bullet)

def get_number_enemies_x(ai_settings, enemy_width):
	available_space_x = ai_settings.screen_width - 2 * enemy_width
	number_enemies_x = int(available_space_x / (2 * enemy_width))
	return number_enemies_x

def create_enemy(ai_settings, screen, enemies, enemy_number, row_number):
	enemy = Enemy(ai_settings, screen)
	enemy_width = enemy.rect.width
	enemy.x = enemy_width + 2 * enemy_width * enemy_number
	enemy.rect.x = enemy.x
	enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number + 35
	enemies.add(enemy)

def create_fleet(ai_settings, screen, ship, enemies):
	"""Tworzenie floty wrogów"""
	enemy = Enemy(ai_settings, screen)
	number_enemies_x = get_number_enemies_x(ai_settings, enemy.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, enemy.rect.height)
	
	#Rząd wrogów
	for row_number in range(number_rows):
		for enemy_number in range(number_enemies_x):
			create_enemy(ai_settings, screen, enemies, enemy_number, row_number)
		
def get_number_rows(ai_settings, ship_height, enemy_height):
	available_space_y = (ai_settings.screen_height - (3 * enemy_height) - ship_height)
	number_rows = int(available_space_y / (2 * enemy_height)) - 1
	return number_rows
		
def check_fleet_edges(ai_settings, enemies):
	for enemy in enemies.sprites():
		if enemy.check_edges():
			change_fleet_direction(ai_settings, enemies)
			break

def change_fleet_direction(ai_settings, enemies):
	for enemy in enemies.sprites():
		enemy.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def update_enemies(ai_settings, stats ,screen, sb, ship, enemies, bullets):
	"""Uaktualnienie położenia floty"""
	check_fleet_edges(ai_settings, enemies)
	enemies.update()
	
	if pygame.sprite.spritecollideany(ship, enemies):
		ship_hit(ai_settings, stats, screen, sb, ship, enemies, bullets)
		print("Statek został trafiony!!!")
	
	check_enemies_bottom(ai_settings, stats, screen, sb, ship, enemies, bullets)
		
def ship_hit(ai_settings, stats, screen, sb, ship, enemies, bullets):
	if stats.ships_left	 > 0:
		stats.ships_left -= 1
		
		sb.prep_ships()
		enemies.empty()
		bullets.empty()
		
		create_fleet(ai_settings, screen, ship, enemies)
		ship.center_ship()
			
		sleep(1)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_enemies_bottom(ai_settings, stats, screen, sb, ship, enemies, bullets):
	screen_rect = screen.get_rect()
	for enemy in enemies.sprites():
		if enemy.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, sb, ship, enemies, bullets)
			break

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, enemies, bullets, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		enemies.empty()
		bullets.empty()
		
		create_fleet(ai_settings, screen, ship, enemies)
		ship.center_ship()

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	
