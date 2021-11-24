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
sbuttonGrid = [[400, 440],[540,440],[400, 520],[540,520],[400,600],[540,600]]

def drawText(text, font, surface, x, y, color): #텍스트 한번에 띄우기
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

def animateText(fpsClock, FPS, text, font, surface, x, y, color): #텍스트 한글자씩 띄우기
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

class Button(): #버튼 이미지 및 누름 감지에 대한 속성을 담은 클래스
  def __init__(self, DISPLAYSURF):
      self.DISPLAYSURF = DISPLAYSURF
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    self.DISPLAYSURF.blit(picture, self.rect)
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

class HealthBar(): #체력 바 클래스
  def __init__(self,DISPLAYSURF,x,y):
    self.position = x,y
    self.negDimensions = (250,10)
    self.posDimensions = [250,10]
    self.DISPLAYSURF = DISPLAYSURF
  def drawRects(self):
    pygame.draw.rect(self.DISPLAYSURF, RED, (self.position, self.negDimensions))
    pygame.draw.rect(self.DISPLAYSURF, GREEN, (self.position, self.posDimensions))
    pygame.display.update()
  def updateBar(self, target):
    maxHealth = target.maxhp
    currentHealth = target.hp
    healthProportion = int(currentHealth)/float(maxHealth)
    newDimension = healthProportion*self.negDimensions[0]
    self.posDimensions[0] = newDimension

def normalMode(DISPLAYSURF): #일반 모드(일반공격, 크리티컬공격, 힐)버튼 셋
  buttonResetImg = pygame.image.load("Image/buttonReset.png")
  DISPLAYSURF.blit(buttonResetImg, (400,440))

  NAButtonImg = pygame.image.load("Image/일반공격버튼.png")
  CAButtonImg = pygame.image.load("Image/크리티컬공격버튼.png")
  HButtonImg = pygame.image.load("Image/회복버튼.png")
  SButtonImg = pygame.image.load("Image/특수능력버튼.png")

  NAButton = Button(DISPLAYSURF) #일반공격버튼
  NAButton.assignImage(NAButtonImg)
  NAButton.setCoords(buttonGrid[0][0], buttonGrid[0][1])
  CAButton = Button(DISPLAYSURF) #크리티컬공격버튼
  CAButton.assignImage(CAButtonImg)
  CAButton.setCoords(buttonGrid[1][0], buttonGrid[1][1])
  HButton = Button(DISPLAYSURF) #힐버튼
  HButton.assignImage(HButtonImg)
  HButton.setCoords(buttonGrid[2][0], buttonGrid[2][1])
  SButton = Button(DISPLAYSURF) #특수능력버튼
  SButton.assignImage(SButtonImg)
  SButton.setCoords(buttonGrid[3][0], buttonGrid[3][1])

  NAButton.drawButton(NAButtonImg)
  CAButton.drawButton(CAButtonImg)
  HButton.drawButton(HButtonImg)
  SButton.drawButton(SButtonImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

def specialMode(DISPLAYSURF, FPS, fpsClock, font, TEXTSURF, player, target, dmg, poison): #특수 공격(4번버튼 누를시 실행) 버튼 셋 및 특수공격 실행
  PosisonAttackImg = pygame.image.load("Image/독 공격 버튼.png")
  DecreaseAttackPowerImg = pygame.image.load("Image/공격력 감소 버튼.png")
  DecreaseDefenceImg = pygame.image.load("Image/방어력 감소 버튼.png")
  reflectionImg = pygame.image.load("Image/반사 버튼.png")
  DefenseIgnoreAttackImg = pygame.image.load("Image/방어력 무시 공격 버튼.png")
  GoBackImg = pygame.image.load("Image/돌아가기 버튼.png")
  buttonResetImg = pygame.image.load("Image/buttonReset.png")
  DISPLAYSURF.blit(buttonResetImg, (400,440))

  s1Button = Button(DISPLAYSURF) #특수능력버튼 6개
  s1Button.assignImage(PosisonAttackImg)
  s1Button.setCoords(sbuttonGrid[0][0], sbuttonGrid[0][1])
  s2Button = Button(DISPLAYSURF)
  s2Button.assignImage(DecreaseDefenceImg)
  s2Button.setCoords(sbuttonGrid[1][0], sbuttonGrid[1][1])
  s3Button = Button(DISPLAYSURF)
  s3Button.assignImage(DecreaseAttackPowerImg)
  s3Button.setCoords(sbuttonGrid[2][0], sbuttonGrid[2][1])
  s4Button = Button(DISPLAYSURF)
  s4Button.assignImage(reflectionImg)
  s4Button.setCoords(sbuttonGrid[3][0], sbuttonGrid[3][1])
  s5Button = Button(DISPLAYSURF)
  s5Button.assignImage(DefenseIgnoreAttackImg)
  s5Button.setCoords(sbuttonGrid[4][0], sbuttonGrid[4][1])
  s6Button = Button(DISPLAYSURF)
  s6Button.assignImage(GoBackImg)
  s6Button.setCoords(sbuttonGrid[5][0], sbuttonGrid[5][1])

  s1Button.drawButton(PosisonAttackImg)
  s2Button.drawButton(DecreaseDefenceImg)
  s3Button.drawButton(DecreaseAttackPowerImg)
  s4Button.drawButton(reflectionImg)
  s5Button.drawButton(DefenseIgnoreAttackImg)
  s6Button.drawButton(GoBackImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

  cancel = 0
  picked = 0
  sNum = 0
  
  while not picked:
    for event in pygame.event.get(): #running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if s1Button.pressed(mouse) == True:
          #특수능력 1
          msg, did, poison = player.poison(target, 0)
          if did == False:
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, target, None, "아직 배우지 않은 기술입니다.",3) 
            continue
          sNum = 3
          picked = 1
        if s2Button.pressed(mouse) == True:
          #특수능력 2 방어력 감소
          msg, did = player.def_decrease(target)
          if did == False: 
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, target, None, "아직 배우지 않은 기술입니다.",3) 
            continue
          sNum = 4
          picked = 1 
        if s3Button.pressed(mouse) == True:
          #특수능력 3 공격력 감소
          msg, did = player.att_decrease(target)
          if did == False:
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, target, None, "아직 배우지 않은 기술입니다.",3)  
            continue
          sNum = 5
          picked = 1
        if s4Button.pressed(mouse) == True:
          #특수능력 4 반사
          msg, did = player.reflect(target, dmg)
          if did == False:
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, target, None, "아직 배우지 않은 기술입니다.",3)  
            continue
          sNum = 6
          picked = 1
        if s5Button.pressed(mouse) == True:
          #특수능력 5 방어력무시 딜
          msg, did = player.absoluteAtt(target)
          if did == False: 
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, target, None, "아직 배우지 않은 기술입니다.",3) 
            continue
          sNum = 7
          picked = 1
        if s6Button.pressed(mouse) == True:
          #돌아가기
          msg = None
          cancel = 1
          picked = 1
  return cancel, msg, sNum, poison
    
def displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,target1, target2, actionNum, msg, mode): #저장해놓은 형식의 텍스트 출력
  reset = pygame.image.load("Image/reset.png")
  DISPLAYSURF.blit(reset, (30,440))
  if mode == 1: #공격 정보 출력 모드
    action = ['일반공격', '크리티컬공격', '회복', '독', '상대 방어력 감소', '상대 공격력 감소', '반사', '방어무시공격']
    animateText(fpsClock, FPS, f"[ {target1.name} ] {action[actionNum]} 선택! ", font, TEXTSURF, 50, 500, BLACK)
    animateText(fpsClock, FPS, msg, font, TEXTSURF, 50, 520, BLACK)
    pygame.display.update()
    time.sleep(1)

  elif mode == 2: #승패 출력 모드
    if target1.hp <= 0: #플레이어 패배
      drawText(f"{target2.name} 이(가) 승리했습니다!",font, TEXTSURF, 50, 500, BLACK)
      win = False
      pygame.display.update()
      time.sleep(1)
      return True, win
    elif target2.hp <= 0: #플레이어 승리
      drawText(f"{target1.name} 이(가) 승리했습니다!",font, TEXTSURF, 50, 500, BLACK)
      win = True
      pygame.display.update()
      time.sleep(1)
      return True, win
    else: return False, False

  elif mode == 3: #일반 출력모드
    animateText(fpsClock, FPS, msg, font, TEXTSURF, 50, 500, BLACK)
    pygame.display.update()
    time.sleep(1)

