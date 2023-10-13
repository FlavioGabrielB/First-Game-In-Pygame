# importing all libraries
import pygame
import math
from random import randint
from timeit import default_timer as timer

def level():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((720, 600))
    clock = pygame.time.Clock()
    running = True
    colison_fruit = False
    colison_entity = False
    colison_enemy = False
    speed = 2
    r1 = 20
    dt = 0
    score = 0
    fruit_pos_x = randint(1, screen.get_width())
    fruit_pos_y = randint(1, screen.get_height())
    cont = 0
    restart_time = 3

    # font config
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)
    text_score_cont = ""
    text_score_pos = (70, 30)
    text_life_cont = ""
    text_life_pos = (60, 70)
    text_time_cont = ""
    text_time_pos = (80, 100)
    text_game_over = "Game Over!"
    text_game_over_pos = (screen.get_width()/2, screen.get_height()/2)
    text_time_game_over = ""
    text_time_game_over_pos = (screen.get_width()/2, screen.get_height()/2+100)

    # player config
    life = 3
    invulnerable_time = 1000
    last_hit_time = 0
    player_color = "red"
    special_time = 5000
    special_cont = 0
    special = False
    last_special_time = 0
    special_current_time = 0
    dead_current_time = 0
    is_live = True

    # set fruit and player position
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    entity_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)
    fruit_pos = pygame.Vector2(fruit_pos_x, fruit_pos_y)

    # function for detect colision
    def circles_collide(player_x, player_y, r1, obj_x, obj_y, r2):
        distance = math.sqrt((player_x - obj_x)**2 + (player_y - obj_y)**2)
        return distance < r1 + r2

    def random_pos():
        fruit_pos_x = randint(1, screen.get_width())
        fruit_pos_y = randint(1, screen.get_height())
        return fruit_pos_x, fruit_pos_y

    # calculate the distance and set the position actual of entity
    def move_towards(obj, target, speed):
        dx = target.x - obj.x
        dy = target.y - obj.y
        dist = math.sqrt(dx * dx + dy * dy)

        dx = dx / dist * speed
        dy = dy / dist * speed

        obj[0] += dx
        obj[1] += dy

    def time_player_hit(current_time, life, last_hit_time, color):
        if current_time - last_hit_time > invulnerable_time:
            life -=1
            last_hit_time = current_time
            color = "white"
        elif(current_time - last_hit_time < invulnerable_time):
            color = "red"
        return life, last_hit_time, color
    
    def special_mod(special, current_time, special_current_time, special_time, color):
        
        # print(special_current_time)

        if special:
            if current_time - special_current_time > special_time:
                color = "red"
                special = False
            else:
                color = "orange"
        return color, special
    
    enemies = []

    while running:
        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        current_time = pygame.time.get_ticks()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw the objects
        if(is_live):
            pygame.draw.circle(screen, player_color, player_pos, r1)
        pygame.draw.circle(screen, "green", entity_pos, r1)

        if not colison_fruit:
            pygame.draw.circle(screen, "purple", fruit_pos, r1)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        if circles_collide(player_pos.x, player_pos.y, r1, fruit_pos.x, fruit_pos.y, r1):
            # print("Colisão da fruta detectada!")
            colison_fruit = True

            fruit_pos_x, fruit_pos_y = random_pos()
            fruit_pos = pygame.Vector2(fruit_pos_x, fruit_pos_y)

            enemy_pos_x, enemy_pos_y = random_pos()
            enemies.append([enemy_pos_x, enemy_pos_y])
            score+=1
            special_cont+=1

        else:
            colison_fruit = False

        if circles_collide(entity_pos.x, entity_pos.y, r1, player_pos.x, player_pos.y, r1) and is_live and not special:
            # print("Colisão da entidade detectada!")
            colison_entity = True
            life, last_hit_time, player_color= time_player_hit(current_time, life, last_hit_time, player_color)
        else:
            colison_entity = False

        #move the entity in the direction of the player
        if(is_live):
            move_towards(entity_pos, player_pos, speed)

        #draw the enemies
        for enemy in enemies:
            pygame.draw.circle(screen, "blue", enemy, r1)
            if circles_collide(enemy[0], enemy[1], r1, player_pos.x, player_pos.y, r1):
                if(special == False):
                    #print("Colisão com inimigo detectada!")
                    colison_enemy = True
                    life, last_hit_time, player_color = time_player_hit(current_time, life, last_hit_time, player_color)
                else:
                    del enemies[cont]
                    score+=1
                    print("especial ativado!")
            else:
                colison_enemy = False
            cont+=1
        cont=0

        if(special_cont == 3):
            special_cont = 0
            special = True
            special_current_time = pygame.time.get_ticks()

        player_color, special = special_mod(special, current_time, special_current_time, special_time, player_color)

        time = 5000 - (current_time - special_current_time)

        #refresh and config the text
        if(special):
            text_time_cont = f"Time: {time}"
            text_time_surface = font.render(text_time_cont, True, "white")
            text_time_rect = text_time_surface.get_rect(center=text_time_pos)

        text_score_cont = f"score: {score}"
        text_score_surface = font.render(text_score_cont, True, "white")
        text_score_rect = text_score_surface.get_rect(center=text_score_pos)

        text_life_cont = f"life: {life}"
        text_life_surface = font.render(text_life_cont, True, "white")
        text_life_rect = text_life_surface.get_rect(center=text_life_pos)

        #write the text
        screen.blit(text_score_surface, text_score_rect)
        screen.blit(text_life_surface, text_life_rect)
        
        #check the special
        if(special):
            screen.blit(text_time_surface, text_time_rect)

        #check the life of player
        if(life <= 0):
            if is_live:  
                dead_current_time = current_time  
                is_live = False

            #write the game over
            time_value = 5000 - (current_time - dead_current_time)
            font1 = pygame.font.SysFont(None, 100)
            text_game_over_surface = font1.render(text_game_over, True, "white")
            text_game_over_rect = text_game_over_surface.get_rect(center=text_game_over_pos)

            text_time_game_over = f"{int((time_value/1000))}" #convert to number

            text_time_game_over_surface = font1.render(text_time_game_over, True, "white")
            text_time_game_over_rect = text_time_game_over_surface.get_rect(center=text_time_game_over_pos)

            #change the text
            screen.blit(text_game_over_surface, text_game_over_rect)
            screen.blit(text_time_game_over_surface, text_time_game_over_rect)

            if time_value <= 0:
                life = 3
                is_live = True
                entity_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                player_color = "red"
                
            
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
