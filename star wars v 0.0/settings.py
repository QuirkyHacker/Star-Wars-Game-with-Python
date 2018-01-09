from background import Background

class Settings():
	"""Klasa przeznaczona do przetrzymywania wszystkich ustawień gry."""
	def __init__(self):
		"""Inicjalizacja ustawień gry"""
		#Ustawienia ekranu.
		self.screen_width = 1024
		self.screen_height = 600
		self.bg_color = (10, 12, 16)
		self.bg = Background('bg_space.bmp', [0,0])
		#Ustawienia dotyczące statku
		self.ship_limit = 3
		#Ustawienia pocisku X-Winga
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 255, 69, 0
		self.bullets_allowed = 6 
		self.tmp_bullet = 0
		#Ustawienia wrogów
		self.fleet_drop_speed = 10
		#Gdy fleet_direction wynosi 1 to flota porusza się w prawo. -1 w lewo.
		self.fleet_direction = 1
		#Zmiana szybkości gry
		self.speedup_scale = 1.1
		#Zmiana licznika punktów
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.enemy_speed_factor = 1
		
		#Gdy fleet_direction wynosi 1 to flota porusza się w prawo. -1 w lewo.
		self.fleet_direction = 1
		
		#Punktacja
		self.enemy_points = 50
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.enemy_speed_factor *= self.speedup_scale
		
		self.enemy_points = int(self.enemy_points * self.score_scale)
		print(self.enemy_points)
		
		
		
		
