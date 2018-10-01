import pygame as pg 
import classes as cs 
import random
import math

class Rabbit(pg.sprite.Sprite):
	def __init__(self, x, y, screen, color = [255, 0, 0]):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.color = color
		self.pos = (x, y)
		self.size = int(20)
		#self.image = pg.Surface([self.size, self.size])
		self.image = pg.image.load("rabbit.png").convert_alpha()
		self.image = pg.transform.scale(self.image,(25,25))
		#self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.directionChangeRate = .05
		self.vx = random.randint(3,7)
		self.vy = self.vx
		self.reproduceCount = 0
		self.predators = []

		self.direction = [1,1]
		self.closestPredator = None
		self.detectionRange = 60

	def addPopulation(self, population):
		self.predators = [deer for deer in population[0]]
		self.predators.extend([wolf for wolf in population[2]])

	def move(self):
		self.run()
		if self.closestPredator == None:
		
			if self.directionChangeRate >= random.random():
				self.vx *= -1
		

			if self.directionChangeRate >= random.random():
				self.vy *= -1

			self.rect.y += self.vy
			self.rect.x += self.vx
		else:
			self.rect.y += self.vy*self.direction[1]
			self.rect.x += self.vx*self.direction[0]

		
		if self.rect.x >= self.screen.get_width():
			self.rect.x = self.size/2+1
		elif self.rect.x  < 0:
			self.rect.x = self.screen.get_width()-self.size/2
	
		if self.rect.y  >= self.screen.get_height():
			self.rect.y = self.size/2+1
		elif self.rect.y < 0:
			self.rect.y = self.screen.get_height()-self.size/2

	def getClosestPredator(self):
		closestDistance = 90000000000000000000000000
		if len(self.predators) == 0:
			self.closestPredator = None
		else:
			closestPredator = None
			for animal in self.predators:
				circle = (self.rect.x - animal.rect.x)**2 + (self.rect.y - animal.rect.y)**2
				if not( circle <= self.detectionRange**2):
					self.predators.remove(animal)
			for animal in self.predators:
				distance = min([math.sqrt((self.rect.x-animal.rect.x)**2 + (self.rect.y-animal.rect.y)**2), 
				math.sqrt((self.rect.x+self.screen.get_width()-animal.rect.x)**2 + (self.rect.y+self.screen.get_height()-animal.rect.y)**2)])
				if  distance < closestDistance:
					closestDistance = distance
					closestPredator = animal

				if distance == 0 :
					self.population.remove(closestPredator)
					self.getClosestPredator()		
			self.closestPredator = closestPredator

		return self.closestPredator


	def run(self):
		print(self.rect.x, self.rect.y)
		if self.getClosestPredator() != None:
			goal = [(self.closestPredator.rect.x*1000 if self.closestPredator.rect.x > self.rect.x else self.closestPredator.rect.x*-1000), 
			(self.closestPredator.rect.y*1000 if self.closestPredator.rect.y > self.rect.y else self.closestPredator.rect.y*-1000)]

		
			directionMatrix = [1,-1]
			direction  = [1,1]
			distanceX = min([abs(self.rect.x + self.vx-goal[0]), abs(self.rect.x+self.screen.get_width() +self.vx-goal[0])])
			distanceY = min([abs(self.rect.y + self.vy-goal[1]), abs(self.rect.y+self.screen.get_height() +self.vy-goal[1])])			
		
			otherDistanceX = min([abs(self.rect.x - self.vx - goal[0]), abs(self.rect.x+self.screen.get_width() -self.vx- goal[0])])
			otherDistanceY = min([abs(self.rect.y - self.vy- goal[1]), abs(self.rect.y+self.screen.get_height() -self.vy- goal[1])])


			#print(self.rect.x, self.rect.y)
			#print[goal]

			if self.rect.x < 10 and abs(otherDistanceX - distanceX) <30:
				direction[0] = -1
			elif otherDistanceX > distanceX:
				direction[0] *= -1
			if self.rect.y < 10 and abs(otherDistanceY - distanceY) <30:
				direction[1] = -1
			
			elif otherDistanceY > distanceY:
				direction[1] *= -1
			

			self.direction = direction

	def reproduce(self):
		self.reproduceCount += 1