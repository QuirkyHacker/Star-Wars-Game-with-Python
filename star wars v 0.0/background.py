import pygame

class Background(pygame.sprite.Sprite):
	"""Klasa przeznaczona do ustawienia tła w grze"""
	def __init__(self, image_file, location):
		"""Inicjalizacja ustawień tła"""
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
