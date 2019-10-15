#source code1 game of life: https://www.pygame.org/project/2899/4734
#source code2 text display: https://pythonprogramming.net/displaying-images-pygame/
#source code3 moving object (in Chinese): https://zhuanlan.zhihu.com/p/40807732

from collections import OrderedDict
import pygame,random
from pygame.locals import *
import time

pygame.init()

speed = 10 # how many iterations per second
squares = 1 # size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size = 32 # the width and height

green=(0,200,0)
bright_green=(0,225,0)
white=(200,200,200)
        

if squares == 0:
        imgs = ["res/alive_8.png","res/dead_8.png",8]
if squares == 1:
        imgs = ["res/alive_16.png","res/dead_16.png",16]
if squares == 2:
        imgs = ["res/alive_32.png","res/dead_32.png",32]
if squares == 3:
        imgs = ["res/alive_64.png","res/dead_64.png",64]

        
#-----CONFIG-----

width = map_size*imgs[2] #width=512
height = map_size*imgs[2]
screen_size = width,600
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
done = False #game is running 
             
screen.fill(white)


#people
people_image = pygame.image.load('res/people.png')

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',25)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((250),(540))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        #time.sleep(2)
        #game_loop()

class People(pygame.sprite.Sprite):
        def __init__(self,up_speed,down_speed):
                pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
                self.up_speed = up_speed #speed of people going up
                self.down_speed=down_speed
                self.image=people_image
                self.rect=self.image.get_rect() #position
                self.rect.top=0
                self.rect.left=0
        def moveup(self):
                self.rect.top -= self.up_speed*0.3
        def movedown(self):
                self.rect.top += self.down_speed*0.5
        def moveforward(self):
                self.rect.right += self.up_speed*0.3
                if self.rect.right > width:
                        self.rect.left=0

people=People(6, 4)

class cell:

        def __init__(self,location,alive = False):
                self.to_be = None
                self.alive = alive
                self.pressed = False
                self.location = location

class board:

        def __init__(self):
                self.map = []
                
        def fill(self,ran):
                for i in range(map_size): # x coordinate
                        self.map.append([])
                        for g in range(map_size): # y coordinate
                                if ran == True:
                                        a = random.randint(0,4)
                                        if a == 0: self.map[i].insert(g,cell((i,g),True))
                                        else: self.map[i].insert(g,cell((i,g))) 
                                else: self.map[i].insert(g,cell((i,g)))
                                        

        def draw(self): 
                for i in range(map_size):
                        for g in range(map_size):
                                cell = self.map[i][g]
                                loc = cell.location
                                if cell.alive == True:
                                        screen.blit(alive,(loc[0]*imgs[2],loc[1]*imgs[2]))
                                else:
                                        screen.blit(dead,(loc[0]*imgs[2],loc[1]*imgs[2]))

        def get_cells(self,cell):# gets the cells around a cell
                mapa = self.map
                a = []
                b = []
                c = 0
                cell_loc = cell.location
                try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
                except Exception: pass
                try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
                except Exception: pass
                num = len(list(OrderedDict.fromkeys(a))) # removes duplicates
                for i in range(len(a)): b.append(mapa[a[i][0]][a[i][1]].alive)
                for i in b:# c houses how many cells are alive around it
                        if i == True: c+=1
                if cell.alive == True:# rules
                        if c < 2: cell.to_be = False #dead
                        if c > 3:cell.to_be = False #dead
                else:
                        if c == 3: cell.to_be = True #live
#rules
        def update_frame(self):
                for i in range(map_size):
                        for g in range(map_size):
                                cell = self.map[i][g]
                                self.get_cells(cell)

        def update(self):
                for i in range(map_size):
                        for g in range(map_size):
                                cell = self.map[i][g]
                                loc = cell.location
                                if cell.to_be != None: cell.alive = cell.to_be
                                if self.map[i][g].alive == True: screen.blit(alive,(loc[0]*imgs[2],loc[1]*imgs[2]))
                                else: screen.blit(dead,(loc[0]*imgs[2],loc[1]*imgs[2]))
                                cell.to_be = None

def cell_list():
    lst = []
    for i in range(map_size):
        lst.append([])
        for g in range(map_size): lst[i].append((board.map[i][g].location[0]*imgs[2],board.map[i][g].location[1]*imgs[2]))
    return lst

board = board()
board.fill(False)
board.draw()  
tp = 0
run = False

while done == False:
        milliseconds = clock.tick(60)
        seconds = milliseconds / 1000.0
        tp += milliseconds
        message_display('Space:run/stop, left click: raises cells')

        pressed = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get(): #looping for getting event
                if event.type == QUIT: #to see if the game is quit
                        done = True

                if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                                run = not run

                if event.type == KEYUP:
                        if event.key == K_q:
                                run = False
                                board.update_frame()
                                board.update()

                if event.type == MOUSEBUTTONUP:
                        for i in range(map_size):
                                for g in range(map_size):
                                        board.map[i][g].pressed = False

        
        if not pressed[K_UP] and people.rect.bottom<height and run ==True:
                people.movedown()
                people.moveforward()
        elif pressed[K_UP] and people.rect.top>0 and run==True:
                people.moveup()
                people.moveforward()
        screen.blit(people_image,people.rect)

        if pressed[K_r]:
                board.map = []
                board.fill(False)
                board.draw()
        if pressed[K_a]:
                board.map = []
                board.fill(True)
                board.draw()

        if run == True and tp >= 1000/speed :
                tp = 0
                board.update_frame()
                board.update()

        if mouse[0]:# makes cells alive
                rects = cell_list()
                for i in range(map_size):
                        for g in range(map_size):
                                if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+imgs[2] and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+imgs[2] and board.map[i][g].pressed == False:
                                        board.map[i][g].alive = True
                                        board.map[i][g].pressed = True
                                        board.update()

        if mouse[2]: # kills cells
                rects = cell_list()
                for i in range(map_size):
                        for g in range(map_size):
                                if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+imgs[2] and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+imgs[2] and board.map[i][g].pressed == False:
                                        board.map[i][g].alive = False
                                        board.map[i][g].pressed = False
                                        board.update()

        
        pygame.display.flip() #display all the things

pygame.quit()
