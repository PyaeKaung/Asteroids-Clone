import pygame as pg
import math
import random
import buttonclass
import player
import stars
from particles import Particle
from explosionparticles import ExplosionParticle as exp
import rocks
import fire
import healthbar
from enemy import Enemy

pg.init()
pg.mixer.init()

font = pg.font.Font(None, 36)
inprogresstext = font.render("In Progress", True, (255, 0, 0))
starttimer = None
gameovertimer = None

black = (0, 0, 0)
world_radius = 6000
time = 2000
volume_value = 0.7
WIDTH = 1400
HEIGHT = 720
score = 0

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASTEROIDS")
icon = pg.image.load('images/asteroidicon.png')
pg.display.set_icon(icon)

#Loading audio CREDITS TO CREATOR
flightnoise = pg.mixer.Sound('audio/flightsound.mp3')
flightnoise.set_volume(1)
bulletsound = pg.mixer.Sound('audio/firesound.mp3')
bulletsound.set_volume(1)
explosionsound = pg.mixer.Sound('audio/explosionsound.wav')
explosionsound.set_volume(1)
enemyfiresound = pg.mixer.Sound('audio/enemyfire.wav')
enemyfiresound.set_volume(1)

#Channels
flightchannel = pg.mixer.Channel(1)
playergunchannel = pg.mixer.Channel(2)
enemygunchannel = pg.mixer.Channel(3)

#Loading images and sprites
startbutimg = pg.transform.scale(pg.image.load('images/startbutton.png'), (120, 60)).convert_alpha()
hangerbutimg = pg.transform.scale(pg.image.load('images/hangerbutton.png'), (120, 60)).convert_alpha()
optionsbutimg = pg.transform.scale(pg.image.load('images/optionsbutton.png'), (120, 60)).convert_alpha()
quitbutimg = pg.transform.scale(pg.image.load('images/quitbutton.png'), (120, 60)).convert_alpha()
mmbutimg = pg.transform.scale(pg.image.load('images/mainmenubutton.png'), (120, 60)).convert_alpha()
enemy_image = pg.transform.scale(pg.image.load('images/enemy.png'), (70, 30)).convert_alpha()
playerch = pg.image.load('images/shipsprite.png')
playerch = pg.transform.scale(playerch, (120, 84))
star = pg.transform.scale(pg.image.load('images/star.png'), (30, 30))

player.player_first_instance = playerch
asteroid_list = rocks.generate_asteroids(100, (world_radius, world_radius), world_radius)

#Button instances
startbutton = buttonclass.Button(100, 50, startbutimg, 2)
hangerbutton = buttonclass.Button(100, 200, hangerbutimg, 2)
optionsbutton = buttonclass.Button(100, 350, optionsbutimg, 2)
quitbutton = buttonclass.Button(100, 500, quitbutimg, 2)
mainmenubutton = buttonclass.Button(1250, 25, mmbutimg, 1)

#State variables
is_moving = False
game_started = False
game_over = False
options_screen = False 
hit = False
explosion = False
enemyhit = None

bullets = []
particles = []
explosionparticlelist = []
enemies = []
enemy_bullets = []

