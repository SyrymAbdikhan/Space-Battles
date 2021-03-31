
import os

import physics
import helper

import pygame


class Spaceship:
    def __init__(self, pos, acc, rot_acc, controller, folder_name):
        # entity physics and properties
        self.object = physics.Object(pos)
        self.acc = acc
        self.rot_acc = rot_acc
        self.controller = controller
        # initializing animations
        self.animations = load_animations(folder_name)
        self.state = "idle"
        self.anim_count = 0
        # bullet acceleration and cooldown between each shoot
        self.bull_acc = 4
        self.shoot_cooldown = helper.Timer(12)
        # health state and cooldown
        self.health = 20
        self.reset_cooldown = helper.Timer(600)
        # making bullet mask for collision detection
        bullet_surf = pygame.Surface((1,1))
        bullet_surf.fill((255,255,255))
        bullet_surf = bullet_surf.convert_alpha()
        self.bullet_mask = pygame.mask.from_surface(bullet_surf)

    def update(self, keys, bullets):
        self.change_state("idle")
        if self.health > 0:
            # moving and rotating trigger
            if keys[self.controller[0]]:
                self.object.move(self.acc)
                self.change_state("moving")
            if keys[self.controller[1]]:
                self.object.move(-self.acc*0.2)
            if keys[self.controller[2]]:
                self.object.rotate(-self.rot_acc)
            if keys[self.controller[3]]:
                self.object.rotate(self.rot_acc)
            # shooting trigger
            self.shoot_cooldown.update()
            if keys[self.controller[4]] and self.shoot_cooldown.do:
                self.add_bullet(bullets)
                self.shoot_cooldown.do = False
        elif self.health == 0 and self.reset_cooldown.do:
            self.reset_cooldown.do = False
        else:
            # reset cooldown
            self.reset_cooldown.update()
            if self.reset_cooldown.do:
                self.health = 20
                self.reset_cooldown.do = True
        
        # checking for hits
        if bullets:
            # getting mask of rotated spaceship
            img, rot_img, rect = self.get_img_rect()
            img_mask = pygame.mask.from_surface(rot_img)
            # looping through every bullet
            for i, bullet in enumerate(bullets):
                # checking if bullet is nearby
                dist = get_dist(self.object.pos, bullet.pos)
                if dist <= 20:
                    # calculating offset
                    offset = int(rect.x - bullet.pos.x), int(rect.y - bullet.pos.y)
                    if self.bullet_mask.overlap(img_mask, offset):
                        if self.health > 0:
                            self.health -= 1
                        bullets.pop(i)
                
        # updating object physics
        self.object.update()
        
        # increasing count by 1 to the next anitmation
        self.anim_count += 1
        # making sure that count do not get out of range
        if self.anim_count >= len(self.animations[self.state]):
            self.anim_count = 0

    def draw(self, surf):
        # rotating image
        img, rot_img, rect = self.get_img_rect()
        surf.blit(rot_img, rect.topleft)
        # determining health bar position and size
        w = 40
        w2 = w * self.health // 20
        h = 5
        x = self.object.pos.x - w//2
        y = self.object.pos.y - (img.get_height() + h)
        # drawing health bar
        pygame.draw.rect(surf, (223,52,52), (x ,y, w, h))
        pygame.draw.rect(surf, (113,205,83), (x ,y, w2, h))
    
    def change_state(self, state):
        if state in self.animations and self.state != state:
            self.state = state
            self.anim_count = 0
    
    def add_bullet(self, bullets):
        # getting idle image
        img = self.animations["idle"][0]
        # getting current direction
        obj_dir = self.object.get_dir()
        # calculating velocity of bullet
        vel = self.object.vel + obj_dir * self.bull_acc
        # determining position of the bullet
        pos = self.object.pos + obj_dir * (img.get_height()/2) * 1.1
        # creating a bullet
        bullet = Bullet(pos, vel)
        bullets.append(bullet)
    
    def get_img_rect(self):
        # getting current image
        img = self.animations[self.state][self.anim_count]
        # rotating image
        rot_img = pygame.transform.rotate(img, -self.object.angle-90)
        rect = rot_img.get_rect()
        # centering image
        rect.center = self.object.pos
        return img, rot_img, rect


class Bullet:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.lifespan = 1200
    
    def draw(self, surf):
        x, y = self.pos
        pygame.gfxdraw.pixel(surf, int(x), int(y), (169,133,245))
    
    def update(self):
        self.pos += self.vel
        self.lifespan -= 1


def load_animations(path):
    animations = {}
    img_extensions = (".png", ".jpg", ".jpeg")
    # getting every file and folder
    states = os.listdir(path)
    # looping through file/folder names
    for state in states:
        # getting full path to the folder
        sub_path = os.path.join(path, state)
        # skips if it is not a folder
        if not os.path.isdir(sub_path):
            continue
        # preparing space for images
        animations[state] = []
        # getting all images from that folder
        imgs = os.listdir(sub_path)
        # looping through images
        for img in imgs:
            # getting image full path
            full_path = os.path.join(sub_path, img)
            # skips if it is not an image
            if not full_path.endswith(img_extensions):
                continue
            # loading image
            surf = pygame.image.load(full_path).convert_alpha()
            # adding image to that stae
            animations[state].append(surf)
    
    return animations


def get_dist(v1, v2):
    return ((v1.x-v2.x)**2+(v1.y-v2.y)**2)**0.5