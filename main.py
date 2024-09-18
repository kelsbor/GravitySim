# Procurar biblioteca para fazer simulação (ok)
# Criar uma janela básica (ok)
# Criar o básico (ok)
# Simulador de gravidade (Ok)

# Interface que crie novos objetos:
# 1. mostrar texto com velocidade (ok)
# 2. criar mais objetos em torno de um unico, (ok) 
# 2.1 zoom function (+-) porcaria
# 2.2 camera fixa (ok)
# 3. por fim, montar interface: 
#   button class (ok) e textbox class (ok)
#   função de mudar alvo, :(
#   função de criar planetas (oki)

import os
import pygame
import math
from itertools import combinations


#global variables
WIDTH, HEIGHT = 1490,900

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
TEXT_COLOR = "white"
BUTTON_COLOR = "blue"
FONT_SIZE = 25
BUTTON_HOVER_COLOR = "red"
font = pygame.font.Font(None, FONT_SIZE)
running = True
zoom_level = 1
camera_x, camera_y = 0,0
target = False
planet_interface = False
paused = False
dt = 0
pn = 1

def to_screen_coordinates(global_x, global_y):
    #print(global_x - camera_x, global_y - camera_y)
    return (global_x - camera_x), (global_y - camera_y)


#background variables
back_image = pygame.image.load('Assets/background_univ.jpg')
back_image = pygame.transform.scale(back_image, (WIDTH, HEIGHT))
back_rect = back_image.get_rect()

#planet images
earth_sprite = pygame.image.load('Assets/earth.png')

class Planeta:
    def __init__(self, pos, size, mass, sprite, speed):
        self.mass = mass
        self.sprite = sprite
        self.size = size
        self.pos = pos
        self.speed = speed

    def render(self):
        sprite_size = (int(self.size*zoom_level), int(self.size*zoom_level))
        screen_sprite_pos = to_screen_coordinates(self.pos[0]*zoom_level, self.pos[1]*zoom_level)

        scaled_sprite = pygame.transform.scale(self.sprite, sprite_size)
        self.rect = sprite_rect = scaled_sprite.get_rect(center=screen_sprite_pos)
        screen.blit(scaled_sprite, sprite_rect)
        
    def apply_force(self, force):
        self.speed[0] += force[0]/self.mass
        self.speed[1] += force[1]/self.mass

    def move(self):
        self.pos = (self.pos[0] + self.speed[0]*dt, self.pos[1] + self.speed[1]*dt)

class Button:
    def __init__(self, pos, width, height, text, action):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = text
        self.action = action
        self.pos = pos

    def draw(self, hover):
        button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, "white", self.rect, 2)  # Add border
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Text:
    def __init__(self, pos, text, color, size):
        self.pos = pos
        self.text = text
        self.color = color
        self.size = size

    def texting(self):
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.pos
        screen.blit(text_surface,text_rect)

class TextBox:
    def __init__(self, rect, confirm, font_size=FONT_SIZE, color='white', active_color='yellow'):
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.active_color = active_color
        self.text = ""
        self.active = False
        self.confirm = confirm

    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif event.type == pygame.KEYDOWN and self.active:
                if self.confirm == True:
                    if event.key == pygame.K_RETURN:
                        confirm_text = self.text
                        change_values(confirm_text)
                        print("User input:", self.text)
                        self.text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, self.active_color if self.active else self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect.topleft)

def is_hovering(button, mouse_pos):
    return button.rect.collidepoint(mouse_pos)

def calc_gravity(obj1, obj2, G=0.01):
    # distancia entre os dois objetos
    dx = obj1.pos[0] - obj2.pos[0]
    dy = obj1.pos[1] - obj2.pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance < 0.001:
        distance = 0.001

    g_force = (G * obj1.mass * obj2.mass) / distance**2
    angle = math.atan2(dy,dx)

    force_x = g_force * math.cos(angle)
    force_y = g_force * math.sin(angle)

    return force_x, force_y

# create planets
def new_planet():
    global paused
    if paused == False:
        paused = True

def create_planet(x,y):
    global paused
    print(x,y)
    if paused == True:
        new_planet = Planeta([x +camera_x/zoom_level, y + camera_y/zoom_level], 100, 1000, earth_sprite, [40,40])
        planets.insert(-1, new_planet)
        paused = False

sun = Planeta([1000,400], 200, 33294600, earth_sprite, [0,0])
earth = Planeta([100,400], 100, 112000, earth_sprite,[0, 100])
moon = Planeta([50,400],50, 100, earth_sprite, [0,130])
planets = [sun, earth, moon]
target_object = planets[pn]

def start_world():
    attr_comb = combinations(planets, 2)
    for comb in attr_comb:
        gravity_force = calc_gravity(comb[0], comb[1])
        #print(comb, gravity_force)
        comb[0].apply_force((-gravity_force[0],-gravity_force[1]))
        comb[1].apply_force(gravity_force)
    
    for planet in planets:
        if planet == target_object:
            planet.sprite.set_colorkey((0,255,0,128))
            planet.render()
            planet.move()
        else:
            planet.render()
            planet.move()

def change_target():
    global pn
    global target_object 
    pn += 1
    if pn > len(planets) - 1:
        pn = 0
    target_object = planets[pn]
    print(pn)

buttons = [
    Button((0.05*WIDTH,0.05*HEIGHT), 150, 50, "Target", lambda: change_target()),
    Button((0.2*WIDTH, 0.05*HEIGHT), 150, 50, "New Planet", lambda: new_planet())
]

interface_text_box = [
    TextBox(confirm=True, rect=(WIDTH*0.05, HEIGHT*0.2, 150, 40))
]

# render text
def load_interface():
    for button in buttons:
        hover = is_hovering(button, pygame.mouse.get_pos())
        button.draw(hover)
    
    for text in texts:
        text.texting()
    
    for textb in interface_text_box:
        textb.render(screen)

def change_values(value):
    target_object.mass *= int(value)

while running:
    for event in pygame.event.get():
        interface_text_box[0].handle_event(event)

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and paused:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x,mouse_y)
            create_planet(mouse_x*zoom_level,mouse_y*zoom_level)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in buttons:
                if is_hovering(button, (mouse_x, mouse_y)):
                    button.action()
            
            #for planet in planets:
            #    if is_hovering(planet, (mouse_x, mouse_y)):

            if event.button == 4:  # Scroll up
                zoom_level *= 1.05
            elif event.button == 5:  # Scroll down
                zoom_level /= 1.05
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        camera_y -= 10  # Move the camera up
    elif keys[pygame.K_DOWN]:
        camera_y += 10  # Move the camera down
    elif keys[pygame.K_LEFT]:
        camera_x -= 10  # Move the camera left
    elif keys[pygame.K_RIGHT]:
        camera_x += 10  # Move the camera right
    
    screen.blit(back_image, back_rect)

    if not paused:
        texts = [
            Text((WIDTH*0.1, HEIGHT*0.9), f'Speed: X = {int(target_object.speed[0])}, Y = {int(target_object.speed[1])}', TEXT_COLOR, FONT_SIZE),
            Text((WIDTH*0.1, HEIGHT*0.85), f'Mass: {int(target_object.mass)}', TEXT_COLOR,FONT_SIZE)
        ]

        if target == True:
            camera_x = target_object.pos[0] - WIDTH/2 
            camera_y = target_object.pos[1] - HEIGHT/2

        start_world()

    load_interface()        

    if paused:
        font = pygame.font.Font(None, 36)
        text = font.render("Click to select a position", True, 'red')
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    dt = clock.tick(50) / 1000

pygame.quit()