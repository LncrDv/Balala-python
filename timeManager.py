import pygame

clock = pygame.time.Clock()
deltaTime = clock.tick(120) / 1000
def CalculateDT():
	global deltaTime
	deltaTime = clock.tick(60) / 1000
