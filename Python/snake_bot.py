import pygame
from sys import exit
import random


# WIDTH and HEIGHT
WIDTH = 600
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
goingDown = True
goingRight = False
goingLeft = False

# Food position
food = []

eaten = True

# Score
score = 0

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

    food_x , food_y = food

    if x < food_x and not goingLeft:
        goingRight = True
        goingLeft = False
        goingUp = False
        goingDown = False        
    elif x > food_x and not goingRight :
        goingLeft = True
        goingRight = False
        goingUp = False
        goingDown = False
    elif y > food_y and not goingDown:
        goingUp = True
        goingDown = False
        goingLeft = False
        goingRight = False
    elif y < food_y and not goingUp :
        goingDown = True
        goingUp = False
        goingRight = False
        goingLeft = False
        
    if not touched :
        snake.remove(snake[0])
    
    if goingRight:
        if x + UNIT >= WIDTH :
            part = [0 , y]
        else:
            part = [x + UNIT , y] 
    if goingLeft:
        if x - UNIT < 0 :
            part = [WIDTH , y]
        else:
            part = [x - UNIT , y]    
    if goingUp:
        if  y - UNIT < 0 :
            part = [x , HEIGHT]
        else:
            part = [x , y - UNIT] 
    if goingDown:
        if y + UNIT >= HEIGHT :
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


pygame.init()
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

text = pygame.font.Font(None , 50)


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

    
    if counter % 3 == 0:
        
        if eaten:
            food = createFood()
            eaten = False
        
        if touch():
            moveSnake(True)
            score += 10
            eaten = True
        else:
            moveSnake(False)

        draw()
        score_text = text.render(str(score) , True , "black")
        screen.blit(score_text , (20 , 20))

        pygame.display.update()
    counter += 1
        
    clock.tick(60)