#Game loop
run = True
while run:
    camx = player.player_pos[0] - WIDTH // 2                
    camy = player.player_pos[1] - HEIGHT // 2

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if game_started and not fire.reloading and not game_over and not options_screen:
                currenttime = pg.time.get_ticks()
                if currenttime - fire.lastshottime >= fire.fire_cooldown:
                    mousepos = pg.mouse.get_pos()
                    world_mouse_pos = pg.Vector2(mousepos[0] + camx, mousepos[1] + camy)
                    bullets.append(fire.Bullet(player.player_pos, world_mouse_pos))
                    fire.lastshottime = currenttime
                    fire.shotsfired += 1
                    playergunchannel.play(bulletsound)
                    if fire.shotsfired >= fire.maxshots:
                        fire.reloading = True
                        fire.reloadstarttime = currenttime

    #Option screen
    if options_screen:
        screen.fill(black)
        vol_text = font.render('VOLUME', True, (255, 255, 255))
        screen.blit(vol_text, (WIDTH // 2 - vol_text.get_width() // 2, 100))
        bar_width = 400
        bar_height = 10
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT // 2
        pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
        circle_radius = 15
        circle_x = bar_x + int(volume_value * bar_width)
        circle_y = bar_y + bar_height // 2
        pg.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), circle_radius)
        mouse_pressed = pg.mouse.get_pressed()[0]
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_pressed:
            if (bar_x - circle_radius) <= mouse_x <= (bar_x + bar_width + circle_radius) and (bar_y - circle_radius) <= mouse_y <= (bar_y + bar_height + circle_radius):
                new_volume = (mouse_x - bar_x) / bar_width
                new_volume = max(0, min(new_volume, 1))
                volume_value = new_volume
                flightnoise.set_volume(volume_value)
                bulletsound.set_volume(volume_value)
                explosionsound.set_volume(volume_value)
                enemyfiresound.set_volume(volume_value)
        if mainmenubutton.draw(screen):
            options_screen = False

    #Main menu
    elif not game_started:
        screen.fill(black)
        screen.blit(pg.transform.scale(pg.transform.rotate(playerch, 90), (420, 600)).convert_alpha(), (720, 150))
        if hangerbutton.draw(screen):
            starttimer = pg.time.get_ticks()

        if starttimer is not None:
            if pg.time.get_ticks() - starttimer < time:
                screen.blit(inprogresstext, (WIDTH // 2 - inprogresstext.get_width() // 2, HEIGHT - 50))
            else:
                starttimer = None

        if optionsbutton.draw(screen):
            starttimer = pg.time.get_ticks()
            options_screen = True

        if starttimer is not None:
            if pg.time.get_ticks() - starttimer < time:
                screen.blit(inprogresstext, (WIDTH // 2 - inprogresstext.get_width() // 2, HEIGHT - 50))
            else:
                starttimer = None

        if startbutton.draw(screen):
            game_started = True
        if quitbutton.draw(screen):
            pg.quit()
            run = False

    #Gameplay
    else:
        if not game_over:
            screen.fill(black)
            pg.draw.circle(screen, (255, 255, 255), (world_radius - player.player_pos.x + WIDTH//2, world_radius - player.player_pos.y + HEIGHT//2), 6100)
            pg.draw.circle(screen, (0, 0, 0), (world_radius - player.player_pos.x + WIDTH//2, world_radius - player.player_pos.y + HEIGHT//2), world_radius)
            if len(enemies) < 7:
                enemies.append(Enemy(player, enemy_bullets, enemy_image, enemyfiresound))
            for pos in stars.spawn_points:
                screen.blit(star, (pos.x - camx, pos.y - camy))
            for enemy in enemies:
                enemy.update()
                enemy.draw(screen, camx, camy)

            rotated_player = pg.transform.rotate(player.player_first_instance, -player.player_angle)
            rotated_hitbox = rotated_player.get_rect(center=player.player_pos)

            for asteroid in asteroid_list:
                asteroid.update((world_radius, world_radius), world_radius)
                asteroid.draw(screen, camx, camy)
                if asteroid.collision(rotated_hitbox):
                    player.player_health -= 25
                    asteroid_list.remove(asteroid)
                    asteroid_list.append(rocks.Asteroid((world_radius, world_radius), world_radius))

            for b in enemy_bullets[:]:
                if b.collision(rotated_hitbox):
                    player.player_health -= 5
                    enemy_bullets.remove(b)                
                if not b.update():
                    enemy_bullets.remove(b)
                else:
                    b.draw(screen, camx, camy)

            #Rotation and movement
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                player.player_angle -= player.player_rotation_speed
            if keys[pg.K_d]:
                player.player_angle += player.player_rotation_speed
            rad = math.radians(player.player_angle)
            direction = pg.Vector2(math.cos(rad), math.sin(rad))
            if keys[pg.K_w]:
                player.player_pos += direction * player.player_speed
                if player.player_speed < player.forward_player_max_speed:
                    player.player_speed += player.player_speed_increase
            if keys[pg.K_s]:
                player.player_pos += direction * player.player_speed
                if player.player_speed > player.backward_player_max_speed:
                    player.player_speed -= player.player_speed_increase
            if not keys[pg.K_w] and not keys[pg.K_s]:
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

            if is_moving:
                particles.append(Particle(tuple(player.player_pos)))
                if not flightchannel.get_busy():
                    flightchannel.play(flightnoise, loops=-1)
            else:
                flightchannel.stop()

            #Particles
            for particle in particles[:]:
                particle.update()
                particle.draw(screen, camx, camy)
                if particle.life <= 0:
                    particles.remove(particle)

            #Gun
            if fire.reloading:
                currenttime = pg.time.get_ticks()
                if currenttime - fire.reloadstarttime >= fire.reloadduration:
                    fire.reloading = False
                    fire.shotsfired = 0
                else:
                    if (currenttime // 500) % 2 == 0:
                        reload_text = font.render("Reloading", True, (255, 0, 0))
                        screen.blit(reload_text, (WIDTH // 2 - reload_text.get_width() // 2, HEIGHT - 50))
            
            for bullet in bullets[:]:
                bullet.update()
                if pg.time.get_ticks() - bullet.spawntime > bullet.life:
                    bullets.remove(bullet)
                    continue

                hit = False

                bullet_rect = pg.Rect(bullet.pos.x - camx - bullet.radius, bullet.pos.y - camy - bullet.radius, bullet.radius * 2, bullet.radius * 2)

                for enemy in enemies[:]:
                    enemy_rect = enemy.get_rect(camx, camy)
                    if enemy_rect.colliderect(bullet_rect):
                        score += 1
                        enemies.remove(enemy)
                        if bullet in bullets:
                            bullets.remove(bullet)
                        for _ in range(50):
                            explosionparticlelist.append(exp(enemy.pos))
                        break
                if bullet in bullets:
                    bullet.draw(screen, camx, camy)


                for asteroid in asteroid_list:
                    if asteroid.rect.colliderect(bullet_rect):
                        asteroid.hp -= 5
                        hit = True
                        if asteroid.hp <= 0:
                            asteroid_list.remove(asteroid)
                            asteroid_list.append(rocks.Asteroid((world_radius, world_radius), world_radius))
                        break
                if hit:
                    bullets.remove(bullet)
                else:
                    bullet.draw(screen, camx, camy)
            
            #Explosion for enemies
            for particle in explosionparticlelist[:]:
                particle.update()
                particle.draw(screen, camx, camy)
                if particle.life <= 0:
                    explosionparticlelist.remove(particle)

            #Healthbar
            healthbar.draw_health_bar(screen, WIDTH - 50, HEIGHT // 4, player.player_health, player.max_health)

            if mainmenubutton.draw(screen):
                game_started = False
                player.player_pos = pg.Vector2(world_radius // 2, world_radius // 2)
                player.player_speed = 0
                player.player_health = 200
                particles.clear()
                explosionparticlelist.clear()
                flightnoise.stop()

            if player.player_health <= 0 and not game_over:
                game_over = True
                gameovertimer = pg.time.get_ticks()
                explosion = False

            screen.blit(rotated_player, (WIDTH // 2 - rotated_hitbox.width // 2, HEIGHT // 2 - rotated_hitbox.height // 2))
            scoredisplay = font.render(str(score), True, (255, 255, 255))
            screen.blit(scoredisplay, (1353, 140))
        else:
            enemyfiresound.stop()
            flightnoise.stop()

            #Gameover sequence
            if not explosion:
                explosionparticlelist = [exp(player.player_pos) for _ in range(100)]
                explosionsound.play()
                explosion = True

            for exparticle in explosionparticlelist[:]:
                exparticle.update()
                exparticle.draw(screen, camx, camy)
                if exparticle.life <= 0:
                    explosionparticlelist.remove(exparticle)
            if pg.time.get_ticks() - gameovertimer > 2000:
                game_over = False
                game_started = False
                player.player_pos = pg.Vector2(world_radius // 2, world_radius // 2)
                player.player_speed = 0
                player.player_health = 200
                score = 0
                particles.clear()
                explosionparticlelist.clear()
                flightnoise.stop()            
    pg.display.update()
    clock.tick(100)
pg.quit()
