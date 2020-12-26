import pygame
import os

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('파이팡')

clock = pygame.time.Clock()
 
game_font = pygame.font.Font(None, 40)
total_time = 20
start_ticks = pygame.time.get_ticks()

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

background = pygame.image.load(os.path.join(image_path, 'background.png'))

stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - stage_height - character_height

character_speed = 0.4
character_to_x = 0

weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

weapon_speed = 0.8
weapons = []

ball_images = [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')),
    pygame.image.load(os.path.join(image_path, 'balloon2.png')),
    pygame.image.load(os.path.join(image_path, 'balloon3.png')),
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))]

ball_spd_y = [-18, -15, -12, -9 ]
balls = []

balls.append({
    'pos_x' : 50,
    'pos_y' : 50,
    'img_idx' : 0,
    'to_x' : 3,
    'to_y' : -8,
    'init_spd_y' : ball_spd_y[0]})

weapon_to_remove = -1 
ball_to_remove = -1

game_result = 'Game Over'

running = True
while running:
    dt =clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_y_pos = screen_height
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x *dt

    if character_x_pos <= 0:
        character_x_pos = 0
        
    elif character_x_pos + character_width >= screen_width:
        character_x_pos = screen_width - character_width

    weapons = [ [w[0], w[1] - weapon_speed * dt] for w in weapons]

    weapons = [ [w[0], w[1] ] for w in weapons if w[1] > 0]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img = ball_images[ball_val['img_idx']]

        ball_size = ball_img.get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_y + ball_height >= screen_height - stage_height:
            ball_val['to_y'] = ball_val['init_spd_y']

        if ball_pos_x <= 0 or ball_pos_x + ball_width >= screen_width:
            ball_val['to_x'] = ball_val['to_x'] * -1

        else:
            ball_val['to_y'] += 0.3

        ball_val['pos_y'] += ball_val['to_y']
        ball_val['pos_x'] += ball_val['to_x']
    
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img = ball_images[ball_val['img_idx']]

        ball_rect = ball_img.get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False

        for weapon_idx, weapon_pos in enumerate(weapons):
            weapon_pos_x = weapon_pos[0]
            weapon_pos_y = weapon_pos[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                
                if ball_val['img_idx'] < 3:
                    ball_height = ball_rect.size[0]
                    ball_width = ball_rect.size[1]

                    small_ball_size = ball_images[ball_val['img_idx'] + 1].get_rect().size
                    small_ball_width = small_ball_size[0]
                    small_ball_height = small_ball_size[1]

                    balls.append({
                        'pos_x' : ball_pos_x + ball_width / 2 - small_ball_width / 2,
                        'pos_y' : ball_pos_y + ball_height / 2 -small_ball_height / 2,
                        'to_x' : 3,
                        'to_y' : -8,
                        'img_idx' : ball_val['img_idx'] + 1,
                        'init_spd_y' : ball_spd_y[ball_val['img_idx'] + 1]})

                    balls.append({
                        'pos_x' : ball_pos_x + ball_width / 2 - small_ball_width / 2,
                        'pos_y' : ball_pos_y + ball_height / 2 -small_ball_height / 2,
                        'to_x' : -3,
                        'to_y' : -8,
                        'img_idx' : ball_val['img_idx'] + 1,
                        'init_spd_y' : ball_spd_y[ball_val['img_idx'] + 1]})

                break


    if weapon_to_remove != -1:
        del weapons[weapon_to_remove]
        del balls[ball_to_remove]

        weapon_to_remove = -1
        ball_to_remove = -1
                   
    screen.blit(background, (0, 0))

    if len(balls) == 0:
        game_result = 'Misson Complite'
        running = False

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img = ball_images[ball_val['img_idx']]
        screen.blit(ball_img, (ball_pos_x, ball_pos_y))


    for weapon_pos in weapons:
        screen.blit(weapon, (weapon_pos[0], weapon_pos[1]))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render('Time : {}'.format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = 'Time Over'
        running = False
        
    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(1000)
pygame.quit()