def displayBar(DISPLAYSURF,font, TEXTSURF,playerBar, comBar, player, com):
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

  drawText(f"{int(player.hp)}/{player.maxhp} ", font, TEXTSURF, 400, 380, WHITE)
  drawText(f"{int(com.hp)}/{com.maxhp} ", font, TEXTSURF, 100, 60, WHITE)
  pygame.display.update()

def movie(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player, com):
  player_image=pygame.image.load("Image/남캐.png")
  text_bar=pygame.image.load("Image/textbar.png")
  if com.name == '밥무새 신입생' :
    com_image=pygame.image.load("Image/신입생 빌런.png")
    movie_background=pygame.image.load("Image/1_background.png")
  elif com.name == '라이벌 동기' :
    com_image=pygame.image.load("Image/라이벌 빌런.png")
    movie_background=pygame.image.load("Image/2_background.png")
  elif com.name == '꼰대 선배' :
    com_image=pygame.image.load("Image/복학생 빌런.png")
    movie_background=pygame.image.load("Image/3_background.png")
  elif com.name == '전 여자친구' :
    com_image=pygame.image.load("Image/전여친 빌런.png")
    movie_background=pygame.image.load("Image/4_background.png")
  elif com.name == 'F폭격기 교수님' :
    com_image=pygame.image.load("Image/f교수빌런.png")
    movie_background=pygame.image.load("Image/5_background.png")
  elif com.name == '연구실 교수님':
    com_image=pygame.image.load("Image/보스.png")
    movie_background=pygame.image.load("Image/6_background.png")
  
  DISPLAYSURF.blit(movie_background, (0,0))
  DISPLAYSURF.blit(player_image, (0,250))
  DISPLAYSURF.blit(com_image, (430,250))
  DISPLAYSURF.blit(text_bar, (0,500))

  if com.name == '밥무새 신입생' :
    story1(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)
  elif com.name == '라이벌 동기':
    story2(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)
  elif com.name == '꼰대 선배':
    story3(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)
  elif com.name == '전 여자친구':
    story4(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)
  elif com.name == 'F폭격기 교수님':
    story5(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)
  elif com.name == '연구실 교수님':
    story6(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF)    

def storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, msg, talkgrid):
  animateText(fpsClock, FPS, msg, font, TEXTSURF, talkgrid[0], talkgrid[1], BLACK)
  text_bar=pygame.image.load("Image/textbar.png")
  next = 0
  while next == 0:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        next = 1
  DISPLAYSURF.blit(text_bar, (0,500))

def story1(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "안녕하십니까 선배님!  ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "밥사주세요!! ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "어 그래 우리 새내기 김덕자 아니야  ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "밥사주세요!!!! ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "..... ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "밥사주세요!!!!!!!!!!!! ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 싸울까...??? ) ", [20, 500])

