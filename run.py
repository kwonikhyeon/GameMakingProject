import pygame
from pygame.locals import *
import sys, os
from contents import *

#COLORS
           #R    G    B
BLUE =     (0,   0,   255)
GREEN =    (0,   128, 0)
PURPLE =   (128, 0,   128)
RED =      (255, 0,   0)
YELLOW =   (255, 255, 0)
NAVYBLUE = (0,   0,   128)
WHITE =    (255, 255, 255)
BLACK =    (0,   0,   0)
ALPHA =    (255, 0,   255)

def drawText(text, font, surface, x, y, color):
#Simple function for drawing text onto the screen. Function contains expression
#for word wrap.
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  
  textobj1 = font.render(textLine1,1,color)
  textrect1 = textobj1.get_rect()
  textrect1.topleft = (x,y)
  surface.blit(textobj1,textrect1)
  pygame.display.update()
  
  textobj2 = font.render(textLine2,1,color)
  textrect2 = textobj2.get_rect()
  textrect2.topleft = (x,y+10)
  surface.blit(textobj2,textrect2)
  pygame.display.update()

class Button():
#Class for creating and maintaining unique buttons for a number of different 
#purposes.
  def assignImage(self, picture):
  #function for handling the assignment of an image to each individual button object
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
  #Function for handling the assignment of coordinates for each individual button 
  #object
    self.rect.topleft = x,y
  def drawButton(self, picture):
  #Function for handling drawing the actual button on the screen
    DISPLAYSURF.blit(picture, self.rect)
  def pressed(self,mouse):
  #Function for determining whether or not a mouse click is inside a button object
    if self.rect.collidepoint(mouse) == True:
      return True

def battle(player, com):
    while(True):
        #플레이어 선택
        
        #컴 선택
        
        
        if player.hp <= 0 or com.hp <= 0:
            if player.hp <= 0: print(f"{com.name} 의 승리!")
            else: print(f"{player.name} 의 승리!")
            break


def run(DISPLAYSURF, TEXTSURF, player, com):
    

    background = pygame.image.load("testbackground.png")
    testplayer = pygame.image.load("testperson.png")
    testcom = pygame.image.load("testperson.png")

    DISPLAYSURF.blit(background, (0,0)) #윈도우에 이미지 삽입
    DISPLAYSURF.blit(testplayer, (120,200))
    DISPLAYSURF.blit(testcom, (450,30))

    testbuttonImg = pygame.image.load("buttonImg.png")

    NAButton = Button() #일반공격버튼
    NAButton.assignImage(testbuttonImg)
    NAButton.setCoords(400, 440)
    CAButton = Button()
    CAButton.assignImage(testbuttonImg)
    CAButton.setCoords(400, 490)
    HButton = Button()
    HButton.assignImage(testbuttonImg)
    HButton.setCoords(400, 540)

    NAButton.drawButton(testbuttonImg)
    CAButton.drawButton(testbuttonImg)
    HButton.drawButton(testbuttonImg)

    pygame.display.update() #변경된 사항(화면) 업데이트

    while(1):
        #플레이어 선택
        picked = 0
        while not picked:
          for event in pygame.event.get(): #running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
            if event.type == QUIT:
              pygame.quit()
              sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
              mouse = pygame.mouse.get_pos()
              if NAButton.pressed(mouse) == True:
                player.normalAttack(com)
                picked = 1
              if CAButton.pressed(mouse) == True:
                player.criticalAttack(com)
                picked = 1
              if HButton.pressed(mouse) == True:
                player.heal()
                picked = 1
        player.state()
        com.state()
        #승패판단
        if com.hp <= 0:
            print(f"{player.name} 의 승리!")
            break

        #컴 선택
        com.action_ai(player)
        
        player.state()
        com.state()
        #승패판단
        if player.hp <= 0:
            print(f"{com.name} 의 승리!")
            break    
'''
    while(1):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
'''
if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((700, 700)) #이미지 윈도우
    TEXTSURF = pygame.display.set_mode((700,700)) #텍스트 윈도우
    pygame.display.set_caption('Bokhakmon') #윈도우 이름
    fpsClock = pygame.time.Clock()
    FPS = 20
    font = pygame.font.SysFont(None, 20)

    player = Person("익현", "남", 100, 50, 50, 600)
    com = Com("보스", "남", 80, 50, 50, 600, [40,40,20])

    run(DISPLAYSURF, TEXTSURF, player, com)