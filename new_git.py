import os
import sys

import pygame
import pygame_textinput
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Epic Adventure')
clock = pygame.time.Clock()


def start():
    return


def exit_game():
    exit()


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
        textinput.font_color = (255, 255, 255)
        textinput.cursor_color = (255, 255, 255)
        font = pygame.font.Font(None, 40)
        text_input_nick = font.render('Введите имя пользователя (максимум 20 символов):', True, (255, 255, 255))
        text_enter = font.render('Нажмите Enter, чтобы запустить игру.', True, (255, 255, 255))
        while True:
            events = pygame.event.get()
            screen.blit(lobby_image, (0, 0))
            screen.blit(textinput.surface, (500, 300))
            if len(textinput.value) < 20:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                        textinput.update(events)
            if len(textinput.value) == 20:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        textinput.update(events)
            screen.blit(text_input_nick, (280, 200))
            if len(textinput.value) != 0:
                screen.blit(text_enter, (380, 600))
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
        font = pygame.font.Font(None, 50)
        welcome_text = font.render('Добро пожаловать в Epic Adventure,', True, (255, 255, 255))
        nickname_text = font.render(f'{nickname_user}!', True, (255, 255, 255))
        button = Button(
            screen, 500, 400, 250, 100, text='Начать игру',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=lambda: print()
        )
        button_exit = Button(
            screen, 480, 600, 300, 100, text='Выйти из игры',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=lambda: exit()
        )
        running = True
        while running:
            screen.blit(lobby_image, (0, 0))
            screen.blit(welcome_text, (300, 200))
            screen.blit(nickname_text, (530, 300))
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

        self.walk_right = False
        self.walk_left = False
        self.jump = False
        self.jump_size = 8
        self.fall_size = 1

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
        self.jump = True

    def update(self):
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
                self.jump_size = 8
                self.fall_size = -8
                self.jump = False

        collides = pygame.sprite.spritecollide(self.hero, level_1.platforms, False)
        for plat in collides:
            if self.hero.rect.bottom > plat.rect.top:
                self.hero.rect.bottom = plat.rect.top + 1
        if not collides and self.hero.rect.bottom < 720 and not self.jump:
            self.hero.rect.bottom += self.fall_size
            self.fall_size += 1
        else:
            self.fall_size = 1

        monster

        if self.hero.rect.bottom > 720:
            self.hero.rect.bottom = 720



class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('platform1.jpg', (300, 20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_images_walk = [load_image('monster1.png', (100, 100)),
                                  load_image('monster2.png', (100, 100)),
                                  load_image('monster3.png', (100, 100)),
                                  load_image('monster4.png', (100, 100)),
                                  load_image('monster5.png', (100, 100))]
        self.walk_right_e = False
        self.walk_left_e = True
        self.fall_size_e = 1
        self.walk_count = 0
        self.image = self.enemy_images_walk[0]
        self.rect = self.image.get_rect()
        self.coord_nach = self.rect.right
        self.enemy_hod_count = 0
        self.enemy_speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update_e(self):
        self.image = self.enemy_images_walk[int(self.enemy_hod_count // 1)]
        if self.walk_left_e:
            self.image = pygame.transform.flip(self.enemy_images_walk[int(self.enemy_hod_count // 1)], True, False)
        self.enemy_hod_count = (self.enemy_hod_count + 0.2) % 5
        self.rect.x += self.enemy_speed
        if self.rect.left - 15 > self.coord_nach:
            self.walk_left_e = True
            self.walk_right_e = False
            self.enemy_speed = -2
        elif self.rect.left + 15 < self.coord_nach:
            self.walk_left_e = False
            self.walk_right_e = True
            self.enemy_speed = 2


class Level_1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        enemies_on_level = [[600, 80], [900, 400]]
        layers_on_level = [[500, 100], [200, 400]]
        for platform in layers_on_level:
            block = Platform()
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            self.platforms.add(block)
        for enemy in enemies_on_level:
            vrag = Enemy()
            vrag.rect.x = enemy[0]
            vrag.rect.y = enemy[1]
            self.enemies.add(vrag)
        all_sprites.add(self.platforms)
        all_sprites.add(self.enemies)


Nickname()
Main_Lobby()
background_image = load_image('background.png')
all_sprites = pygame.sprite.Group()
level_1 = Level_1()
Hero = Player()
FPS = 40

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