def story2(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "안녕, 인공아 오랜만에 보네 ", [430, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "요새도 공부만 하느라 도서관에만 사니?? ", [390, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "어 그래... 준성아 너는 어떤데?? ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "난 내가 하고싶은거 다 하는편이야 ", [400,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "그런데도 너랑 1등수 밖에 차이 안나잖아 ", [370,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "너도 편하게 살아 ~ ~ ~ ~ ~ ~ ~ ", [400,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 싸울까...??? ) ", [20, 500])
      
def story3(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "선배님 안녕하십니까 (_ _) ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "인공이 ~ 내가 제일 좋아하는 후배 인공이 ~ ", [330, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "여자 소개좀 시켜주라 ...ㅎㅎㅎ  ", [380,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "네...??? ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "여자 소개좀...ㅎㅎㅎㅎ ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "........", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "여소좀...ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ ", [360, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ ", [360, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 싸울까...??? ) ", [20, 500])
  

def story4(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 앗... 1학기때 헤어진 전여친이다....) ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 어떻게 대해야 하지....??) ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "( 전 여친이랑 눈 마주침 )  ", [250,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " ............  ", [530, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " ............  ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " ............  ", [530, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " ..........아..안녕..?  ", [20, 500])


def story5(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 인공학생...? ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 네 교수님! ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 저번주 출석을 하지않았더군...  ", [380,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 아 그 코로나 접종을 한다고 출석으...ㄹ  ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 자네는 F일세  ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "네...????? ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 자네는 F일세 ", [500, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "ㅈ..저..교수님 그게 아니라...", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 아니면 D+이 좋은가??? ", [470, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, "........................", [20, 500])

def story6(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF):
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 여기까지 오다니 대단한 학생이군...  ", [380, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 하지만 순순히 졸업시켜주지는 않을걸세!!  ", [380, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 저도 순순히 돌아갈 생각 없습니다 ! ", [20,500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 졸업시켜 주십시오 !!!! ", [20, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 내년에 졸업하게!!!  ", [480, 500])
  storyNext(fpsClock, FPS,DISPLAYSURF,font,TEXTSURF, " 졸업!!시켜 주십시오 !!!!!! ", [20, 500])


def run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player, com):
  
  movie(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player, com) #초반 스토리
  
  if com.name == '체온측정 도우미':
    background = pygame.image.load("Image/튜토리얼 맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/튜토리얼 빌런.png") 
  elif com.name == '연구실 교수님':
    background = pygame.image.load("Image/보스 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/보스.png") 
  elif com.name == '밥무새 신입생':
    background = pygame.image.load("Image/신입생 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/신입생 빌런.png") 
  elif com.name == '라이벌 동기':
    background = pygame.image.load("Image/라이벌 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/라이벌 빌런.png")
  elif com.name == '꼰대 선배':
    background = pygame.image.load("Image/복학생 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/복학생 빌런.png") 
  elif com.name == '전 여자친구':
    background = pygame.image.load("Image/전애인 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/전여친 빌런.png") 
  elif com.name == 'F폭격기 교수님':
    background = pygame.image.load("Image/F교수 대전맵.png")
    playerImg = pygame.image.load("Image/남캐 뒷모습2.png")
    comImg = pygame.image.load("Image/f교수빌런.png")  

  DISPLAYSURF.blit(background, (0,0)) #윈도우에 이미지 삽입
  DISPLAYSURF.blit(playerImg, (130,180))
  DISPLAYSURF.blit(comImg, (430,110))

  NAButtonImg = pygame.image.load("Image/일반공격버튼.png")
  CAButtonImg = pygame.image.load("Image/크리티컬공격버튼.png")
  HButtonImg = pygame.image.load("Image/회복버튼.png")
  SButtonImg = pygame.image.load("Image/특수능력버튼.png")

  NAButton = Button(DISPLAYSURF) #일반공격버튼
  NAButton.assignImage(NAButtonImg)
  NAButton.setCoords(buttonGrid[0][0], buttonGrid[0][1])
  CAButton = Button(DISPLAYSURF) #크리티컬공격버튼
  CAButton.assignImage(CAButtonImg)
  CAButton.setCoords(buttonGrid[1][0], buttonGrid[1][1])
  HButton = Button(DISPLAYSURF) #힐버튼
  HButton.assignImage(HButtonImg)
  HButton.setCoords(buttonGrid[2][0], buttonGrid[2][1])
  SButton = Button(DISPLAYSURF) #특수능력버튼
  SButton.assignImage(SButtonImg)
  SButton.setCoords(buttonGrid[3][0], buttonGrid[3][1])

  NAButton.drawButton(NAButtonImg)
  CAButton.drawButton(CAButtonImg)
  HButton.drawButton(HButtonImg)
  SButton.drawButton(SButtonImg)

  pygame.display.update() #변경된 사항(화면) 업데이트

  animateText(fpsClock,FPS,f"야생의 [{com.name}]이(가) 나타났다! ", font, TEXTSURF, 50, 500, BLACK)
  animateText(fpsClock,FPS,"공격을 시작하자 ", font, TEXTSURF, 50, 530, BLACK)
  pygame.display.update()

  playerBar = HealthBar(DISPLAYSURF,400,370)
  comBar = HealthBar(DISPLAYSURF,100,50)
  playerBar.drawRects()
  comBar.drawRects()
  displayBar(DISPLAYSURF,font, TEXTSURF,playerBar,comBar,player,com)

  #스킬관련 변수
  turn = 0 #독데미지를 입은 턴 수를 저장하는 변수
  cancel = 0 #특수능력버튼을 누른 후 아무것도 선택하지 않고 기본메뉴로 돌아오는 것을 저장하기 위한 변수
  comDmg = 0 #이전에 빌런으로부터 받은 데미지를 저장하는 변수
  poison = False #독 중독 여부를 저장하는 변수
  gameOver = False #게임 끝 여부를 저장하는 변수
  win = False #승패 여부를 저장하는 변수
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
            msg, myDmg = player.normalAttack(com)
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, com, 0, msg,1)
            picked = 1
          if CAButton.pressed(mouse) == True: #크리티컬 공격버튼 누를때
            msg, myDmg = player.criticalAttack(com)
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, com, 1, msg,1)
            picked = 1
          if HButton.pressed(mouse) == True: #회복버튼 누를때
            msg = player.heal()
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, com, 2, msg,1)
            picked = 1
          if SButton.pressed(mouse) == True: #특수버튼 누를때
            cancel, msg , sNum, poison = specialMode(DISPLAYSURF,FPS, fpsClock,font,TEXTSURF,player, com, comDmg, poison)
            normalMode(DISPLAYSURF)
            if cancel == 1: continue
            displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF, player, com, sNum, msg,1)
            picked = 1
    displayBar(DISPLAYSURF,font, TEXTSURF,playerBar,comBar,player,com)
    time.sleep(0.2)
    #독데미지
    if poison == True:
      msg, poison = player.poison(com, 1)
      #글자 디스플레이에 표시하기
      reset = pygame.image.load("Image/reset.png")
      DISPLAYSURF.blit(reset, (30,440))
      animateText(fpsClock,FPS,msg, font, TEXTSURF, 50, 520, BLACK)
      displayBar(DISPLAYSURF,font, TEXTSURF,playerBar,comBar,player,com)
      time.sleep(0.2)

    #승패판단
    gameOver, win = displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, com, None, None,2)
    
    if gameOver == True: 
      player.hp = player.maxhp
      com.hp = com.maxhp
      player.poisonTrun = 0
      if win == True:
        return 'win'
      else:
        return 'lose'

    #컴 선택
    actionNum, msg, comDmg = com.action_ai(player)
    displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,com, player, actionNum, msg, 1)
    displayBar(DISPLAYSURF,font, TEXTSURF,playerBar,comBar,player,com)
    time.sleep(0.2)
    
    #승패판단
    gameOver, win = displayMessage(fpsClock,FPS,DISPLAYSURF,font, TEXTSURF,player, com, None, None,2)
    
    if gameOver == True: 
      player.hp = player.maxhp
      com.hp = com.maxhp
      player.poisonTrun = 0
      if win == True:
        return 'win'
      else:
        return 'lose'

