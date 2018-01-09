import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
	"""Klasa przedstawiająca pojedyńczego wroga"""
	def __init__(self, ai_settings, screen):
		"""Położenie początkowe oraz inicjalizacja"""
		super(Enemy, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Wczytanie wroga oraz definicja atrybutu rect.
		self.image = pygame.image.load('tie_fighter.png')
		self.rect = self.image.get_rect()
		
		#Umieszczenie nowego wroga w lewym górnym rogu
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#Przechowywanie dokładnego położenia wroga
		self.x = float(self.rect.x)
	
	def bltime(self):
		"""Wyświetlenie wroga w jego aktualnym położeniu"""
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		"""Przesuniecie wroga"""
		self.x += (self.ai_settings.enemy_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""Jeśli krawędz ekranu to zwróć True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
