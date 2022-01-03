import pygame_textinput
import pygame

pygame.init()
textinput = pygame_textinput.TextInputVisualizer()
screen = pygame.display.set_mode((600, 200))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
text_input_nick = font.render('Введите имя пользователя (максимум 25 символов):', True, (0, 0, 0))
text_enter = font.render('Нажмите Enter, чтобы запустить игру.', True, (0, 0, 0))
while True:
    screen.fill((225, 225, 225))
    events = pygame.event.get()
    screen.blit(textinput.surface, (100, 100))
    if len(textinput.value) < 25:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                textinput.update(events)
    if len(textinput.value) == 25:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE1SPACE:
                screen.blit(textinput.surface, (100, 100))
    screen.blit(text_input_nick, (40, 50))
    if len(textinput.value) != 0:
        screen.blit(text_enter, (100, 150))
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            nickname_user = textinput.value
            import new_git
            exit()
    pygame.display.update()
    clock.tick(60)