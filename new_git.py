import os
import pygame
import pygame_textinput
import pygame_widgets
import sys
from PIL import ImageFont
from pygame_widgets.button import Button
import random
import sqlite3

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Epic Adventure')
clock = pygame.time.Clock()


def load_image(name, size_of_sprite=None, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if size_of_sprite:
        image = pygame.transform.scale(image, (size_of_sprite[0], size_of_sprite[1]))
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((2, 2))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Nickname:
    def __init__(self):
        super().__init__()
        global nickname_user
        lobby_image = load_image('lobby.jpg')
        textinput = pygame_textinput.TextInputVisualizer()
        textinput.font_color = (255, 255, 200)
        textinput.cursor_color = (255, 255, 255)
        font = pygame.font.Font("Arial.ttf", 40)
        text_input_nick = font.render('Введите имя пользователя (максимум 20 символов):', True, (255, 255, 255))
        text_enter = font.render('Нажмите Enter, чтобы запустить игру.', True, (255, 255, 255))
        while True:
            events = pygame.event.get()
            screen.blit(lobby_image, (0, 0))
            screen.blit(textinput.surface, (480, 300))
            if len(textinput.value) < 20:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                        textinput.update(events)
            if len(textinput.value) >= 20:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        textinput.update(events)
            screen.blit(text_input_nick, (153, 200))
            if len(textinput.value) != 0:
                screen.blit(text_enter, (293, 550))
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(textinput.value) != 0:
                    nickname_user = textinput.value
                    return
            pygame.display.update()
            clock.tick(60)


class Main_Lobby:
    def __init__(self):
        super().__init__()
        lobby_image = load_image('lobby.jpg')
        font = pygame.font.Font("Arial.ttf", 50)
        font_size = ImageFont.truetype("Arial.ttf", 50)
        font_size = font_size.getsize(f'{nickname_user}!')
        welcome_text = font.render('Добро пожаловать в Epic Adventure,', True, (255, 255, 255))
        nickname_text = font.render(f'{nickname_user}!', True, (255, 255, 255))
        button = Button(
            screen, 515, 400, 250, 100, text='Начать игру',
            fontSize=50, margin=20,
            inactiveColour=(221, 3, 225),
            pressedColour=(0, 255, 0), radius=20
        )
        button_exit = Button(
            screen, 490, 600, 300, 100, text='Выйти из игры',
            fontSize=50, margin=20,
            inactiveColour=(221, 3, 225),
            pressedColour=(0, 255, 0), radius=20,
            onClick=lambda: exit()
        )
        running = True
        while running:
            screen.blit(lobby_image, (0, 0))
            screen.blit(welcome_text, (223, 200))
            screen.blit(nickname_text, ((1280 - font_size[0]) // 2, 300))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if 750 >= pos[0] >= 500 and 500 >= pos[1] >= 400:
                        return
            pygame_widgets.update(events)
            pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.hero_image = load_image('image_part_022.png', (40, 40))
        self.hero_images_walk = [load_image('image_part_001.png', (40, 40)), load_image('image_part_002.png', (40, 40)),
                                 load_image('image_part_003.png', (40, 40)), load_image('image_part_004.png', (40, 40)),
                                 load_image('image_part_005.png', (40, 40)), load_image('image_part_006.png', (40, 40)),
                                 load_image('image_part_007.png', (40, 40)), load_image('image_part_008.png', (40, 40)),
                                 load_image('image_part_009.png', (40, 40)), load_image('image_part_010.png', (40, 40)),
                                 load_image('image_part_011.png', (40, 40)), load_image('image_part_012.png', (40, 40)),
                                 load_image('image_part_013.png', (40, 40)), load_image('image_part_014.png', (40, 40)),
                                 load_image('image_part_015.png', (40, 40)), load_image('image_part_016.png', (40, 40)),
                                 load_image('image_part_017.png', (40, 40)), load_image('image_part_018.png', (40, 40)),
                                 load_image('image_part_019.png', (40, 40)), load_image('image_part_020.png', (40, 40)),
                                 load_image('image_part_021.png', (40, 40)), load_image('image_part_023.png', (40, 40)),
                                 load_image('image_part_024.png', (40, 40)), load_image('image_part_025.png', (40, 40)),
                                 load_image('image_part_026.png', (40, 40)), load_image('image_part_027.png', (40, 40))]

        self.walk_right = False
        self.walk_left = False
        self.jump = False
        self.jump_size = 5
        self.fall_size = 1
        self.enemy_collide = enemy
        self.hero = pygame.sprite.Sprite()
        self.hero.image = self.hero_image
        self.hero.rect = self.hero.image.get_rect()
        self.hero.rect.left = 0
        self.hero.rect.bottom = 720
        self.hod_count = 0
        self.hero_speed = 5
        all_sprites.add(self.hero)

    def walk_left_fu(self):
        self.walk_right = False
        self.walk_left = True

    def walk_right_fu(self):
        self.walk_right = True
        self.walk_left = False

    def stop_walk_left_fu(self):
        self.walk_left = False

    def stop_walk_right_fu(self):
        self.walk_right = False

    def jump_fu(self):
        collides = pygame.sprite.spritecollide(self.hero, level_1.platforms, False)
        if not collides and self.hero.rect.bottom < 720:
            return
        self.jump = True

    def update(self):
        collides = pygame.sprite.spritecollide(self.hero, level_1.platforms, False)
        next_level = pygame.sprite.collide_mask(self.hero, Flag)
        if not self.walk_right and not self.walk_left:
            self.hero.image = self.hero_image

        elif self.walk_left and self.hero.rect.left > 0:
            self.hero.rect.left -= self.hero_speed
            self.hero.image = pygame.transform.flip(self.hero_images_walk[self.hod_count], True, False)
            self.hod_count = (self.hod_count + 1) % 26

        elif self.walk_right and self.hero.rect.right < 1280:
            self.hero.rect.left += self.hero_speed
            self.hero.image = self.hero_images_walk[self.hod_count]
            self.hod_count = (self.hod_count + 1) % 26

        if self.jump and self.fall_size == 1:
            if self.jump_size >= 0:
                self.hero.rect.bottom -= self.jump_size * self.jump_size
                self.jump_size -= 1
            else:
                self.jump_size = 6
                self.fall_size = -6
                self.jump = False

        for plat in collides:
            if self.hero.rect.bottom > plat.rect.top:
                self.hero.rect.bottom = plat.rect.top + 1
        if not collides and self.hero.rect.bottom < 720 and not self.jump:
            self.hero.rect.bottom += self.fall_size
            self.fall_size += 1
        else:
            self.fall_size = 1

        for enemy in self.enemy_collide:
            if pygame.sprite.collide_mask(self.hero, enemy):
                print('***Экран информирующий о поражении***')

        if next_level:
            print('Переход на уровень 2')

        if self.hero.rect.bottom > 720:
            self.hero.rect.bottom = 720

        if self.hero.rect.bottom > 720:
            self.hero.rect.bottom = 720

        if self.hero.rect.top < 0:
            self.hero.rect.top = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, size, cords, *group):
        super().__init__(*group)
        self.image = load_image('platform1.jpg', size)
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, cords, border_left, border_right, speed, *group):
        super().__init__(*group)
        self.enemy_images_walk = [load_image('monster1.png', size),
                                  load_image('monster2.png', size),
                                  load_image('monster3.png', size),
                                  load_image('monster4.png', size),
                                  load_image('monster5.png', size)]
        self.walk_right_e = False
        self.walk_left_e = True
        self.fall_size_e = 1
        self.walk_count = random.choice(range(0, 5))
        self.image = self.enemy_images_walk[self.walk_count]
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.enemy_speed = speed
        self.b_l = border_left
        self.b_r = border_right
        self.mask = pygame.mask.from_surface(self.image)

    def update_e(self):
        self.image = self.enemy_images_walk[int(self.walk_count // 1)]

        if self.walk_left_e:
            self.image = pygame.transform.flip(self.enemy_images_walk[int(self.walk_count // 1)], True, False)
            self.walk_count = (self.walk_count + 0.2) % 5
            self.rect.x -= self.enemy_speed
        elif self.walk_right_e:
            self.walk_count = (self.walk_count + 0.2) % 5
            self.rect.x += self.enemy_speed
        if self.rect.x <= self.b_l:
            self.walk_right_e = True
            self.walk_left_e = False
        elif self.rect.x >= self.b_r:
            self.walk_right_e = False
            self.walk_left_e = True


class Flag(pygame.sprite.Sprite):
    def __init__(self, coord, *group):
        super().__init__(*group)
        self.image = load_image('end_flag.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = coord
        self.mask = pygame.mask.from_surface(self.image)


class Level_1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        enemies_on_level = [[(40, 40), (100, 260), 0, 250, 2], [(60, 60), (800, 460), 600, 800, 1]]
        layers_on_level = [[(300, 40), (100, 300)], [(80, 40), (300, 430)], [(50, 20), (500, 500)],
                           [(200, 20), (700, 500)], [(110, 20), (1000, 600)]]
        for platform in layers_on_level:
            Platform(platform[0], platform[1], self.platforms, all_sprites)
        for enemy in enemies_on_level:
            Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], self.enemies, all_sprites)


Nickname()
Main_Lobby()
background_image = load_image('background.png')
all_sprites = pygame.sprite.Group()
level_1 = Level_1()
Hero = Player(level_1.enemies)
Flag = Flag((30, 255), all_sprites)
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                Hero.walk_right_fu()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                Hero.walk_left_fu()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                Hero.jump_fu()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                Hero.stop_walk_left_fu()
            if event.key == pygame.K_RIGHT:
                Hero.stop_walk_right_fu()
    Hero.update()
    for elem in level_1.enemies:
        elem.update_e()
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
