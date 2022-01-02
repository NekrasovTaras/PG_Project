import os
import pygame
import sys

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Epic adventure')


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('Файла не существует')
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hero_image = load_image('image_part_022.png')
        self.hero_images_walk = [load_image('image_part_001.png'), load_image('image_part_002.png'),
                            load_image('image_part_003.png'), load_image('image_part_004.png'),
                            load_image('image_part_005.png'), load_image('image_part_006.png'),
                            load_image('image_part_007.png'), load_image('image_part_008.png'),
                            load_image('image_part_009.png'), load_image('image_part_010.png'),
                            load_image('image_part_011.png'), load_image('image_part_012.png'),
                            load_image('image_part_013.png'), load_image('image_part_014.png'),
                            load_image('image_part_015.png'), load_image('image_part_016.png'),
                            load_image('image_part_017.png'), load_image('image_part_018.png'),
                            load_image('image_part_019.png'), load_image('image_part_020.png'),
                            load_image('image_part_021.png'), load_image('image_part_023.png'),
                            load_image('image_part_024.png'), load_image('image_part_025.png'),
                            load_image('image_part_026.png'), load_image('image_part_027.png')]
        
        self.WALK_RIGHT = False
        self.WALK_LEFT = False
        self.JUMP = False
        self.jump_size = 8

        self.hero = pygame.sprite.Sprite()
        self.hero.image = self.hero_image
        self.hero.rect = self.hero.image.get_rect()
        self.hero.rect.left = 0
        self.hero.rect.bottom = 1080
        self.hod_count = 0
        self.hero_speed = 10
        all_sprites.add(self.hero)
        
    def Walk_Left(self):
        self.WALK_RIGHT = False
        self.WALK_LEFT = True
        
    def Walk_Right(self):
        self.WALK_RIGHT = True
        self.WALK_LEFT = False

    def Stop_Walk_Left(self):
        self.WALK_LEFT = False

    def Stop_Walk_Right(self):
        self.WALK_RIGHT = False

    def Jump(self):
        self.JUMP = True

    def Update(self):
        if not self.WALK_RIGHT and not self.WALK_LEFT:
            self.hero.image = self.hero_image

        elif self.WALK_LEFT and self.hero.rect.left > 0:
            self.hero.rect.left -= self.hero_speed
            self.hero.image = pygame.transform.flip(self.hero_images_walk[self.hod_count], True, False)
            self.hod_count = (self.hod_count + 1) % 26

        elif self.WALK_RIGHT and self.hero.rect.right < 1920:
            self.hero.rect.left += self.hero_speed
            self.hero.image = self.hero_images_walk[self.hod_count]
            self.hod_count = (self.hod_count + 1) % 26

        if self.JUMP:
            if self.jump_size >= -8:
                self.hero.rect.bottom -= self.jump_size * abs(self.jump_size)
                self.jump_size -= 1
            else:
                self.jump_size = 8
                self.JUMP = False

        collides = pygame.sprite.spritecollide(self.hero, level_1.platformi, False)
        for plat in collides:
            if self.hero.rect.bottom >= plat.rect.top:
                self.hero.rect.bottom = plat.rect.top

        if not collides and self.hero.rect.bottom < 1080 and not self.JUMP:
            self.hero.rect.bottom += 5


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('platform_fly.png')
        self.rect = self.image.get_rect()


class Level_1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.platformi = pygame.sprite.Group()
        layers_on_level = [[1300, 800], [200, 400]]
        for platform in layers_on_level:
            block = Platform()
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            self.platformi.add(block)
        all_sprites.add(self.platformi)


background_image = load_image('background.jpg')
all_sprites = pygame.sprite.Group()
level_1 = Level_1()
Hero = Player()
FPS = 50
clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                Hero.Walk_Right()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                Hero.Walk_Left()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                Hero.Jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                Hero.Stop_Walk_Left()
            if event.key == pygame.K_RIGHT:
                Hero.Stop_Walk_Right()
    Hero.Update()
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
