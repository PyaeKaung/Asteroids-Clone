import pygame as pg
import math
import random
import buttonclass
import stars
from particles import Particle
import rocks
import fire

pg.init()
pg.mixer.init()

font = pg.font.Font(None, 36)

WIDTH = 1400
HEIGHT = 720
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASTEROIDS")
icon = pg.image.load('images/asteroidicon.png')
pg.display.set_icon(icon)

black = (0, 0, 0)

world_radius = 6000

particles = []

#Loading audio CREDITS TO CREATOR
flightnoise = pg.mixer.Sound('audio/flightsound.mp3')
bullet_sound = pg.mixer.Sound('audio/firesound.mp3')
bullet_sound.set_volume(0.7)

#Loading images and sprites
startbutimg = pg.transform.scale(pg.image.load('images/startbutton.png'), (120, 60)).convert_alpha()
hangerbutimg = pg.transform.scale(pg.image.load('images/hangerbutton.png'), (120, 60)).convert_alpha()
optionsbutimg = pg.transform.scale(pg.image.load('images/optionsbutton.png'), (120, 60)).convert_alpha()
quitbutimg = pg.transform.scale(pg.image.load('images/quitbutton.png'), (120, 60)).convert_alpha()
mmbutimg = pg.transform.scale(pg.image.load('images/mainmenubutton.png'), (120, 60)).convert_alpha()
background = pg.transform.scale(pg.image.load('images/background.jpg'), (WIDTH,HEIGHT)).convert_alpha()

bodysprite = pg.transform.scale(pg.image.load('images/shipbody.png'), (100, 100)).convert_alpha()
wingsprite = pg.transform.scale(pg.image.load('images/shipwings.png'), (75,225)).convert_alpha()
gunsprite = pg.transform.scale(pg.image.load('images/shipgun.png'),(100, 300)).convert_alpha()

sprwidth = 200
sprheight = 600
playerch = pg.Surface((sprwidth, sprheight), pg.SRCALPHA)
playerch.blit(bodysprite, (100,250))
playerch.blit(wingsprite, (100,187))
playerch.blit(gunsprite, (100,150))
playerch = pg.transform.scale(playerch, (100,300))

import player
player.player_first_instance = playerch
asteroid_list = rocks.generate_asteroids(100, (world_radius, world_radius), world_radius)

#Button instances
startbutton = buttonclass.Button(100, 50, startbutimg, 2)
hangerbutton = buttonclass.Button(100, 200, hangerbutimg, 2)
optionsbutton = buttonclass.Button(100, 350, optionsbutimg, 2)
quitbutton = buttonclass.Button(100, 500, quitbutimg, 2)
mainmenubutton = buttonclass.Button(1250, 25, mmbutimg, 1)

is_moving = False
game_started = False

bullets = []

