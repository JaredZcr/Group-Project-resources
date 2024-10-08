import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Character Movement, Jumping, and Throwing")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

background_image = pygame.image.load(r'C:\Users\zcrcs\Desktop\qVtx2.png')
background_image = pygame.transform.scale(background_image, (1200, 800))

character_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Dude_Monster.png')
character_image = pygame.transform.scale(character_image, (64, 64))

throw_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Dude_Monster_Attack2_6.png')
frame_width = throw_image.get_width() // 6
frame_height = throw_image.get_height()
throw_frames = [pygame.transform.scale(throw_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)), (64, 64)) for i in range(6)]

snowball_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Rock2.png')

jump_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Dude_Monster_Jump_8.png')
jump_frame_width = jump_image.get_width() // 8
jump_frames = [pygame.transform.scale(jump_image.subsurface(pygame.Rect(i * jump_frame_width, 0, jump_frame_width, jump_image.get_height())), (64, 64)) for i in range(8)]

jump_dust_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Double_Jump_Dust_5.png')
dust_frame_width = jump_dust_image.get_width() // 5
dust_frames = [pygame.transform.scale(jump_dust_image.subsurface(pygame.Rect(i * dust_frame_width, 0, dust_frame_width, jump_dust_image.get_height())), (64, 32)) for i in range(5)]

run_image = pygame.image.load(r'C:\Users\zcrcs\Downloads\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\3 Dude_Monster\Dude_Monster_Run_6.png')
run_frame_width = run_image.get_width() // 6
run_frames = [pygame.transform.scale(run_image.subsurface(pygame.Rect(i * run_frame_width, 0, run_frame_width, run_image.get_height())), (64, 64)) for i in range(6)]

character_rect = character_image.get_rect()
character_rect.topleft = (375, 680)

snowballs = []
player_speed = 5
jump_power = 15
gravity = 0.8
is_jumping = False
vertical_velocity = 0
ground_level = 680
direction = 'right'

jump_frame_index = 0
jump_frame_rate = 5
jump_frame_counter = 0

dust_frame_index = 0
dust_frame_rate = 5
dust_frame_counter = 0

run_frame_index = 0
run_frame_rate = 5
run_frame_counter = 0

is_throwing = False
throw_frame_index = 0
throw_frame_rate = 5
throw_frame_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_throwing = True
            throw_frame_index = 0
            snowball_rect = snowball_image.get_rect()
            snowball_rect.center = character_rect.center
            snowballs.append({'rect': snowball_rect, 'direction': direction})

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        character_rect.x -= player_speed
        direction = 'left'
        run_frame_counter += 1
        if run_frame_counter >= run_frame_rate:
            run_frame_index = (run_frame_index + 1) % len(run_frames)
            run_frame_counter = 0
    elif keys[pygame.K_RIGHT]:
        character_rect.x += player_speed
        direction = 'right'
        run_frame_counter += 1
        if run_frame_counter >= run_frame_rate:
            run_frame_index = (run_frame_index + 1) % len(run_frames)
            run_frame_counter = 0

    if not is_jumping:
        if keys[pygame.K_UP]:
            is_jumping = True
            vertical_velocity = -jump_power
    else:
        vertical_velocity += gravity
        character_rect.y += vertical_velocity

        if character_rect.y >= ground_level:
            character_rect.y = ground_level
            is_jumping = False

    for snowball in snowballs:
        if snowball['direction'] == 'right':
            snowball['rect'].x += 10
        elif snowball['direction'] == 'left':
            snowball['rect'].x -= 10

    snowballs = [snowball for snowball in snowballs if 0 < snowball['rect'].x < 1200]

    screen.blit(background_image, (0, 0))

    if is_jumping:
        screen.blit(dust_frames[dust_frame_index], (character_rect.x, character_rect.y + 50))
        dust_frame_counter += 1
        if dust_frame_counter >= dust_frame_rate:
            dust_frame_index = (dust_frame_index + 1) % len(dust_frames)
            dust_frame_counter = 0

        screen.blit(jump_frames[jump_frame_index], character_rect)
        jump_frame_counter += 1
        if jump_frame_counter >= jump_frame_rate:
            jump_frame_index = (jump_frame_index + 1) % len(jump_frames)
            jump_frame_counter = 0
    elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        screen.blit(run_frames[run_frame_index], character_rect)
    else:
        if is_throwing:
            screen.blit(throw_frames[throw_frame_index], character_rect)
            throw_frame_counter += 1
            if throw_frame_counter >= throw_frame_rate:
                throw_frame_index += 1
                throw_frame_counter = 0
            if throw_frame_index >= len(throw_frames):
                is_throwing = False
                throw_frame_index = 0
        else:
            screen.blit(character_image, character_rect)

    for snowball in snowballs:
        screen.blit(snowball_image, snowball['rect'])

    pygame.display.flip()
    pygame.time.Clock().tick(60)
