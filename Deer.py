import pygame as pg 
import classes as cs
import random
"""
class Deer():
	def __init__(self, x, y):
		print("deer")
		self.x = x
		self.y = y
		self.speedx = random.randint(1,5)
		self.speedy = self.speedx
		self.directionChangeRate = random.uniform(0,.3)

	def draw(self, screen):
		radius = 13

		if self.x - radius >= screen.get_width():
			self.x = 0
		elif self.x -radius < -radius:
			self.x = screen.get_width()+1

		if self.y - radius >= screen.get_height():
			self.y = 0
		elif self.y - radius < -radius:
			self.y = screen.get_height()

		pg.draw.rect(screen, cs.BLUE, [self.x-radius, self.y-radius, radius*2, radius*2 ])

	def addXDistance(self):
		if self.directionChangeRate >= random.random():
			self.speedx *= -1
		self.x += self.speedx

	def addYDistance(self):
		if self.directionChangeRate >= random.random():
			self.speedy *= -1
		self.y += self.speedy
"""

class Deer(pg.sprite.Sprite):
	def __init__(self, x, y, screen, color = [255, 0, 0]):
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.color = color
		self.pos = (x, y)
		self.size = int(20)
		#self.image = pg.Surface([self.size, self.size])
		self.image = pg.image.load("deer.jpg").convert_alpha()
		self.image = pg.transform.scale(self.image,(25,25))
		#self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.directionChangeRate = .05
		self.vx = random.randint(6,8)
		self.vy = self.vx
		self.hp = random.randint(50,500)
		self.starveRate  =random.randint(0,int(self.hp*.05))
		self.killCount = 0

		self.prey = []

		self.direction = [1,1]
		self.closestPrey = None
		self.detectionRange = self.vx * 3


	def move(self):
		iterator = 1
		if iterator%3 == 0:
			self.hunt()	
		iterator += 1
		
		if self.closestPrey == None:
		
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
			self.rect.x = self.screen.get_width()-1
	
		if self.rect.y  >= self.screen.get_height():
			self.rect.y = self.size/2+1
		elif self.rect.y < 0:
			self.rect.y = self.screen.get_height()
		#self.decay()

	def decay(self):
		self.hp -= self.starveRate

	def addPopulation(self, population):
		self.prey = [rabbit for rabbit in population[1]]
	

	def getClosestPrey(self):
		closestDistance = 90000000000000000000000000
		if len(self.prey) == 0:
			self.closestPrey = None
		else:
			closestPrey = None	
			for animal in self.prey:
				if not((self.rect.x - animal.rect.x)**2 + (self.rect.y - animal.rect.y)**2 <= self.detectionRange**2):
					self.prey.remove(animal)
			for animal in self.prey:
				distance = min([math.sqrt((self.rect.x-animal.rect.x)**2 + (self.rect.y-animal.rect.y)**2), 
				math.sqrt((self.rect.x+self.screen.get_width()-animal.rect.x)**2 + (self.rect.y+self.screen.get_height()-animal.rect.y)**2)])
				if  distance < closestDistance:
					closestDistance = distance
					closestPrey = animal

				if distance == 0 :
					self.population.remove(closestPrey)
					self.getClosestPrey()		
			self.closestPrey = closestPrey

		return self.closestPrey

	def hunt(self):
		#print(self.closestPrey)
		if self.getClosestPrey() != None:
			directionMatrix = [1,-1]
			direction  = [1,1]
			distanceX = min([abs(self.rect.x + self.vx-self.closestPrey.rect.x), abs(self.rect.x+self.screen.get_width() +self.vx-self.closestPrey.rect.x)])
			distanceY = min([abs(self.rect.y + self.vy-self.closestPrey.rect.y), abs(self.rect.y+self.screen.get_height() +self.vy-self.closestPrey.rect.y)])			
		
			otherDistanceX = min([abs(self.rect.x - self.vx -self.closestPrey.rect.x), abs(self.rect.x+self.screen.get_width() -self.vx-self.closestPrey.rect.x)])
			otherDistanceY = min([abs(self.rect.y - self.vy-self.closestPrey.rect.y), abs(self.rect.y+self.screen.get_height() -self.vy-self.closestPrey.rect.y)])


			if otherDistanceX < distanceX:
				direction[0] *= -1
			if otherDistanceY < distanceY:
				direction[1] *= -1

			
				
			self.direction = direction

	