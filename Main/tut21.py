import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#colours:
white= (255,255,255)
red= (255,0,0)
black= (0,0,0)
colour=(121, 29, 84)

#Creating window
screen_width=900
screen_height=600

#Background image:
start=pygame.image.load("BG pics/start.gif")
start=pygame.transform.scale(start,(screen_width,screen_height))

#Grass background:
grass=pygame.image.load("BG pics/grass.gif")
grass=pygame.transform.scale(grass,(screen_width,screen_height))

#Ending background:
end=pygame.image.load("BG pics/ending.gif")
end=pygame.transform.scale(end,(screen_width,screen_height))

#Fruit image:
apple=pygame.image.load("BG pics/apple.gif")
apple=pygame.transform.scale(apple,(30,30))

#Snake image:
snat=pygame.image.load("BG pics/snaket.gif")
snat=pygame.transform.scale(snat,(28,28))

#Score bar:
sbar=pygame.image.load("BG pics/scorebar.gif")
sbar=pygame.transform.scale(sbar,(screen_width,50))

width=300
height=150

gameWindow=pygame.display.set_mode((screen_width,screen_height))

#Game title:
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock=pygame.time.Clock()
font = pygame.font.SysFont("Jersey15-Regular", 40)

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
     for x,y in snk_list:
         pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])
         gameWindow.blit(snat,(x,y))


def welcome():
    exit_game=False
    pygame.mixer.music.load("Audio files/start.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(start,(0,0))
        text_screen("Press Any Key To Continue",black,20,500)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                pygame.mixer.music.load("Audio files/back.mp3")
                pygame.mixer.music.play()
                gameloop()
        
        pygame.display.update()
        clock.tick(80)

#Game loop
def gameloop():
    # Game specific variables
    exit_game=False
    game_over=False
    snake_x=450
    snake_y=300
    velocity_x=0
    velocity_y=0
    # Initialize hiscore
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        hiscore = f.read().strip()
        if not hiscore.isdigit():
            hiscore = 0
        else:
            hiscore = int(hiscore)

    food_x=random.randint(100, width)
    food_y=random.randint(100, height)
    score=0
    init_velocity=5
    snake_size=28
    fps=80

    snk_list=[]
    snk_length=1

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(end,(0,0))
            text_screen("PRESS ENTER TO CONTINUE",red,175,350)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()            

        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0

                    if event.key==pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0

                    if event.key==pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0

                    if event.key==pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0

                    if event.key==pygame.K_q:
                        score +=10


            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            if abs(snake_x-food_x)<25 and abs(snake_y-food_y)<25:
                score+=10
                pygame.mixer.music.load("Audio files/eatfruit.mp3")
                pygame.mixer.music.play()
            
                food_x=random.randint(60, screen_width-150)
                food_y=random.randint(60, screen_height-150)
                snk_length+=5
                if score>int(hiscore):
                    hiscore=score

            gameWindow.fill(white)
            gameWindow.blit(grass,(0,0))
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
            gameWindow.blit(apple,(food_x,food_y))
            gameWindow.blit(sbar,(0,0))
            text_screen("Score: "+str(score)+ "                            HighScore: "+ str(hiscore),white,25,3)

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over= True
                pygame.mixer.music.load("Audio files/end.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>(screen_width-10):
                game_over=True
                pygame.mixer.music.load("Audio files/end.mp3")
                pygame.mixer.music.play()

            if snake_y < 50 or snake_y > (screen_height-10):
                game_over= True
                pygame.mixer.music.load("Audio files/end.mp3")
                pygame.mixer.music.play()

        plot_snake(gameWindow,black,snk_list,snake_size) 
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome()
gameloop()