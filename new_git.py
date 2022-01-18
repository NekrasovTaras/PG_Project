import os
import pygame
import pygame_textinput
import pygame_widgets
import random
import sqlite3
import sys
from datetime import datetime
import time
from PIL import ImageFont
from pygame_widgets.button import Button


con = sqlite3.connect('game_base.sqlite')
cur = con.cursor()
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Epic Adventure')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


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
        pygame.mixer.music.load("music/main_lobby.mp3")
        pygame.mixer.music.play(-1)
        lobby_image = load_image('lobby.jpg')
        textinput = pygame_textinput.TextInputVisualizer()
        textinput.font_color = (255, 255, 200)
        textinput.cursor_color = (255, 255, 255)
        font = pygame.font.Font("Arial.ttf", 40)
        text_input_nick = font.render('Введите имя пользователя (максимум 12 символов):', True, (255, 255, 255))
        text_enter = font.render('Нажмите Enter, чтобы запустить игру.', True, (255, 255, 255))
        while True:
            events = pygame.event.get()
            screen.blit(lobby_image, (0, 0))
            screen.blit(textinput.surface, (520, 300))
            if len(textinput.value) < 12:
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                        textinput.update(events)
            if len(textinput.value) >= 12:
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
        self.time_of_game = None
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
                        pygame.mixer.music.stop()
                        self.time_of_game = time.time()
                        return
            pygame_widgets.update(events)
            pygame.display.update()


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.win = False
        self.win_time = 0
        self.number_of_level = 1
        self.old_n_o_l = 1
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def next_level(self):
        global all_sprites
        all_sprites = pygame.sprite.Group()
        for platform in self.platforms:
            platform.kill()
        for enemy in self.enemies:
            enemy.kill()
        try:
            file = open(f"level_{self.number_of_level}.txt", mode="r", encoding="UTF-8")
            n = 0
            enemies_on_level = []
            layers_on_level = []
            for line in file.readlines():
                if line == "":
                    continue
                if n == 0:
                    if line.split()[0] == "Enemy":
                        n = 1
                    else:
                        line = list(map(int, line.split()))
                        self.Flag = Flag((line[0], line[1]), all_sprites)
                elif n == 1:
                    if line.split()[0] == "Platform":
                        n = 2
                    else:
                        line = list(map(int, line.split()))
                        enemies_on_level.append([(line[0], line[1]), (line[2], line[3]), line[4], line[5], line[6]])
                elif n == 2:
                    line = list(map(int, line.split()))
                    layers_on_level.append([(line[0], line[1]), (line[2], line[3])])
            for platform in layers_on_level:
                Platform(platform[0], platform[1], self.platforms, all_sprites)
            for enemy in enemies_on_level:
                Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], self.enemies, all_sprites)
            if self.number_of_level != self.old_n_o_l:
                Hero.hero.kill()
                Hero.__init__(level.enemies)
                self.old_n_o_l = self.number_of_level
            pygame.display.flip()
        except:
            self.win_time = time.time() - lobby.time_of_game
            self.win_time = round(self.win_time, 2)
            pygame.mixer.music.load("music/win.mp3")
            pygame.mixer.music.play(-1)
            self.win = True


