import sys
import pygame
from background import Background
from settings import Settings
from ships import xWing
import game_functions as gf
from pygame.sprite import Group
from enemy import Enemy
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	
	#Inicjalizacja gry i utworzenie obiektu ekranu.
	
	pygame.init()
	#pygame.mixer.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Star Wars")
	
	#pygame.mixer.music.load('music.wav')
	#pygame.mixer.music.play(-1)
	
	#Dane statystyczne
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	#Utworzenie statku
	
	Tie_Fighter = Enemy(ai_settings, screen)
	X_Wing = xWing(ai_settings, screen)
	bullets = Group()
	enemies = Group()
	
	gf.create_fleet(ai_settings, screen, X_Wing, enemies)
	
	play_button = Button(ai_settings, screen, "Gra")
	
	#Rozpoczęcie pętli głównej gry.
	
	while True:
		
		#Oczekiwanie na wciśnięcie klawisza lub przycisku myszy.
		
		gf.check_events(ai_settings, screen, stats,sb, play_button, X_Wing, enemies, bullets)
		
		if stats.game_active:
			X_Wing.update()
			gf.update_bullets(ai_settings, screen, stats, sb, X_Wing, enemies, bullets)
			gf.update_enemies(ai_settings, stats ,screen, sb, X_Wing, enemies, bullets)
		
		gf.update_screen(ai_settings, screen, stats, sb, X_Wing, enemies, bullets, play_button)		
	
run_game()
	
