#IMPORTS
import pygame
from pygame.locals import *
import json


#INITIALISATION
pygame.init()
pygame.mixer.init()



#LOAD SETTINGS/IMAGES
with open("settings.json", "r") as f:
    data = json.load(f)

WIDTH = data["WIDTH"]
HEIGHT = data["HEIGHT"]
FPS = data["FPS"]

BRICK_1 = pygame.image.load("assets/images/bricks_1.png")
BRICK_2 = pygame.image.load("assets/images/bricks_2.png")
HEART_1 = pygame.image.load("assets/images/heart_1.png")
HEART_1 = pygame.transform.scale(HEART_1, (30, 30))
HEART_2 = pygame.image.load("assets/images/heart_2.png")
HEART_2 = pygame.transform.scale(HEART_2, (30, 30))


#LOAD WINDOW
clock = pygame.time.Clock()
window_size = [WIDTH, HEIGHT]
pygame.display.set_caption("Breakout")
screen = pygame.display.set_mode(window_size) 
display = pygame.Surface(window_size)


#OBJECTS
class Player:
    def __init__(self):
        self.img = pygame.image.load("assets/images/player.png")
        self.rect = pygame.Rect(50, 50, self.img.get_width(), self.img.get_height())
        self.rect.x = round((window_size[0] / 2) - (self.img.get_width() / 2))
        self.rect.y = round(window_size[1] - 50)

class Brick:
    def __init__(self, x, y):
        self.img = BRICK_1
        self.rect = pygame.Rect(50, 50, self.img.get_width(), self.img.get_height())
        self.rect.x = x
        self.rect.y = y

class Ball:
    def __init__(self):
        self.img = pygame.image.load("assets/images/ball.png")
        self.rect = pygame.Rect(50, 50, self.img.get_width(), self.img.get_height())
        self.rect.x = round((window_size[0] / 2) - (self.img.get_width() / 2))
        self.rect.y = round(window_size[1] - 70)


#VARIABLES
moving_right = False
moving_left = False
paused = False
diagonal_x = -2
diagonal_y = -2
player = Player()
ball = Ball()
timer = 0
hearts = 3
message = False


#BRICKS GENERATION
bricks = []
for i in range (10):
    c = i + 1
    x = 50 - BRICK_1.get_width()
    for j in range(10):
        if i > 2:
            bricks.append(Brick(x, c * 20))
            x += 50


def collide(obj1, obj2):
    if obj1.rect.colliderect(obj2.rect):
        return True
    return False

def get_time(timer):
    seconds = int(timer / FPS)
    miliseconds = str(((timer / FPS) - seconds) * 100)
    minutes = int(seconds / 60)
    seconds = seconds - (minutes * 60)
    return f"{minutes}:{seconds}:{miliseconds[0]}"


while True:
    #CLEAR THE FRAME/INCREMENT TIMER
    display.fill((0, 0, 0))


    #GAME LOGIC
    if not message:
        if hearts < 1:
            message_data = [0, "Game over!", "Impact", "white"]
            message = True
        elif len(bricks) < 1:
            message_data = [0, f"You Win!\nTime: {get_time(timer)}", "Impact", "white"]
            message = True
    else:
        message_data[0] += 1
        size = int(message_data[0] / 2)
        if size < 1:
            size = 1
        if size > 40:
            size = 40
        font = pygame.font.SysFont(message_data[2], size)
        message_text = font.render(message_data[1], 1, pygame.Color(message_data[3]))
        display.blit(message_text, (round((display.get_width() / 2) - (message_text.get_width() / 2)), round((display.get_height() / 2) - (message_text.get_height() / 2))))
        if message_data[0] >= 1 * FPS:
            if message_data[0] >= 7 * FPS:
                message = False
                pygame.quit()
    if paused:
        font = pygame.font.SysFont("Impact", 55)
        paused_text = font.render("PAUSED", 1, pygame.Color("azure3"))
        display.blit(paused_text, (round((display.get_width() / 2) - (paused_text.get_width() / 2)), round((display.get_height() / 2) - (paused_text.get_height() / 2))))




    #PLAYER LOGIC
    if not paused and not message:
        timer += 1
        if moving_right:
            player.rect.x += 5
            if player.rect.x > (display.get_width() - player.img.get_width()):
                player.rect.x = (display.get_width() - player.img.get_width())
        if moving_left:
            player.rect.x -= 5
            if player.rect.x < 0:
                player.rect.x = 0
        if collide(player, ball):
            diagonal_y = -diagonal_y
    

    #BALL LOGIC
    if not paused and not message:
        ball.rect.x += diagonal_x
        ball.rect.y += diagonal_y

        if ball.rect.x < 1:
            diagonal_x = -diagonal_x
        if ball.rect.x > (display.get_width() - ball.img.get_width()):
            diagonal_x = -diagonal_x

        if ball.rect.y < 1:
            diagonal_y = -diagonal_y
        if ball.rect.y > (display.get_width() - ball.img.get_width()):
            diagonal_y = -diagonal_y
            hearts -= 1
            ball.rect.x = round((window_size[0] / 2) - (ball.img.get_width() / 2))
            ball.rect.y = round(window_size[1] - 70)

        for brick in bricks[:]:
            if collide(brick, ball):
                if brick.rect.y >= ball.rect.y + ball.img.get_height() or brick.rect.y + brick.img.get_height() >= ball.rect.y:
                    diagonal_y = -diagonal_y
                if brick.rect.x >= ball.rect.x + ball.img.get_width() or brick.rect.x + brick.img.get_width() <= ball.rect.x:
                    diagonal_x = -diagonal_x
                bricks.remove(brick)


    #RENDERING
    display.blit(player.img, (player.rect.x, player.rect.y))
    display.blit(ball.img, (ball.rect.x, ball.rect.y))
    for brick in bricks:
        display.blit(brick.img, (brick.rect.x, brick.rect.y))
    font = pygame.font.SysFont("Impact", 25)
    time = get_time(timer)
    timer_text = font.render(time, 1, pygame.Color("white"))
    display.blit(timer_text, (round(display.get_width() - timer_text.get_width()) - 5, 5))
    x = 5
    for i in range(3):
        if hearts >= i+1:
            display.blit(HEART_1, (x, 5))
        else:
            display.blit(HEART_2, (x, 5))
        x += 35


    #EVENTS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key in (K_e, K_RIGHT):
                moving_right = True
            elif event.key in (K_q, K_LEFT):
                moving_left = True
            elif event.key == K_ESCAPE:
                if not paused:
                    paused = True
                else:
                    paused = False

        elif event.type == KEYUP:
            if event.key in (K_e, K_RIGHT):
                moving_right = False
            elif event.key in (K_q, K_LEFT):
                moving_left = False


        elif event.type == MOUSEMOTION:
            if not paused and not message:
                player.rect.x = pygame.mouse.get_pos()[0] - round(player.img.get_width() / 2)


    #Display
    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
