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


background_image = load_image('background.jpg')
hero_image = load_image('image_part_022.png')
hero_images_walk = [load_image('image_part_001.png'), load_image('image_part_002.png'),
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

WALK_RIGHT = True


all_sprites = pygame.sprite.Group()
hero = pygame.sprite.Sprite()
hero.image = hero_image
hero.rect = hero.image.get_rect()
hero.rect.left = 0
hero.rect.bottom = 1080
all_sprites.add(hero)

hod_count = 0
hero_speed = 10
FPS = 50
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and hero.rect.left > 0:
            hero.rect.left -= hero_speed
            hero.image = hero_images_walk[hod_count]
            hod_count = (hod_count + 1) % 26
            print(hod_count)

        if key[pygame.K_RIGHT] and hero.rect.right < 1920:
            hero.rect.left += hero_speed
            hero.image = hero_images_walk[hod_count]
            hod_count = (hod_count + 1) % 26
            print(hod_count)

    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