class Flag(pygame.sprite.Sprite):
    def __init__(self, coord, *group):
        super().__init__(*group)
        self.image = load_image('end_flag.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = coord
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    def __init__(self, size, cords, *group):
        super().__init__(*group)
        self.image = load_image('platform1.jpg', size)
        self.rect = self.image.get_rect()
        self.rect.center = cords
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.death = False
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
        collides = pygame.sprite.spritecollide(self.hero, level.platforms, False)
        if not collides and self.hero.rect.bottom < 720:
            return
        self.jump = True

    def update(self):
        collides = pygame.sprite.spritecollide(self.hero, level.platforms, False)
        next_level = pygame.sprite.collide_mask(self.hero, level.Flag)
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
                pygame.mixer.music.load("music/death.mp3")
                pygame.mixer.music.play(-1)
                self.death = True

        if next_level:
            level.number_of_level += 1
            level.next_level()

        if self.hero.rect.bottom > 720:
            self.hero.rect.bottom = 720

        if self.hero.rect.bottom > 720:
            self.hero.rect.bottom = 720

        if self.hero.rect.top < 0:
            self.hero.rect.top = 0


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


level = Level()
Nickname()
lobby = Main_Lobby()
background_image = load_image('background.png')
table_image = load_image('Table.png')
game_over_image = load_image('game_over.jpg')
win_image = load_image('win.jpg')
white_screen_image = load_image('white_screen.png')
level.next_level()
pygame.mixer.music.load("music/game.mp3")
pygame.mixer.music.play(-1)
Hero = Player(level.enemies)
pygame.display.flip()
FPS = 60
win_exit = 0
base_win = 0

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
    for elem in level.enemies:
        elem.update_e()
    if level.win:
        if base_win == 0:
            name = cur.execute(
                f"""SELECT Nickname, Time FROM Players""").fetchall()
            all_nick = []
            for nick in name:
                nick = nick[0]
                all_nick.append(nick)
            if nickname_user in all_nick:
                if float(name[all_nick.index(nickname_user)][1]) > level.win_time:
                    cur.execute(
                        f"""DELETE from Players WHERE Nickname = '{nickname_user}'""")
                    cur.execute(
                        f"""INSERT INTO Players (Nickname, Time, Date)
                                        VALUES ('{nickname_user}', '{level.win_time}', '{datetime.now().date()}');""")
                    con.commit()
            else:
                cur.execute(
                    f"""INSERT INTO Players (Nickname, Time, Date)
                        VALUES ('{nickname_user}', '{level.win_time}', '{datetime.now().date()}');""")
                con.commit()
            base_win = 1
        else:
            pass
        if win_exit == 0:
            screen.blit(win_image, (0, 0))
            font = pygame.font.Font("Arial.ttf", 50)
            win_text = font.render('Нажмите Space, чтобы продолжить.', True, (255, 255, 255))
            screen.blit(win_text, (220, 600))
            pygame.display.flip()
        else:
            players = cur.execute(
                f"""SELECT * FROM Players ORDER BY Time ASC""").fetchall()
            screen.fill([255, 255, 255])
            screen.blit(table_image, (50, 150))
            font_size = ImageFont.truetype("Arial.ttf", 25)
            font = pygame.font.Font("Arial.ttf", 25)
            text = font.render(f'Никнейм:', True, (0, 0, 0))
            screen.blit(text, (180, 180))
            text = font.render(f'Время(в секунда):', True, (0, 0, 0))
            screen.blit(text, (525, 180))
            text = font.render(f'Дата:', True, (0, 0, 0))
            screen.blit(text, (980, 180))
            if len(players) == 1:
                screen.blit(white_screen_image, (50, 315))
            elif len(players) == 2:
                screen.blit(white_screen_image, (50, 395))
            elif len(players) == 3:
                screen.blit(white_screen_image, (50, 475))
            elif len(players) == 4:
                screen.blit(white_screen_image, (50, 555))
            if len(players) >= 5:
                for i in range(0, 5):
                    size = font_size.getsize(f'{players[i][0]}')
                    text = font.render(f'{players[i][0]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (435 - size[0]) // 2, 270 + i * 75))
                    size = font_size.getsize(f'{players[i][1]}')
                    text = font.render(f'{players[i][1]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (1210 - size[0]) // 2, 270 + i * 75))
                    size = font_size.getsize(f'{players[0][2]}')
                    text = font.render(f'{players[i][2]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (1970 - size[0]) // 2, 270 + i * 75))
            else:
                for i in range(0, len(players)):
                    size = font_size.getsize(f'{players[i][0]}')
                    text = font.render(f'{players[i][0]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (435 - size[0]) // 2, 270 + i * 80))
                    size = font_size.getsize(f'{players[i][1]}')
                    text = font.render(f'{players[i][1]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (1210 - size[0]) // 2, 270 + i * 80))
                    size = font_size.getsize(f'{players[0][2]}')
                    text = font.render(f'{players[i][2]}', True, (0, 0, 0))
                    screen.blit(text, (25 + (1970 - size[0]) // 2, 270 + i * 80))
            font = pygame.font.Font("Arial.ttf", 50)
            win_text_1 = font.render('Топ игроков за всё время:', True, (0, 0, 0))
            win_text_2 = font.render('Нажмите Enter, чтобы перейти в главное меню.', True, (0, 0, 0))
            screen.blit(win_text_1, (300, 50))
            screen.blit(win_text_2, (83, 630))
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                win_exit = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and win_exit == 1:
                base_win = 0
                win_exit = 0
                level.win = False
                level.number_of_level = 1
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/main_lobby.mp3")
                pygame.mixer.music.play(-1)
                lobby = Main_Lobby()
                for platform in level.platforms:
                    platform.kill()
                for enemy in level.enemies:
                    enemy.kill()
                Hero.death = False
                pygame.mixer.music.load("music/game.mp3")
                pygame.mixer.music.play(-1)
                level.next_level()
                Hero.hero.kill()
                Hero.__init__(level.enemies)
    elif Hero.death:
        screen.blit(game_over_image, (0, 0))
        font = pygame.font.Font("Arial.ttf", 50)
        death_text = font.render('Нажмите Enter, чтобы перейти в главное меню.', True, (255, 255, 255))
        screen.blit(death_text, (83, 600))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                level.number_of_level = 1
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/main_lobby.mp3")
                pygame.mixer.music.play(-1)
                lobby = Main_Lobby()
                for platform in level.platforms:
                    platform.kill()
                for enemy in level.enemies:
                    enemy.kill()
                Hero.death = False
                pygame.mixer.music.load("music/game.mp3")
                pygame.mixer.music.play(-1)
                level.next_level()
                Hero.hero.kill()
                Hero.__init__(level.enemies)
    else:
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
