
import sys
import random

import entities

import pygame
import pygame.gfxdraw


def main():
    pygame.init()
    
    screen_size = (800, 600)
    display_size = (400, 300)
    # making 2 surfaces, screen is where its going to show and siplay is where its going to draw
    screen = pygame.display.set_mode(screen_size)
    display = pygame.Surface(display_size)

    clock = pygame.time.Clock()
    FPS = 60
    # making background stars
    space = display.copy()
    space.fill((0,5,20))
    for _ in range(40):
        pygame.gfxdraw.pixel(space, random.randint(0, display_size[0]-1), random.randint(0, display_size[1]-1), (242, 246, 255))

    bullets = []
    # properties of each spaceship
    controller = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT]
    ship = entities.Spaceship((display_size[0]//4, display_size[1]//2), 0.03, 0.06, controller, "images/ship1")

    controller2 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT]
    ship2 = entities.Spaceship((display_size[0]//4*3, display_size[1]//2), 0.03, 0.06, controller2, "images/ship2")

    while True:

        # getting pressed keys, updateing spaceships and checking if ship is on the screen
        keys = pygame.key.get_pressed()
        ship.update(keys, bullets)
        check(ship.object.pos, display_size)
        ship2.update(keys, bullets)
        check(ship2.object.pos, display_size)
        # updating bullets
        for i, bullet in enumerate(bullets):
            # checking if bullet should be removed
            if bullet.lifespan <= 0:
                bullets.pop(i)
                continue
            bullet.update()
            # also checking if bullet is on the screen
            check(bullet.pos, display_size)

        # clearing display
        display.blit(space, (0,0))
        # drawing bullets
        for bullet in bullets:
            bullet.draw(display)
        # drawing spaceships
        ship.draw(display)
        ship2.draw(display)
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
        screen.blit(pygame.transform.scale(display, screen_size), (0,0))
        # updating screen to show frame
        pygame.display.flip()
        clock.tick(FPS)


def check(pos, screen_size):
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
    main()