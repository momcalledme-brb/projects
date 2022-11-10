import pygame, sys, os, random, math, time

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('arkanoid')
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE) # start window


font = pygame.font.Font('slkscr.ttf', 15)




paddx = 290 #paddle initail position
paddy = 340

paddle = pygame.Rect(paddx, paddy, 40, 5) #paddle object


blocks = [] #blocks to hit

limittop = pygame.Rect(0, 0, 600, 10) #create limites
limitbot = pygame.Rect(0, 390, 600, 10)
limitright = pygame.Rect(590, 0, 10 , 600)
limitleft = pygame.Rect(0, 0, 10 , 600)


ball = pygame.Rect(300, 300, 5 , 5) #ball object


def ball_set(): #function to set ball
    ball = pygame.Rect(300, 300, 5 , 5)
    pygame.draw.rect(screen, (255,255,255), ball) #draw the ball
    v = [2,3,4,5,6,7,8] #list of speeds
    s = [1, -1] #ball direction
    
    ball_xv = random.choice(s)*random.choice(v) #x speed
    ball_yv = -(random.choice(v)) #y speed
    return ball_xv, ball_yv #return speeds

ball_xv, ball_yv = ball_set()

ball_pre_x, ball_pre_y = ball.x, ball.y


walls = []

def create_blocks(blocks, walls):
    x_dis = 75
    a = x_dis 
    b = 0 
    for x in range(0, 7): #amount rows of blocks 
        for y in range(0, 10): #amount columns of blocks
            block = pygame.Rect(a, 25 + b , 30, 15) #create block
            walls.append([[(block.x,  block.y),(block.x, block.y + block.h), 'x'],
                          [(block.x,  block.y), (block.x + block.w, block.y), 'y'],
                          [(block.x + block.w,  block.y), (block.x + block.w, block.y + block.h), 'x'],
                          [(block.x,  block.y + block.h), (block.x + block.w, block.y + block.h), 'y']])
            blocks.append(block)
            a = a + 45
        b = b + 30
        a = x_dis

#each wall appended in the list has 4 lines. the order is left line, top line, right line and the bottom line
#these lines are the walls that each brick will have. each line has an x or a y in it. these will later tell in which direction the ball will bounce.

create_blocks(blocks, walls)



points = []

dis = []

point = None


def colli(padxs, padys, padxf, padyf, ballx, bally, ballpx, ballpy): #check if the raycast is colliding with a line
    
    x1 = padxs
    y1 = padys
    x2 = padxf
    y2 = padyf

    x3 = ballx
    y3 = bally
    x4 = ballpx
    y4 = ballpy

    den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if den == 0:
        return False

    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
    u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den

    if ((t <= 1 and t >= 0) and (u > 0)):
        x = padxs + t*(padxf - padxs)
        y = padys + t*(padyf - padys)
        return x, y
    else:
        return False

hits_something = False    

def colli_paddle(padxs, padys, padxf, padyf, ballx, bally, ballpx, ballpy):
    
    x1 = padxs
    y1 = padys
    x2 = padxf
    y2 = padyf

    x3 = ballx
    y3 = bally
    x4 = ballpx
    y4 = ballpy

    den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if den == 0:
        return False

    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
    u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den

    if ((t <= 1 and t >= 0) and (u >= 0 and u <= 1)): 
        x = padxs + t*(padxf - padxs)
        y = padys + t*(padyf - padys)
        return x, y
    else:
        return False


last = [False, False, False, False] #previous state of collisions. starts as false.

    
last_time = time.time()



def raycast_line(): #returns the closest collision line
    points = [] #points of collision
    dis = [] # distance
    bounce = []
    bricks = []

    for wall in walls: #get each wall
        for limit in wall: #get each limit in the walls
        #check the collision between each wall and an elongated line coming from the center of the ball.
            col = colli(limit[0][0], limit[0][1], limit[1][0], limit[1][1] , ball_pre_x + 2.5 , ball_pre_y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)
            if col!= False:
                points.append(col) #if colli is not false, meaning that it saw a point, add the point to the list of points
                bounce.append(limit[2]) #will give the x or the y for the bounce
                bricks.append(wall) #gives the entire brick, with all of their walls.
    if len(points) > 1:
        #if there's more that one point detected
        for i in range(len(points)):
            #add the distance of each point and the posicion on the ball.
            dis.append(math.sqrt((ball_pre_x-points[i][0])**2 + (ball_pre_y-points[i][1])**2))
                
        #return the point with the shortest distance.
        #each distance has the same index as each point
        #the +2 and the -2 creates a short line to check for the crossing of short line that the ball has.
        a = ((points[dis.index(min(dis))][0] + 2, points[dis.index(min(dis))][1]), (points[dis.index(min(dis))][0] - 2, points[dis.index(min(dis))][1]))
        #pygame.draw.circle(screen, (255,255,255), (points[dis.index(min(dis))][0], points[dis.index(min(dis))][1]), 5)
        #print(len(points))
        #print(bricks[dis.index(min(dis))])
        return a, bounce[dis.index(min(dis))], bricks[dis.index(min(dis))]

