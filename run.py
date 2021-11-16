import pygame
from pygame.locals import *
import sys, os
from contents import *
import time

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

buttonGrid = [[400, 440], [400, 500], [400, 560], [400, 620]]

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

def animateText(text, font, surface, x, y, color):
#Function for printing text. The first block of code acts as a word wrap creator
#in the event that the string is too long to fit in the window. The animated portion
#is simply the act of adding each additional charcter after a tick in the FPS clock.
  if len(text) > 49:
    textLine1 = text[:49]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  i = 0
  for letter in textLine1:
    realLine1 = textLine1[:i]
    textobj1 = font.render(realLine1,1,color)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x,y)
    surface.blit(textobj1,textrect1)
    pygame.display.update()
    fpsClock.tick(FPS)
    i += 1
  j = 0
  for letter in textLine2:
    realLine2 = textLine2[:j]
    textobj2 = font.render(textLine2,1,color)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x,y+10)
    surface.blit(textobj2,textrect2)
    pygame.display.update()
    j += 1

class Button():
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    DISPLAYSURF.blit(picture, self.rect)
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

class HealthBar():
  def __init__(self,x,y):
    self.position = x,y
    self.negDimensions = (250,10)
    self.posDimensions = [250,10]
  def drawRects(self):
    pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
    pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
    pygame.display.update()
  def updateBar(self, target):
    maxHealth = target.maxhp
    currentHealth = target.hp
    healthProportion = int(currentHealth)/float(maxHealth)
    newDimension = healthProportion*self.negDimensions[0]
    self.posDimensions[0] = newDimension

