import pygame, sys, os, random, math, time
import numpy as np

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

font = pygame.font.Font('slkscr.ttf', 20) #font

pygame.display.set_caption('sudoku')
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE) # start window

#borders

left = pygame.Rect(30, 20, 4, 360)

right = pygame.Rect(570, 20, 4, 360)

top = pygame.Rect(30, 20, 540, 4)

bottom = pygame.Rect(30, 380, 544, 4)

global squares

global squares_with_numbers

squares_with_numbers = {}



positions = []


global allowed_pos
allowed_pos = []

font = pygame.font.Font('slkscr.ttf', 32)

font2 = pygame.font.Font('slkscr.ttf', 20)

font3 = pygame.font.Font('slkscr.ttf', 20)

global clues
clues = 0

global board

def draw_text(text, font, color, surface, x, y): ##funcion que dibuja el texto sobre un rect
    textobj = font.render(text, 1, color) ##obj de texto
    textrect = textobj.get_rect() ##obj de rect 
    textrect.center = (x, y) ##modifica el centro del rect
    surface.blit(textobj, textrect) ##dibuja el obj de texto en el rect
    return textrect  ## devuelve el rect


def main_menu():
    global clues
    
    click = False

    global allowed_pos
    allowed_pos = []


    
    clues = 0
    while True:

        screen.fill((0,0,0))
        title = draw_text('SUDOKU', font, (255, 255, 255), screen, 300, 150)
        
        button1 = draw_text('PLAY', font2, (255, 255, 255), screen, 300, 190)
        
        button2 = draw_text('QUIT', font2, (255, 255, 255), screen, 300, 220)

        mx, my = pygame.mouse.get_pos()
        if button1.collidepoint((mx, my)):
            if click:
                difficulties() #select difficulty
                
        if button2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


#17 is the minium ammount of clues neccesary for a unique sudoku
#64 for beginners
#30 for mid
#17 hard
#board with one solution






def difficulties():

    click = False
    global clues

    while True:


        screen.fill((0,0,0))

        
        level1 = draw_text('easy', font2, (255, 255, 255), screen, 300, 160)
            
        level2 = draw_text('mid', font2, (255, 255, 255), screen, 300, 190)
            
        level3 = draw_text('hard', font2, (255, 255, 255), screen, 300, 220)
        
        mx, my = pygame.mouse.get_pos()
        
        if level1.collidepoint((mx, my)):
            if click:
                clues = 64
                game() #easy

        if level2.collidepoint((mx, my)):
            if click:
                clues = 30
                game() #mid

        if level3.collidepoint((mx, my)):
            if click:
                clues = 17
                game() #hard
                
        

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()



def generate_rects(): #just makes the squares

    current_number_clues = 0
    random_choice = 0

    ##the 60 and the 40 position each rect to a space in the sudoku board

    for i in range(0, 9 ):
        for j in range(0, 9):
            rect = pygame.Rect( 35 + j*60 , 25 + i*40 , 50 , 30 )
            squares_with_numbers[tuple(rect)] = 0
            positions.append((i, j)) #creates a list of all positions of the squares.

    