sfx = pygame.mixer.Sound('sfx.wav') # sound of collisions

score = 0

while True: #game loop

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    screen.fill((0,0,0))
    textSurfaceObj = font.render('score: ' + str(score), True, (255,255,255), (0,0,0)) #puntaje en pantalla
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (55, 380)

    screen.blit(textSurfaceObj, textRectObj)
    
    #pygame.draw.rect(screen, (255,255,255), block)

    pygame.draw.rect(screen, (255,255,255), limittop) # draw limits
    pygame.draw.rect(screen, (255,255,255), limitbot)
    pygame.draw.rect(screen, (255,255,255), limitright)
    pygame.draw.rect(screen, (255,255,255), limitleft)
    
    



    #ball position now
    
    ball.x = ball.x + ball_xv

    ball.y = ball.y + ball_yv

    
    #paddle
    
    pygame.draw.polygon(screen, (255,255,255), [(paddle.x + 5, paddle.y), (paddle.x + 35, paddle.y), (paddle.x + 40, paddle.y + 5), (paddle.x, paddle.y + 5)])


    #paddle collision with limits and movement
        
    x, y = pygame.mouse.get_pos()

    paddle.x = x - 20



    hipo = math.sqrt((ball_pre_x-ball.x)**2 + (ball_pre_y-ball.y)**2)

    #raycasting
    if ball_xv < 0 and ball_yv > 0: 
        rad = math.asin((ball_pre_y-ball.y)/(hipo))
        degrees = 180 - rad*(180/math.pi)
    elif ball_xv < 0 and ball_yv < 0: 
        rad = math.asin((ball_pre_y-ball.y)/(hipo))
        degrees = 180 - rad*(180/math.pi) 
    elif ball_xv > 0 and ball_yv < 0: 
        rad = math.asin((ball_pre_y-ball.y)/(hipo))
        degrees = rad*(180/math.pi) 
    elif ball_xv > 0 and ball_yv > 0:
        rad = math.asin((ball_pre_y-ball.y)/(hipo))
        degrees = rad*(180/math.pi) + 360

    xtrig = math.cos(degrees*(math.pi/180))*15
    ytrig = math.sin(degrees*(math.pi/180))*15

    #pygame.draw.line(screen, (255, 255, 255),(ball.x + 2.5, ball.y + 2.5), (ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig), width = 1)

    # draw ball trayectory
    
    #pygame.draw.line(screen, (255,0,0), (ball.x + 2.5, ball.y + 2.5), (ball.x + 2.5 + xtrig, ball.y + 2.5 - ytrig) , width = 1 )

    pygame.draw.rect(screen, (255,255,255), ball) # draw ball object


    
    ##limit collisions
    if ball.colliderect(limittop):
        ball_yv = -(ball_yv)
        sfx.play()
    if ball.colliderect(limitright) or ball.colliderect(limitleft):
        ball_xv = -(ball_xv)
        sfx.play()
    if ball.colliderect(limitbot):
        ball_xv, ball_yv = ball_set()
        ball = pygame.Rect(300, 300, 5 , 5) #ball object
        score -= 5

    
    


    
    ##--------collision with line intersection
    
    ## -------line on top of the rectangle
    
    #pygame.draw.rect(screen, (255,0,0), (paddle.x, paddle.y), (paddle.x + 40, paddle.y), width = 1 )
    
    
    
    ## ----------line intersection

    ##-----------function does here def colli(padxs, padys, padxf, padyf, ballx, bally, ballpx, ballpy):


    coll_balltop = colli(0, 0, 600, 0 , ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig) #start up collision detection
    
    coll_ballleft = colli(0, 0, 0, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)

    coll_ballright = colli(600, 0, 600, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)

    coll_balldown = colli(0, 400, 600, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)


    current = [coll_balltop, coll_ballleft, coll_ballright, coll_balldown] #start up logic condition

    for ele in current:
        if ele != False: #will give points, not a boolean
            current[current.index(ele)] = True #this part will force the boolean to a true.
            

    #current = [False, False, False, False]
    

    if last != current or hits_something == True: #sees a different border or has hit a brick
        #the below code will only run if the ball is seeing a new wall or if it has hit a brick with the hits_somthing variable.
        #print('seeing a different wall')
        
        

        coll_balltop = colli(0, 0, 600, 0 , ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)
    
        coll_ballleft = colli(0, 0, 0, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)

        coll_ballright = colli(600, 0, 600, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)

        coll_balldown = colli(0, 400, 600, 400, ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)

        current = [coll_balltop, coll_ballleft, coll_ballright, coll_balldown] # collision logic
        #set the current new collision logic
        for ele in current:
            if ele != False:
                current[current.index(ele)] = True

        #print('current', current)
        #print('last', last)
        last = current
        if raycast_line() != None: #if true, the ball is seeing a brick
            point, bounce, brick = raycast_line()
        #print(bricks)

        
    if point is not None and bounce is not None:
        #reminder: point is refering to the +2 -2 line created in the function raycast_line()
        colli_point_or_logic = colli(point[0][0], point[0][1], point[1][0], point[1][1], ball.x + 2.5 + xtrig, ball.y + 2.5 - ytrig, ball_pre_x + 2.5, ball_pre_y + 2.5)
        #colli_point_or_logic = colli(point[0][0], point[0][1], point[1][0], point[1][1], ball.x + 2.5, ball.y + 2.5, ball.x + 2.5 + xtrig/5, ball.y + 2.5 - ytrig/5)
        
        if colli_point_or_logic != False: #if the function doesn't give false, it means that it hit somthing and it give an x and y coor
            if bounce == 'x':
                ball_xv = ball_xv*-1
            elif bounce == 'y':
                ball_yv = ball_yv*-1
            point = None
            bounce = None
            blocks.pop(walls.index(brick))
            walls.remove(brick)
            hits_something = True
            score += 5
            sfx.play()
    else:
        hits_something = False

    if (colli_paddle(paddle.x + 5, paddle.y, paddle.x + 35, paddle.y , ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)) != False:

        ball_yv = -(ball_yv)
        sfx.play()

    
   
    # left part of the paddle
    elif (colli_paddle(paddle.x, paddle.y + 5, paddle.x + 5, paddle.y , ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)) != False:

        if ball_xv > 0:
        
            ball_xv = -(ball_xv)
            ball_yv = -(ball_yv)
            sfx.play()

    elif (colli_paddle(paddle.x + 40, paddle.y + 5, paddle.x + 35, paddle.y , ball.x + 2.5 , ball.y + 2.5 , ball.x + 2.5 + xtrig , ball.y + 2.5 - ytrig)) != False:

        if ball_xv < 0:
            ball_xv = -(ball_xv)
            ball_yv = -(ball_yv)
            sfx.play()


            
    for block in blocks:
        pygame.draw.rect(screen, (255,255,255), block)
    if len(blocks) == 0:
        if ball.y > 300:
            create_blocks(blocks, walls)
            
            
        

                

    last = current #changes the collision logic
                
    
    
    #walls = [[(block.x,  block.y),(block.x, block.y + 100), 'x'], [(block.x,  block.y), (block.x + 100, block.y), 'y'], [(block.x + 100,  block.y), (block.x + 100, block.y + 100), 'x'], [(block.x,  block.y), (block.x + 100, block.y), 'y']]

    """
    pygame.draw.line(screen, (255,0,0), (walls[0][0][0],  walls[0][0][1]), (walls[0][1][0], walls[0][1][1]) , width = 1 )
    pygame.draw.line(screen, (255,0,0), (walls[1][0][0],  walls[1][0][1]), (walls[1][1][0], walls[1][1][1]) , width = 1 )
    pygame.draw.line(screen, (255,0,0), (walls[2][0][0],  walls[2][0][1]), (walls[2][1][0], walls[2][1][1]) , width = 1 )
    pygame.draw.line(screen, (255,0,0), (walls[3][0][0],  walls[3][0][1]), (walls[3][1][0], walls[3][1][1]) , width = 1 )
    """
    
    ball_pre_x, ball_pre_y = ball.x, ball.y
    
        
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        
                
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            

                

    
            
    pygame.display.update()
    clock.tick(60)
