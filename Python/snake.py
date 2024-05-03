import pygame
from sys import exit
import random

# WIDTH and HEIGHT
WIDTH = 1000
HEIGHT = 600

#  snake part in pixels
UNIT = 25

# Snake
snake = [[100 , 100] ,
         [100 + UNIT , 100] ,
         [100 + (UNIT * 2), 100] , 
         [100 + (UNIT * 3), 100]]

# Snake moveing direction

goingUp = False
goingDown = False
goingRight = True
goingLeft = False

# Food position
food = []

eaten = True

# Score
score = 0

# Main game flag
game_over = True

# difficality 
difficality = ""

intro = True

def draw():      # Draw everything
    
    r = 0
    g = 0
    b = 255
    
    isgreen = False
    isblue = False
    isred = False
    
    food_surface = pygame.Surface( (UNIT , UNIT) )
    food_surface.fill("red")
    food_rect = food_surface.get_rect(topleft = food)
    screen.blit(food_surface, food_rect)
    
    for i in snake:
        surface = pygame.Surface( ( UNIT, UNIT ) )
        surface.fill("green")
        surface_rect = surface.get_rect(topleft = i)
        

        surface.fill((r , g , b))
        
        if (r , g , b) == (0 , 0 , 255) :
            isblue = True
            isred = False
            isgreen = False
        if (r , g , b) == (0 , 255 , 0) :
            isgreen = True
            isblue = False
            isred = False
        if (r , g , b) == (255 , 0 , 0) :
            isred = True
            isblue = False
            isgreen = False
            
        if isred :
            r -= 5
            g += 5
        if isgreen :
            g -= 5
            b += 5
        if isblue :
            b -= 5
            r += 5

        if i == snake[-1]:
            surface.fill("black")
        screen.blit(surface , surface_rect)    
       
def  moveSnake(touched):      # Move the snake
    global goingRight
    global goingLeft
    global goingUp
    global goingDown
    
    x , y = snake[-1]

        
    if not touched :
        snake.remove(snake[0])
    
    if goingRight:
        if x + UNIT >= WIDTH and difficality == "easy" :
            part = [0 , y]
        else:
            part = [x + UNIT , y] 
    if goingLeft:
        if x - UNIT < 0 and difficality == "easy":
            part = [WIDTH , y]
        else:
            part = [x - UNIT , y]    
    if goingUp:
        if  y - UNIT < 0 and difficality == "easy":
            part = [x , HEIGHT]
        else:
            part = [x , y - UNIT] 
    if goingDown:
        if y + UNIT >= HEIGHT and difficality == "easy":
            part = [x , 0]
        else:
            part = [x , y + UNIT]
    
    snake.append(part)
              
def createFood():      # Make a random food
    x = (random.randint(1 , WIDTH // UNIT) * UNIT) - UNIT
    y = (random.randint(1 , HEIGHT // UNIT) * UNIT) - UNIT
    while [x , y] in snake:
        x = (random.randint(1 , WIDTH // UNIT) * UNIT) - UNIT
        y = (random.randint(1 , HEIGHT // UNIT) * UNIT) - UNIT

    return [x , y]

def touch():         # check if the is eaten
    if snake[-1] == food:
        return True
    else:
        return False

def check_end_game(snake):
    global game_over
    head = snake[-1]
    new_snake = snake[:len(snake)-1]
    for part in new_snake:
        if part == head:
            game_over = True
    if (head[0] <= 0 or head[0] >= WIDTH or head[1]  <= 0 or head[1] >= HEIGHT) and difficality == "hard":
        game_over = True

pygame.init()
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

text = pygame.font.Font(None , 50)


#intro screen
surface = pygame.Surface((WIDTH , HEIGHT))
surface.fill("orange")
surface_rect = surface.get_rect(center = (WIDTH // 2 , HEIGHT // 2))
wellcome_text = pygame.font.Font(None , 30)
wellcome_text = wellcome_text.render("Snake" , True , "black")
wellcome_rect = wellcome_text.get_rect(center = (WIDTH // 2 , 150))

block_surface = pygame.Surface( (200 , 200) )
block_rect = block_surface.get_rect(center = (300 , 400))
computer_text = pygame.font.Font(None , 30)
computer_text = computer_text.render("Hard" , True , "black")
computer_rect = computer_text.get_rect(center = (300 , 400))
block_surface.fill("black")


block2_surface = pygame.Surface( (200 , 200) )
block2_rect = block2_surface.get_rect(center = (WIDTH - 300 , 400))
firend_text = pygame.font.Font(None , 30)
firend_text = firend_text.render("Easy" , True , "black")
firend_rect = firend_text.get_rect(center = (WIDTH - 300 , 400))
block2_surface.fill("black")




counter = 0
while True:
    screen.fill("orange")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and  not goingDown :
                goingUp = True
                goingRight = False
                goingLeft = False
            if event.key == pygame.K_DOWN and not goingUp:
                goingDown = True
                goingRight = False
                goingLeft = False
            if event.key == pygame.K_RIGHT and not goingLeft:
                goingRight = True
                goingUp = False
                goingDown = False
            if event.key == pygame.K_LEFT and not goingRight:
                goingLeft = True
                goingUp = False
                goingDown = False
        if event.type == pygame.MOUSEBUTTONDOWN and intro:
            if block_rect.collidepoint(pos):
                difficality = "hard"
                intro = False
                game_over = False
            if block2_rect.collidepoint(pos):
                difficality = "easy"
                intro = False
                game_over = False
    if intro:
        pos = pygame.mouse.get_pos()
        color1 = (0 , 0 , 0)
        color2 = (0 , 0 , 0)
        if block_rect.collidepoint(pos):
            color1 = (90 , 90 , 90)
        if block2_rect.collidepoint(pos):
            color2 = (90 , 90 , 90)
        
        surface.blit(wellcome_text , wellcome_rect)
        pygame.draw.rect(surface ,color1, block_rect , 3 , 10)
        pygame.draw.rect(surface ,color2, block2_rect , 3 , 10)
        surface.blit(computer_text , computer_rect)
        surface.blit(firend_text , firend_rect)
        screen.blit(surface , surface_rect)
        pygame.display.update()    

    else:
        if not game_over:    
            if counter % 6 == 0:
                if touch():
                    moveSnake(True)
                    score += 10
                    eaten = True
                else:
                    moveSnake(False)
                    
                
                if eaten:
                    food = createFood()
                    eaten = False
                draw()
                score_text = text.render(str(score) , True , "black")
                screen.blit(score_text , (20 , 20))
                check_end_game(snake)
                pygame.display.update()    
                
            counter += 1
    clock.tick(60)