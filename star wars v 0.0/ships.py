import pygame
from pygame.sprite import Sprite

class xWing(Sprite):
	
	def __init__(self, ai_settings, screen):
		"""Inicjalizacja X-Winga i jego położenie początkowe"""
		super(xWing, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Wczytywanie obrazu statku.
		self.image = pygame.image.load('X_Wing.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#X-Wing pojawi sie na dole ekranu
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom - 10
		
		#Punkt środkowy statku jest przechowywany w postaci liczby zmiennoprzecinkowej
		self.center = float(self.rect.centerx)
		
		#Opcje wskazujące na poruszanie się statku
		self.moving_right = False
		self.moving_left = False
	
	def blitme(self):
		"""Wyświetlenie X-Winga w jego aktualnym położeniu"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		self.rect.centerx = self.center
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
