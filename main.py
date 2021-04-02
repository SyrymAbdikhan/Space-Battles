
import sys
import random

import entities

import pygame
import pygame.gfxdraw


class Game:
    def __init__(self):
        pygame.init()
        
        self.screen_size = (800, 600)
        self.display_size = (400, 300)
        # making 2 surfaces, screen is where its going to show and siplay is where its going to draw
        self.screen = pygame.display.set_mode(self.screen_size)
        self.display = pygame.Surface(self.display_size)
        # making display transparent so that it is possible to see last farme (optional)
        self.display.set_alpha(100)

        self.clock = pygame.time.Clock()
        self.FPS = 60
        # making background stars
        self.space = self.display.copy()
        self.space.fill((0,5,20))
        for _ in range(40):
            x = random.randint(0, self.display_size[0]-1)
            y = random.randint(0, self.display_size[0]-1)
            # lower light around star 
            pygame.gfxdraw.pixel(self.space, x-1, y, (242, 246, 255, 50))
            pygame.gfxdraw.pixel(self.space, x, y-1, (242, 246, 255, 50))
            pygame.gfxdraw.pixel(self.space, x+1, y, (242, 246, 255, 50))
            pygame.gfxdraw.pixel(self.space, x, y+1, (242, 246, 255, 50))
            # star itself
            pygame.gfxdraw.pixel(self.space, x, y, (242, 246, 255))

        self.bullets = []
        # properties of each spaceship
        controller = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT]
        self.ship = entities.Spaceship(
            pos=(self.display_size[0]//4, self.display_size[1]//2),
            angle=-90,
            s_acc=0.03,
            s_rot_acc=0.06,
            controller=controller,
            folder_name="images/ship1"
        )

        controller2 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT]
        self.ship2 = entities.Spaceship(
            pos=(self.display_size[0]//4*3, self.display_size[1]//2),
            angle=-90,
            s_acc=0.03,
            s_rot_acc=0.06,
            controller=controller2,
            folder_name="images/ship2"
        )

    def run(self):
        while True:
            self.update()
            self.draw()
            # event loop
            for event in pygame.event.get():
                # quits if QUIT x or ESCAPE buttton is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            # resizing and drawing display on screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0,0))
            # updating screen to show frame
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def draw(self):
        # clearing display
        self.display.blit(self.space, (0,0))
        # drawing bullets
        for bullet in self.bullets:
            bullet.draw(self.display)
        # drawing spaceships
        self.ship.draw(self.display)
        self.ship2.draw(self.display)
    
    def update(self):
        # getting pressed keys, updateing spaceships and checking if ship is on the screen
        keys = pygame.key.get_pressed()
        self.ship.update(keys, self.bullets)
        self.check(self.ship.pos, self.display_size)
        self.ship2.update(keys, self.bullets)
        self.check(self.ship2.pos, self.display_size)
        # updating bullets
        for i, bullet in enumerate(self.bullets):
            # checking if bullet should be removed
            if bullet.lifespan <= 0:
                self.bullets.pop(i)
                continue
            bullet.update()
            # also checking if bullet is on the screen
            self.check(bullet.pos, self.display_size)

    def check(self, pos, screen_size):
        # keeping object on the screen by x
        if pos.x < 0:
            pos.x = screen_size[0]
        elif pos.x > screen_size[0]:
            pos.x = 0

        # keeping object on the screen by y
        if pos.y < 0:
            pos.y = screen_size[1]
        elif pos.y > screen_size[1]:
            pos.y = 0


if __name__ == "__main__":
    game = Game()
    game.run()