def roulette(player, rank): #랜덤뽑기
  skill = ['독 공격', '상대 방어력 감소', '상대 공격력 감소', '반사', '방어력 무시 공격']
  
  if rank == 'B':
    if player.coin > 50:
      player.coin -= 50
      up = random.randint(0,4)
      if player.skill[up] <= 0: 
        player.skill[up] = 1 #랜덤으로 선택된 특수능력 능력치 up
        return f'{skill[up]} 의 레벨이 1로 변경되었습니다!!  '
      else: return '존재하는 능력치의 능력을 뽑았습니다.  '
    else: return '학점이 부족합니다!  '

  if rank == 'A':
    if player.coin > 100:
      player.coin -= 100
      up = random.randint(0,4)
      if player.skill[up] <= 1: 
        player.skill[up] = 2
        return f'{skill[up]} 의 레벨이 2로 변경되었습니다!!  '
      else: return '존재하는 능력치의 능력을 뽑았습니다.  '
    else: return '학점이 부족합니다!  '

  if rank == 'S':
    if player.coin > 150:
      player.coin -= 150
      up = random.randint(0,4)
      if player.skill[up] <= 2: 
        player.skill[up] = 3
        return f'{skill[up]} 의 레벨이 3으로 변경되었습니다!!  '
      else: return '존재하는 능력치의 능력을 뽑았습니다.  '
    else: return '학점이 부족합니다!  '

