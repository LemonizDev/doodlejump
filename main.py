from abc import abstractstaticmethod
from turtle import speed
import webbrowser
import pygame
import random
pygame.init()

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gray = (128,128,128)
background = pygame.image.load('background.png')

# help valriables
new = 2
url = 'https://github.com/lemonizdev/doodlejump'
#screen constants
width = 500
height = 600
background = pygame.transform.scale(background, (width, height))
player = pygame.transform.scale(pygame.image.load('player.png'), (100,82)) 
block = pygame.transform.scale(pygame.image.load('platform.png'), (100, 30))
white_block = pygame.transform.scale(pygame.image.load('white-platform.png'), (100, 30))
comp_spring = pygame.image.load('spring_comp.png')
spring = pygame.image.load('spring.png')
brokenp = pygame.image.load('broken_platforms.png')
brokenp1 = pygame.image.load('broken_platforms1.png')
icon = pygame.image.load('icon.jpg')
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

#game variables
player_x = 270
player_y = 450
platforms = [[260, 550], [160, 430], [160, 166], [30, 298], [280, 46]]
white_platforms = [[280, 298]]
broken_platforms = [[random.randint(10, width - 100), random.randint(-300, -200)]] 
used_brown = []
springs = []
used_springs = []
jump = False
y_change = 0
x_change = 0
speed = 8
score = 0
high_score = 0
game_over = False
powerup = 2
previous_score = 0
jump_height = 10
gravity = .45

#screen 
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Doodle Jump')
pygame.display.set_icon(icon)


running = True
pause = False

#generating springed platforms
def generate_springs():
    global comp_spring
    global spring
    global platforms
    probabilities = [True, False, False, False] #25% probability for true
    choice = random.choice(probabilities)
    if choice:
        if len(springs) != 1:
            n = random.choice(platforms)
            while n[1] > 0:
                n = random.choice(platforms)
            springs.append([n[0] + 6, n[1] - 34])


#function to update the player's y position every loop
def update_player(y_pos):
    global jump
    global jump_height
    global y_change
    global gravity
    jump_height = 10
    if jump:
        if y_change == -20:
            pass
        else:
            y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    gravity = 0.45
    return y_pos

#function to break brown platforms on collision
def break_platform(list):
    global broken_platforms
    global used_brown
    global y_change
    global gravity
    x = list[0]
    y = int(list[1])
    used_brown.append([x, y])
    broken_platforms.remove(list)
    broken_platforms.append([random.randint(10, width - 100), random.randint(-300, 0)])
    