def normalMode(): #일반 모드(일반공격, 크리티컬공격, 힐)버튼 셋
  testbuttonImg = pygame.image.load("Image/buttonImg.png")

  NAButton = Button() #일반공격버튼
  NAButton.assignImage(testbuttonImg)
  NAButton.setCoords(buttonGrid[0][0], buttonGrid[0][1])
  CAButton = Button() #크리티컬공격버튼
  CAButton.assignImage(testbuttonImg)
  CAButton.setCoords(buttonGrid[1][0], buttonGrid[1][1])
  HButton = Button() #힐버튼
  HButton.assignImage(testbuttonImg)
  HButton.setCoords(buttonGrid[2][0], buttonGrid[2][1])
  SButton = Button() #특수능력버튼
  SButton.assignImage(testbuttonImg)
  SButton.setCoords(buttonGrid[3][0], buttonGrid[3][1])

  NAButton.drawButton(testbuttonImg)
  CAButton.drawButton(testbuttonImg)
  HButton.drawButton(testbuttonImg)
  SButton.drawButton(testbuttonImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

def specialMode(): #특수 공격(4번버튼 누를시 실행) 버튼 셋 및 특수공격 실행
  specialButtonImg = pygame.image.load("Image/buttonImg2.png")

  s1Button = Button() #일반공격버튼
  s1Button.assignImage(specialButtonImg)
  s1Button.setCoords(buttonGrid[0][0], buttonGrid[0][1])
  s2Button = Button()
  s2Button.assignImage(specialButtonImg)
  s2Button.setCoords(buttonGrid[1][0], buttonGrid[1][1])
  s3Button = Button()
  s3Button.assignImage(specialButtonImg)
  s3Button.setCoords(buttonGrid[2][0], buttonGrid[2][1])
  s4Button = Button()
  s4Button.assignImage(specialButtonImg)
  s4Button.setCoords(buttonGrid[3][0], buttonGrid[3][1])

  s1Button.drawButton(specialButtonImg)
  s2Button.drawButton(specialButtonImg)
  s3Button.drawButton(specialButtonImg)
  s4Button.drawButton(specialButtonImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

  picked = 0
  while not picked:
    for event in pygame.event.get(): #running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if s1Button.pressed(mouse) == True:
          #특수능력 1
          picked = 1
        if s2Button.pressed(mouse) == True:
          #특수능력 2
          picked = 1
        if s3Button.pressed(mouse) == True:
          #특수능력 3
          picked = 1
        if s4Button.pressed(mouse) == True:
          #특수능력 4
          picked = 1
    
def displayMessage(target1, target2, actionNum, msg, mode):
  reset = pygame.image.load("Image/reset.png")
  DISPLAYSURF.blit(reset, (30,440))
  if mode == 1: #공격 정보 출력 모드
    action = ['일반공격', '크리티컬공격', '회복']
    animateText(f"[ {target1.name} ] {action[actionNum]} 선택! ", font, TEXTSURF, 50, 500, BLACK)
    animateText(msg, font, TEXTSURF, 50, 520, BLACK)
    pygame.display.update()
    time.sleep(1)
  elif mode == 2: #승패 출력 모드
    #time.sleep(0.5)
    if target1.hp <= 0:
      drawText(f"{target2.name} 이(가) 승리했습니다!",font, TEXTSURF, 50, 500, BLACK)
      pygame.display.update()
      time.sleep(1)
      return True
    elif target2.hp <= 0:
      drawText(f"{target1.name} 이(가) 승리했습니다!",font, TEXTSURF, 50, 500, BLACK)
      pygame.display.update()
      time.sleep(1)
      return True

def displayBar(playerBar, comBar, player, com):
    barReset = pygame.image.load("Image/barNumReset.png")
    DISPLAYSURF.blit(barReset, (400,380))
    DISPLAYSURF.blit(barReset, (100,60))
    playerBar.updateBar(player)
    playerBar.drawRects()
    comBar.updateBar(com)
    comBar.drawRects()

    if player.hp <= 0 or com.hp <= 0:
      if player.hp <= 0: player.hp = 0
      else: com.hp = 0

    drawText(f"{int(player.hp)} / {player.maxhp} ", font, TEXTSURF, 400, 380, BLACK)
    drawText(f"{int(com.hp)} / {com.maxhp} ", font, TEXTSURF, 100, 60, BLACK)
    pygame.display.update()

  

def run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player, com):
    
  background = pygame.image.load("Image/testbackground.png")
  testplayer = pygame.image.load("Image/남캐 뒷모습2.png")
  testcom = pygame.image.load("Image/전여친 빌런2.png")

  DISPLAYSURF.blit(background, (0,0)) #윈도우에 이미지 삽입
  DISPLAYSURF.blit(testplayer, (120,200))
  DISPLAYSURF.blit(testcom, (450,10))

  testbuttonImg = pygame.image.load("Image/buttonImg.png")

  NAButton = Button() #일반공격버튼
  NAButton.assignImage(testbuttonImg)
  NAButton.setCoords(buttonGrid[0][0], buttonGrid[0][1])
  CAButton = Button() #크리티컬공격버튼
  CAButton.assignImage(testbuttonImg)
  CAButton.setCoords(buttonGrid[1][0], buttonGrid[1][1])
  HButton = Button() #힐버튼
  HButton.assignImage(testbuttonImg)
  HButton.setCoords(buttonGrid[2][0], buttonGrid[2][1])
  SButton = Button() #특수능력버튼
  SButton.assignImage(testbuttonImg)
  SButton.setCoords(buttonGrid[3][0], buttonGrid[3][1])

  NAButton.drawButton(testbuttonImg)
  CAButton.drawButton(testbuttonImg)
  HButton.drawButton(testbuttonImg)
  SButton.drawButton(testbuttonImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

  animateText("야생의 전여친이 나타났다! ", font, TEXTSURF, 50, 500, BLACK)
  animateText("공격을 시작하자 ", font, TEXTSURF, 50, 530, BLACK)
  pygame.display.update()

  playerBar = HealthBar(400,370)
  comBar = HealthBar(100,50)
  playerBar.drawRects()
  comBar.drawRects()
  displayBar(playerBar,comBar,player,com)

  while(1):
    #플레이어의 선택
    picked = 0
    while not picked:
      for event in pygame.event.get(): #running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
        if event.type == QUIT: #종료(x)버튼 누르면 창 닫음
          pygame.quit()
          sys.exit()
        elif event.type == MOUSEBUTTONDOWN: #마우스 클릭으로 이벤트 발생
          mouse = pygame.mouse.get_pos()
          if NAButton.pressed(mouse) == True: #일반 공격버튼 누를때
            msg = player.normalAttack(com)
            displayMessage(player, com, 0, msg,1)
            picked = 1
          if CAButton.pressed(mouse) == True: #크리티컬 공격버튼 누를때
            msg = player.criticalAttack(com)
            displayMessage(player, com, 1, msg,1)
            picked = 1
          if HButton.pressed(mouse) == True: #회복버튼 누를때
            msg = player.heal()
            displayMessage(player, com, 2, msg,1)
            picked = 1
          if SButton.pressed(mouse) == True: #특수버튼 누를때
            specialMode()
            normalMode()
            picked = 1
    displayBar(playerBar,comBar,player,com)

    #승패판단
    if displayMessage(player, com, None, None,2): break

    #컴 선택
    actionNum, msg = com.action_ai(player)
    displayMessage(com, player, actionNum, msg, 1)

    displayBar(playerBar,comBar,player,com)
    
    #승패판단
    if displayMessage(player, com, None, None,2): break 

if __name__ == '__main__':
  #환경변수 세팅
  pygame.init()
  DISPLAYSURF = pygame.display.set_mode((700, 700)) #이미지 윈도우
  TEXTSURF = pygame.display.set_mode((700,700)) #텍스트 윈도우
  pygame.display.set_caption('Bokhakmon') #윈도우 이름
  fpsClock = pygame.time.Clock()
  FPS = 20
  font = pygame.font.SysFont('휴먼모음t', 20)
  #플레이어 및 컴퓨터 능력치 설정
  player = Person("익현", "남", 500, 50, 70, 1000)
  com = Com("전여자친구", "여", 200, 50, 50, 2500, [40,40,20])
  #실행
  run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player, com)