def storeRun(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, player):
  storeBackground = pygame.image.load("Image/뽑기 배경.png")
  BbuttonImg = pygame.image.load("Image/B뽑기.png")
  AbuttonImg = pygame.image.load("Image/A뽑기.png")
  SbuttonImg = pygame.image.load("Image/S뽑기.png")
  gradeRemainImg = pygame.image.load("Image/학점 칸.png")
  backImg = pygame.image.load("Image/뒤로가기.png")
  rouletteDisplayImg = pygame.image.load("Image/뽑기 대화창.png")

  DISPLAYSURF.blit(storeBackground, (0,0))
  DISPLAYSURF.blit(gradeRemainImg, (21,21))
  DISPLAYSURF.blit(rouletteDisplayImg, (121,232))

  Bbutton = Button(DISPLAYSURF)
  Bbutton.assignImage(BbuttonImg)
  Bbutton.setCoords(70, 494)
  Bbutton.drawButton(BbuttonImg)
  Abutton = Button(DISPLAYSURF)
  Abutton.assignImage(AbuttonImg)
  Abutton.setCoords(267, 494)
  Abutton.drawButton(AbuttonImg)
  Sbutton = Button(DISPLAYSURF)
  Sbutton.assignImage(SbuttonImg)
  Sbutton.setCoords(465, 494)
  Sbutton.drawButton(SbuttonImg)
  backButton = Button(DISPLAYSURF)
  backButton.assignImage(backImg)
  backButton.setCoords(656,14)
  backButton.drawButton(backImg)

  pygame.display.update()
  drawText(f"{player.coin}",font, TEXTSURF, 100, 37, BLACK)
  drawText(f'현재 능력치는 독, 방.감, 공.감, 반사, 방.무 순으로  ', font, TEXTSURF, 140, 300, BLACK)
  drawText(f'{player.skill} 입니다.  ', font, TEXTSURF, 140, 340, BLACK)
  goBack = False
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
          if Bbutton.pressed(mouse) == True: #B버튼 누를때
            rank = 'B'
            picked = 1
          if Abutton.pressed(mouse) == True: #A버튼 누를때
            rank = 'A'
            picked = 1
          if Sbutton.pressed(mouse) == True: #S버튼 누를때
            rank = 'S'
            picked = 1
          if backButton.pressed(mouse) == True: #뒤로가기 버튼 누를때
            goBack = True
            picked = 1
    
    if goBack: break

    DISPLAYSURF.blit(rouletteDisplayImg, (121,232))
    pygame.display.update()
    msg = roulette(player, rank)
    DISPLAYSURF.blit(gradeRemainImg, (21,21))
    drawText(f"{player.coin}",font, TEXTSURF, 100, 37, BLACK)
    animateText(fpsClock,FPS,msg, font, TEXTSURF, 140, 270, BLACK)
    animateText(fpsClock,FPS,f'현재 능력치는 독, 방.감, 공.감, 반사, 방.무 순으로  ', font, TEXTSURF, 140, 300, BLACK)
    animateText(fpsClock,FPS,f'{player.skill} 입니다.  ', font, TEXTSURF, 140, 330, BLACK)

  
      
def ending(DISPLAYSURF, TEXTSURF, fpsClock, FPS):
  EndingImg = pygame.image.load("mapImage/stage.jpg") #승호 이미지
  EndingButtonImg1 = pygame.image.load("Image/buttonImg.png")
  EndingButtonImg2 = pygame.image.load("Image/buttonImg2.png")

  DISPLAYSURF.blit(EndingImg, (0,0)) #윈도우에 이미지 삽입

  End1Button = Button(DISPLAYSURF) #엔딩1 버튼
  End1Button.assignImage(EndingButtonImg1)
  End1Button.setCoords(100, 350)
  End1Button.drawButton(EndingButtonImg1)

  End2Button = Button(DISPLAYSURF) #엔딩2 버튼
  End2Button.assignImage(EndingButtonImg2)
  End2Button.setCoords(400, 350)
  End2Button.drawButton(EndingButtonImg2)
  
  pygame.display.update()
  running = False

  picked = 0
  while not picked:  
    for event in pygame.event.get(): #running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
      if event.type == QUIT: #종료(x)버튼 누르면 창 닫음
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        EndingImg2 = pygame.image.load("mapImage/testB1.jpg")
        font1 = pygame.font.SysFont('휴먼모음t', 25)
        DISPLAYSURF.blit(EndingImg2, (0,0)) #윈도우에 이미지 삽입

        if End1Button.pressed(mouse) == True: #엔딩1 : 대학원
          animateText(fpsClock, FPS, "그렇게 대학원에서 교수님과 5년을 보냈다고 한다....  ", font1, TEXTSURF, 100, 350, WHITE)
          pygame.display.update()
          time.sleep(0.2)
          picked = 1

        elif End2Button.pressed(mouse) == True: #엔딩2 : 취준
          animateText(fpsClock, FPS, "그렇게 취업준비로 5년을 썼다고 한다;;;;  ", font1, TEXTSURF, 100, 350, WHITE)
          pygame.display.update()
          time.sleep(0.2)
          picked = 1

  return running