#Game loop
run = True
while run:
    camx = player.player_pos[0] - WIDTH // 2                
    camy = player.player_pos[1] - HEIGHT // 2
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if game_started and not fire.reloading:
                currenttime = pg.time.get_ticks()
                if currenttime - fire.lastshottime >= fire.fire_cooldown:
                    mousepos = pg.mouse.get_pos()
                    world_mouse_pos = pg.Vector2(mousepos[0] + camx, mousepos[1] + camy)
                    bullets.append(fire.Bullet(player.player_pos, world_mouse_pos))
                    fire.lastshottime = currenttime
                    fire.shotsfired += 1
                    bullet_sound.play()
                    if fire.shotsfired >= fire.maxshots:
                        fire.reloading = True
                        fire.reloadstarttime = currenttime


    if not game_started:
        screen.fill(black)
        screen.blit(pg.transform.scale(pg.transform.rotate(playerch, 90), (2000, 665)).convert_alpha(),(-50, 150))
        if hangerbutton.draw(screen):
            inprogresstext = font.render("In Progress", True, (255, 0, 0))
            screen.blit(inprogresstext, (WIDTH // 2 - inprogresstext.get_width() // 2, HEIGHT - 50))
        if optionsbutton.draw(screen):
            inprogresstext = font.render("In Progress", True, (255, 0, 0))
            screen.blit(inprogresstext, (WIDTH // 2 - inprogresstext.get_width() // 2, HEIGHT - 50))
        if startbutton.draw(screen):
            game_started = True
        if quitbutton.draw(screen):
            pg.quit()
            run = False
    else:
        screen.fill(black)
        pg.draw.circle(screen, (255, 255, 255), (world_radius - player.player_pos.x + WIDTH//2, world_radius - player.player_pos.y + HEIGHT//2), 6100)
        pg.draw.circle(screen, (0, 0, 0), (world_radius - player.player_pos.x + WIDTH//2, world_radius - player.player_pos.y + HEIGHT//2), world_radius)
        for pos in stars.spawn_points:
            screen.blit(stars.star, (pos.x - camx, pos.y - camy))


        rotated_player = pg.transform.rotate(player.player_first_instance, -player.player_angle)
        rotated_hitbox = rotated_player.get_rect(center=player.player_pos)

        for asteroid in asteroid_list:
            asteroid.update((world_radius, world_radius), world_radius)
            asteroid.draw(screen, camx, camy)

            if asteroid.collision(rotated_hitbox):
                print("Collision imbound!")

        #Rotation
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            player.player_angle -= player.player_rotation_speed
        if keys[pg.K_d]:
            player.player_angle += player.player_rotation_speed
        rad = math.radians(player.player_angle)
        direction = pg.Vector2(math.cos(rad), math.sin(rad))



        #Movement and drift logic
        if keys[pg.K_w]:
            player.player_pos += direction * player.player_speed
            if player.player_speed < player.forward_player_max_speed:
                player.player_speed += player.player_speed_increase

        if keys[pg.K_s]:
            player.player_pos += direction * player.player_speed
            if player.player_speed > player.backward_player_max_speed:
                player.player_speed -= player.player_speed_increase

        if not keys[pg.K_w] and not keys [pg.K_s]:
            if player.player_speed > 0:
                player.player_speed = max(player.player_speed - player.player_speed_decrease, 0)
            elif player.player_speed < 0:
                player.player_speed = min(player.player_speed + player.player_speed_decrease, 0)
            player.player_pos += direction * player.player_speed

        #World border
        distance_from_center = player.player_pos.distance_to(pg.Vector2(world_radius, world_radius))
        if distance_from_center > world_radius:
            direction_to_center = (pg.Vector2(world_radius, world_radius) - player.player_pos).normalize()
            player.player_pos = pg.Vector2(world_radius, world_radius) + direction_to_center * world_radius

        if keys[pg.K_a] or keys[pg.K_d] or keys[pg.K_w] or keys[pg.K_s]:
            is_moving = True
        else:
            is_moving = False

        #Particles
        if is_moving:
            particles.append(Particle(tuple(player.player_pos)))
            if not pg.mixer.get_busy():
                flightnoise.play(-1)
        else:
            flightnoise.stop()

        for particle in particles[:]:
            particle.update()
            particle.draw(screen, camx, camy)
            if particle.life <= 0:
                particles.remove(particle)

        if fire.reloading:
            currenttime = pg.time.get_ticks()
            if currenttime - fire.reloadstarttime >= fire.reloadduration:
                fire.reloading = False
                fire.shotsfired = 0
            else:
                if(currenttime // 500) % 2 == 0:
                    reload_text = font.render("Reloading", True, (255, 0, 0))
                    screen.blit(reload_text, (WIDTH // 2 - reload_text.get_width() // 2, HEIGHT - 50))
        
        for bullet in bullets[:]:
            bullet.update()
            if pg.time.get_ticks() - bullet.spawntime > bullet.life:
                bullets.remove(bullet)
                continue
            bullet_rect = pg.Rect(bullet.pos.x - bullet.radius, bullet.pos.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
            hit = False
            for asteroid in asteroid_list:
                if asteroid.rect.colliderect(bullet_rect):
                    asteroid.hp -= 5
                    hit = True
                    if asteroid.hp <= 0:
                        asteroid_list.remove(asteroid)
                        asteroid_list.append(rocks.Asteroid((world_radius,world_radius), world_radius))
                    break
            if hit:
                bullets.remove(bullet)
            else:
                bullet.draw(screen, camx, camy)

        if mainmenubutton.draw(screen):
            game_started = False
            player.player_pos = pg.Vector2(world_radius // 2, world_radius // 2)
            player.player_speed = 0
            particles.clear()
            flightnoise.stop()
        screen.blit(rotated_player, (WIDTH//2 - rotated_hitbox.width//2, HEIGHT//2 - rotated_hitbox.height//2))

    pg.display.update()
    clock.tick(100)
pg.quit()
