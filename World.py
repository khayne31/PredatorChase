import Deer, Rabbit, Wolf
from random import randint


def populate(screen):
	for animal in pop:
		animal.addXDistance()
		animal.addYDistance()
		animal.draw(screen)

def returnAnimal():
	seed = randint(2,3)
		#return Deer.Deer(randint(0, 500), randint(0, 500))
	if seed == 2:
		return Rabbit.Rabbit(randint(0,500), randint(0,500))
	else:
		return Wolf.Wolf(randint(0,500), randint(0,500))



pop = [returnAnimal() for i in range(10)]