#game pause
def pause():
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        fent = pygame.font.SysFont('times new roman', 60)
        text = fent.render('Game Paused', True, black)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        ntext = fent.render('Press P to resume', True, black)
        ntextRect = ntext.get_rect()
        ntextRect.center = (width // 2, height // 2 + 50)
        screen.blit(text, textRect)
        screen.blit(ntext, ntextRect)
        pygame.display.update()
        timer.tick(15)




#function to check platform collisions
def check_collision(list, white_list, j, w_platforms):
    global player_y
    global player_x
    global y_change
    global screen
    global player
    global block
    global platforms
    global white_platforms
    global springs
    global springy
    global browns
    global broken_platforms
    global used_brown
    l= []
    wl = []
    spl = []
    bpl = []

    #generating a list of rectangles
    for i in range(len(list)):
        l.append(list[i].get_rect(topleft = (platforms[i][0], platforms[i][1])))
    for i in range(len(white_list)):
        wl.append(white_list[i].get_rect(topleft = (white_platforms[i][0], white_platforms[i][1])))
    for i in range(len(springs)):
        spl.append(springy[i].get_rect(topleft = (springs[i][0], springs[i][1])))
    for i in range(len(broken_platforms)):
        bpl.append(brokenp1.get_rect(topleft = (broken_platforms[i][0], broken_platforms[i][1])))


    #checking collisions 
    for i in range(len(l)):
        if l[i].colliderect([player_x+ 20, player_y, 35, 82]) and j == False and y_change > 0:
            j = True

    for i in range(len(wl)):
        if wl[i].colliderect([player_x+ 20, player_y, 35, 82]) and j == False and y_change > 0:
            j = True
            w_platforms.remove(w_platforms[i])
            w_platforms.append([random.randint(10, width - 100), random.randint(-700, 0)])
    
    for i in range(len(spl)):
        if spl[i].colliderect([player_x+ 20, player_y, 35, 82]) and j == False and y_change > 0:
            j = True
            y_change = -20
            x = int(springs[i][0])
            y = int(springs[i][1])
            springs.remove(springs[i])
            used_springs.append([x, y])
    for i in range(len(bpl)):
        if bpl[i].colliderect([player_x+ 20, player_y, 35, 82]) and j == False and y_change > 0:
            break_platform(broken_platforms[i])
    return j, w_platforms
        
# Function to move camera as the player progresses upwards
def update_platforms(array, white_array, y, delta_y):
    global gravity
    global score
    global springs
    global used_springs
    if y < height//2 and delta_y < 0:
        for i in range(len(array)):
            array[i][1] -= 0.5 * delta_y
        for i in range(len(white_array)):
            white_array[i][1] -= 0.5 * delta_y
        for i in range(len(springs)):
            springs[i][1] -= 0.5 * delta_y
        for i in range(len(used_springs)):
            used_springs[i][1] -= 0.5 * delta_y
        for i in range(len(broken_platforms)):
            broken_platforms[i][1] -= 0.5 * delta_y
        for i in range(len(used_brown)):
            used_brown[i][1] -= 0.5 * delta_y

    if y < 0 and delta_y < 0:
        gravity = 0.9
        for i in range(len(array)):
            array[i][1] -= 2 * delta_y
        for i in range(len(white_array)):
            white_array[i][1] -= 2 * delta_y
        for i in range(len(springs)):
            springs[i][1] -= 2 * delta_y
        for i in range(len(used_springs)):
            used_springs[i][1] -= 2 * delta_y
        for i in range(len(broken_platforms)):
            broken_platforms[i][1] -= 2 * delta_y
        for i in range(len(used_brown)):
            used_brown[i][1] -= 2 * delta_y
            
    else:
        pass;
    for element in array:
        if element[1] > height:
            array.remove(element)
            array.append([random.randint(10, width - 100), 0])
            generate_springs()
            score += 1
    for element in white_array:
        if element[1] > height:
            white_array.remove(element)
            white_array.append([random.randint(10, width - 100), random.randint(-700, -200)])
            score += 1
    for element in springs:
        if element[1] > height:
            springs.remove(element)
    for element in used_springs:
        if element[1] > height:
            used_springs.remove(element)
    for element in broken_platforms:
        if element[1] > height:
            broken_platforms.remove(element)
            broken_platforms.append([random.randint(10, width - 100), random.randint(-300, 0)])
    for element in used_brown:
        if element[1] > height:
            used_brown.remove(element)
    return array, white_array


#game loop
while running:
    screen.blit(background, (0,0))
    screen.blit(player, (player_x, player_y))
    timer.tick(fps)
    blocks = []
    white_blocks = []
    springy = []
    browns = [] #non racist comment
    score_render = font.render('Score: ' + str(score), True, black)
    screen.blit(score_render, (10, 10))


    if score > high_score:
        high_score = score
    high_score_render = font.render('High Score: ' + str(high_score), True, black)
    screen.blit(high_score_render, (10, 30))

    powerupsfont = font.render('Powerups: ' + str(powerup) + ' (Spacebar)', True, black)
    screen.blit(powerupsfont, (10, 50))

#generating blocks
    for i in range(len(platforms)):
        screen.blit(block, (platforms[i][0], platforms[i][1]))
        blocks.append(block)

    for i in range(len(white_platforms)):
        screen.blit(white_block, (white_platforms[i][0], white_platforms[i][1]))
        white_blocks.append(white_block)

    for i in range(len(springs)):
        screen.blit(comp_spring, (springs[i][0], springs[i][1]))
        springy.append(spring)

    for i in range(len(used_springs)):
        screen.blit(spring, (used_springs[i][0], used_springs[i][1]))
    
    for i in range(len(broken_platforms)):
        screen.blit(brokenp, (broken_platforms[i][0], broken_platforms[i][1]))
        browns.append(brokenp)
    
    for i in range(len(used_brown)):
        screen.blit(brokenp1, (used_brown[i][0], used_brown[i][1]))


#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #key handler
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and powerup > 0 and not game_over:
                powerup -= 1
                y_change = -15
            if((event.key == pygame.K_r) or (event.key == pygame.K_SPACE)) and game_over == True:
                game_over = False
                platforms = [[260, 550], [160, 430], [160, 166], [30, 298], [280, 46]]
                white_platforms = [[280, 298]]
                broken_platforms = [[random.randint(10, width - 100), random.randint(-300, -200)]]
                used_brown = []
                used_springs = []
                springs = []
                player_x = 270
                player_y = 450
                score = 0
            if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                x_change = -speed
            if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                x_change = speed 
            if(event.key == pygame.K_F1):
                webbrowser.open(url, new = new)
                if not game_over:
                    pause()
            if (event.key == pygame.K_p):
                pause()
            
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                x_change = 0
            if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                x_change = 0  
        
    
    player_x += x_change
    jump, white_platforms = check_collision(blocks, white_blocks, jump, white_platforms)
    platforms, white_platforms = update_platforms(platforms, white_platforms, player_y, y_change)

    if x_change > 0:
        player = pygame.transform.scale(pygame.image.load('player.png'), (100,82.55395683453238))
    elif x_change < 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('player.png'), (100,82.55395683453238)), 1,0)
    
    
    if player_x < 0:
        player_x = player_x + width
    elif player_x > width - 100:
        player_x = -(width - player_x)
    
    if player_y < 0:
        player_y = 0
    


    if player_y < 560:
        player_y = update_player(player_y)
    else:
        game_over = True
        finalscore = None
        if high_score == score:
            finalscore = 'New High Score! ' + str(high_score)
        else:
            finalscore = 'Score: ' + str(score)

        if score == 0:
            finalscore = 'Score: 0. L Bozo'
        fent = pygame.font.SysFont('times new roman', 60)
        fent2 = pygame.font.SysFont('times new roman', 30)


        gover = fent.render('YOU DIED', True, black)
        gover_rect = gover.get_rect(center=(width/2, height/2))

        scr = fent2.render(finalscore, True, black)
        scr_rect = scr.get_rect(center=(width/2, height/2 + 50))

        restartmsg = fent2.render('Press R to restart', True, black)
        restartmsg_rect = restartmsg.get_rect(center=(width/2, height/2 + 100))

        helpmsg = fent2.render('Press F1 for help', True, black)
        helpmsg_rect = helpmsg.get_rect(center=(width/2, height/2 + 150))

        screen.blit(restartmsg, restartmsg_rect)
        screen.blit(helpmsg, helpmsg_rect)
        screen.blit(scr, scr_rect)
        screen.blit(gover, gover_rect)
        y_change = 0
        x_change = 0
        previous_score = score
    
    #powerup generation
    if score % 100 == 0 and score != 0 and score != previous_score:
        powerup += 1
        previous_score = score
    
    
    pygame.display.flip()

pygame.quit()