def possible(y, x, ran_number): #check if the clues aren't breaking the rules

    global board
    

    for i in range(0, 9):
        if board[y][i] == ran_number:
            return False

    for i in range(0, 9):    
        if board[i][x] == ran_number:
            return False

    x0 = (x//3)*3
    y0 = (y//3)*3
                

    for i in range(0, 3):
        for j in range(0, 3):
            if board[y0+i][x0+j] == ran_number:
                return False
            
    return True

def possible_win(y, x, number, board): #check if player gave a solution to the game.

    rep_counter = 0

    for i in range(0, 9):
        if int(board[y][i]) == number:
            rep_counter += 1

    for i in range(0, 9):    
        if int(board[i][x]) == number:
            rep_counter += 1

    x0 = (x//3)*3
    y0 = (y//3)*3
                

    for i in range(0, 3):
        for j in range(0, 3):
            if int(board[y0+i][x0+j]) == number:
                rep_counter += 1
            
    return rep_counter






def ran_gen(): #give a random number for the first, second and third row

    global board

    finished = False

    # first row

    rand = random.randint(1, 9)

    if possible(0, 0, rand):
        board[0][0] = rand
    rand = random.randint(1, 9)

    if possible(0, 4, rand):
        board[0][4] = rand

    rand = random.randint(1, 9)

    if possible(0, 8, rand):
        board[0][8] = rand

    #mid row

    rand = random.randint(1, 9)
        
    if possible(4, 0, rand):
        board[4][0] = rand
        
    rand = random.randint(1, 9)

    if possible(4, 4, rand):
        board[4][4] = rand

    rand = random.randint(1, 9)

    if possible(4, 8, rand):
        board[4][8] = rand


    #last row

    rand = random.randint(1, 9)


    if possible(8, 0, rand):
        board[8][0] = rand

    rand = random.randint(1, 9)

    if possible(8, 4, rand):
        board[8][4] = rand

    rand = random.randint(1, 9)

    if possible(8, 8, rand):
        board[8][8] = rand
    

    return board




global finished

finished = False

def solver():
    global board
    global finished
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n) and finished == False:
                        board[y][x] = n
                        solver()
                        if finished == False:
                            board[y][x] = 0 #this is used to change the previous
                                            #iteration from a number to 0.
                            #if a solution has been found, finished will be true
                            #and the previous values from previous recurssions
                            #will not run.
                return
    finished = True
    
    
    




def gen_clues(clues):

    clues = 81 - clues
    global squares
    global board
    global allowed_pos

    squares = list(squares_with_numbers.keys())

    while clues != 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if board[y][x] != 0:
            board[y][x] = 0
            allowed_pos.append((x, y))
            clues -= 1
    
    
    for square in squares:
        coor = positions[squares.index(square)]
        squares_with_numbers[square] = board[coor[1]][coor[0]]
            
            




def win_or_lose(): #check if player has won or lost.

    condition = False
    if 0 not in squares_with_numbers.values():
        whole_board = list(squares_with_numbers.values())
        whole_board = np.array([whole_board])
        whole_board = whole_board.reshape((9,9))
        for coor in positions:
            for number in range(1, 10):
                rep_amount = possible_win(coor[1], coor[0], number, whole_board)
                if rep_amount > 3: #the number of apperances will be 3. one for the row, one for the column and one for the square.
                                    #anything above that is a repeat.
                    
                    condition = False
                    return condition

    
        condition = True
        return condition
    

    
        


def check_num_clues(): #only for debugging. checks if the amount of clues given were generated.
    numbers_clues = 0 
    for rect in squares_with_numbers:
        if squares_with_numbers[rect] != 0:
            numbers_clues += 1
    print('the amount of clues generates were' ,numbers_clues)




def draw_lines():

    #borders
    pygame.draw.rect(screen, (255,255,255), left)
    pygame.draw.rect(screen, (255,255,255), right)
    pygame.draw.rect(screen, (255,255,255), top)
    pygame.draw.rect(screen, (255,255,255), bottom)

    #horizontal lines
    for i in range(0, 10):
        #horizontal lines

        if i % 3 == 0:
            horizontal = pygame.Rect(30 + i*60, 20, 6, 360)
        else:
            horizontal = pygame.Rect(30 + i*60, 20, 4, 360)
        pygame.draw.rect(screen, (255,255,255), horizontal)

    #vertical lines
    for j in range(0, 10):
        #vertical lines
        if j % 3 == 0:
            vertical = pygame.Rect(30, 20 + 40*j, 540, 6)
        else:
            vertical = pygame.Rect(30, 20 + 40*j, 540, 4)
            
        pygame.draw.rect(screen, (255,255,255), vertical)


def render_numbers(squares_with_numbers, win_condition): #loop over board to render the numbers

    click = False
    for rect in squares_with_numbers:
        if squares_with_numbers[rect] != 0:
            textSurfaceObj = font.render(str(squares_with_numbers[rect]), True, (255,255,255), (0,0,0)) #number on the board
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (rect[0] + 25 , rect[1] + 15) #the 25 and the 15 is to center the numbers
            screen.blit(textSurfaceObj, textRectObj)
            
    if win_condition != None:
        if win_condition == True:

            
            textSurfaceObj = font2.render('you win! click this box to go to the main menu', True, (255,255,255), (0,0,0)) #number on the board
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (300 , 200) #the 25 and the 15 is to center the numbers
            screen.blit(textSurfaceObj, textRectObj)
            

        elif win_condition == False:

            textSurfaceObj = font2.render('you lose. click this box to go to the main menu', True, (255,255,255), (0,0,0)) #number on the board
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (300 , 200) #the 25 and the 15 is to center the numbers
            screen.blit(textSurfaceObj, textRectObj)

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if textRectObj.collidepoint((mx, my)):
            if click:
                main_menu()
        
        
        
    

        

def game(): #game function
    global board
    global finished

    global allowed_pos
    board = [[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0]]

    board = ran_gen()

    generate_rects()

    solver()
    
    gen_clues(clues)



    clicked = False #to check if i clicked
    clicked_rect = None #to saved the clicked rect in object form

    running = True
    win_condition = None

    finished = False



    

    while running:


        screen.fill((0,0,0))

        draw_lines()
        #render the allowed number input blocks a different color
        for rect in squares_with_numbers:
            coor = positions[squares.index(rect)]
            
            if coor in allowed_pos:
                rect_allowed = pygame.Rect( rect[0] , rect[1] , 50 , 30 )
                pygame.draw.rect(screen, (128,128,128), rect_allowed )

        render_numbers(squares_with_numbers, win_condition)

        

        if clicked: #if i clicked on a square, the program will wait for a number to input.
            #the line below highlights the clicked box.
            pygame.draw.rect(screen, (193, 222, 9), clicked_rect[0])#the element in index 0 is the actual rect

            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    try:
                        number = int(event.unicode)
                        squares_with_numbers[clicked_rect[0]] = number
                        clicked = False #when it get an input, the program will no longer wait.
                        clicked_rect_str = ''
                        clicked_rect = None
                        win_condition = win_or_lose() #check if the player was won or lost.
                    except:
                        clicked = False #when it get an input, the program will no longer wait.
                        clicked_rect_str = ''
                        clicked_rect = None



        
        

        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                  
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN: #if the player clicks on a square
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0] and clicked == False: #if left click
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_rect = pygame.Rect( mouse_pos[0] , mouse_pos[1] , 5 , 5 ) #makes a temp rect for the mouse.

                    if mouse_rect.collidedict(squares_with_numbers): #checks the dictionary for which rect was clicked.
                        clicked_rect = mouse_rect.collidedict(squares_with_numbers) #this is the rect that was clicked on.
                        coor = positions[squares.index(clicked_rect[0])]
                        if coor in allowed_pos:
                            clicked = True 

                
        pygame.display.update()

main_menu()
