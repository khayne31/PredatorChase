import pygame
import sys
import Deer, Wolf, Rabbit
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        #creates the size
        self.image = pygame.Surface([2, 2])
        #colour
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.center = pos

def returnAnimal():
    seed = randint(1,3)
    if seed == 1:
        return Deer.Deer(randint(0, size[0]), randint(0, size[0]), screen)
    elif seed == 2:
        return Rabbit.Rabbit(randint(0, size[0]), randint(0, size[0]), screen)
    else:
        return Wolf.Wolf(randint(0, size[0]), randint(0, size[0]), screen)



def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 30
    bg = [255, 255, 255]
    size =[1000, 600]


    screen = pygame.display.set_mode(size)

    player = Deer.Deer(40,40, screen)
    #player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    player.vx = 5
    player.vy = 5




    wall_group = pygame.sprite.Group()

    player_group = pygame.sprite.Group()

    wolf_group = pygame.sprite.Group()


    for i in range(15):
        player_group.add(Deer.Deer( randint(0, size[0]), randint(0, size[0]), screen))
    for i in range(30):
        wall_group.add(Rabbit.Rabbit( randint(0, size[0]), randint(0, size[0]), screen))
    for i in range(7):
        wolf_group.add(Wolf.Wolf( randint(0, size[0]), randint(0, size[0]), screen))

    population = [player_group, wall_group,wolf_group]
  
    for wolf in wolf_group:

        wolf.addPopulation(population)

    for rabbit in wall_group:
        rabbit.addPopulation(population)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False


        

        for animal in player_group:
            animal.move()
        for animal in wall_group:
            animal.move()
        for animal in wolf_group:
            animal.move()

        screen.fill(bg)

        # first parameter takes a single sprite
        # second parameter takes sprite groups
        # third parameter is a do kill commad if true
        # all group objects colliding with the first parameter object will be
        # destroyed. The first parameter could be bullets and the second one
        # targets although the bullet is not destroyed but can be done with
        # simple trick bellow

        wolf_eats_deer = [[pygame.sprite.spritecollide(wolf, player_group, False), wolf] for wolf in wolf_group]
        wolf_eats_rabbit = [[pygame.sprite.spritecollide(wolf, wall_group, False), wolf] for wolf in wolf_group]
        deer_eats_rabbit = [[pygame.sprite.spritecollide(deer, wall_group, False), deer] for deer in player_group]

        for collision in wolf_eats_deer:
            for animal in collision[0]:
                population[0].remove(animal)
                animal.kill()

        for collision in deer_eats_rabbit:
            for animal in collision[0]:
                population[1].remove(animal)
                animal.kill()


        for collision in wolf_eats_rabbit:
            for animal in collision[0]:
                population[1].remove(animal)
                animal.kill()

        for wolf in wolf_group:
            if wolf.hp <= 0:
                wolf.kill()

        for deer in player_group:
            if deer.hp <= 0:
                population[0].remove(deer)
                deer.kill()
        
        for wolf in wolf_group:
            wolf.addPopulation(population)
        for rabbit in wall_group:
            rabbit.addPopulation(population)
        for deer in player_group:
            deer.addPopulation(population)

        player_group.draw(screen)
        wall_group.draw(screen)
        wolf_group.draw(screen)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit


if __name__ == '__main__':
    main()



#TODO
"""
-make it so that the rabbits run from the closest predator(look into 
detection range) if no nearby predator just move randomly
-make it so that depending on if the there is a predator or prey closer a deer
will either prioritize running or hunting respectivly(look into detection range)
-make it so that when rabbits come in contact with other rabiits they have a chance 
to reproduce
-look into reproduction of wolves and deer
-look into what the respective traits for each species are
-start prepping for the genetic algorithm, meanign clean up the code running the 
simulation
-look into a trait called confusion which would make an afflicted animal move 
randomly even if there is pre or predator nearby
-toy with a clumsyness modifyier which affects speed
-think about a risk favtor for deer where they are more willing 
to go after prey than run from predators
-think about a stamina trait  where after a certain amount of steps 
the speed of the decreases

"""