import pygame
from pygame.locals import *
import sys, os

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

def run(DISPLAYSURF, TEXTSURF):
    

    background = pygame.image.load("testbackground.jpg")
    testplayer = pygame.image.load("testplayer.jpg")
    testcom = pygame.image.load("testcom.jpg")

    DISPLAYSURF.blit(background, (0,0)) #윈도우에 이미지 삽입
    DISPLAYSURF.blit(testplayer, (100,300))
    DISPLAYSURF.blit(testcom, (600,30))

    testbuttonImg = pygame.image.load("buttonImg.jpg")

    NAButton = Button() #일반공격버튼
    NAButton.assignImage(testbuttonImg)
    NAButton.setCoords(50, 520)
    CAButton = Button()
    CAButton.assignImage(testbuttonImg)
    CAButton.setCoords(400, 520)
    HButton = Button()
    HButton.assignImage(testbuttonImg)
    HButton.setCoords(750, 520)

    NAButton.drawButton(testbuttonImg)
    CAButton.drawButton(testbuttonImg)
    HButton.drawButton(testbuttonImg)

    pygame.display.update() #변경된 사항 업데이트

    while(1):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((1000, 750)) #이미지 윈도우
    TEXTSURF = pygame.display.set_mode((1000,750)) #텍스트 윈도우
    pygame.display.set_caption('Bokhakmon') #윈도우 이름
    fpsClock = pygame.time.Clock()
    FPS = 20
    font = pygame.font.SysFont(None, 20)
    run(DISPLAYSURF, TEXTSURF)