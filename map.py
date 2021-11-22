import pygame
import run
from contents import *

class Sprite(pygame.sprite.Sprite):
 
    def __init__(self, image, position, idNum): # 생성자 파라미터로 스프라이트에 사용될 이미지 경로와 스프라이트 초기 위치를 받는다
        pygame.sprite.Sprite.__init__(self)
        self.image = image # 스프라이트에 사용될 이미지를 저장할 사용자 변수
        self.position = position # 스프라이트의 위치를 저장할 사용자 변수
        self.rotation = 0 # 스프라이트의 회전 각도를 저장할 사용자 변수
        self.idNum = idNum # 고유번호, 오브젝트마다 다 다르게, 방번호
        #고유번호 = 플레이어:0  
    def update(self): # 스프라이트의 상태를 업데이트 하는 함수. 필요에 따라 파라미터가 추가될 수도 있다.
        # 출력에 사용될 이미지, 위치를 정한다
        self.image = pygame.transform.rotate(self.image, self.rotation) # 이미지를 회전 각도 만큼 회전시킨다
        self.rect = self.image.get_rect()
        self.rect.center = self.position # 이미지의 출력 위치를 정한다


def background_init(initialBackground):
    clock = pygame.time.Clock()
    screen_width = 700 # 가로 크기
    screen_height = 700 # 세로 크기
    screen = pygame.display.set_mode((screen_width, screen_height))
    # 화면 타이틀(제목) 설정
    pygame.display.set_caption("Welcome! Bohak Monster.")
    # FPS 초당 프레임 변수 설정
    clock = pygame.time.Clock()

    screen.blit(initialBackground, (0, 0)) # 배경 그리기(background 가 표시되는 위치)
    pygame.display.update()
    return screen, clock


def room(player, screen, background, clock, obj):
    screenSize = screen.get_rect().size
    characterRect = player.image.get_rect()
    characterSize = characterRect.size

    objRect = []
    for i in range(len(obj)):
        obj[i].update()
        objRect.append(obj[i].image.get_rect())
        objRect[i].center = obj[i].position 

    # 이동할 좌표
    to_x = 0
    to_y = 0
    # 이동 속도
    character_speed = 0.5
    # 이벤트 루프
    running = True # 게임이 진행중인지 확인하기
    while running:
        dt = clock.tick(60) # 게임화면의 초당 프레임 수 설정

        for event in pygame.event.get(): # running 중 키보드나,마우스 입력값(이벤트)을 체크해주는것
            if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는지
                pygame.quit()
                running = False # 게임이 진행중이 아님

            if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
                if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                    to_x -= character_speed # -5만큼
                elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                    to_x += character_speed
                elif event.key == pygame.K_UP: # 캐릭터를 위로
                    to_y -= character_speed
                elif event.key == pygame.K_DOWN: # 캐릭터를 아래로
                    to_y += character_speed

            if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    to_y = 0

        player.position[0] += to_x * dt # 캐릭터의 포지션을 x만큼 실제 움직임 프레임수(dt)만큼 곱해서
        player.position[1] += to_y * dt # 캐릭터의 포지션을 x만큼 실제 움직임

        characterRect.center = player.position
        
        # X 경계값 설정
        if player.position[0] < 0:
            player.position[0] = 0
        elif player.position[0] > screenSize[0] - characterSize[0]:
            player.position[0] = screenSize[0] - characterSize[0]
        # Y 경계값 설정
        if player.position[1] < 110:
            player.position[1] = 110
        elif player.position[1] > 540:
            player.position[1] = 540

        # 충돌 체크 및 이벤트 설정
        for i in range(len(obj)):
            if characterRect.colliderect(objRect[i]):       
                if obj[i].idNum == 1 or obj[i].idNum == 2 or obj[i].idNum == 3:
                    return obj[i].idNum
                elif obj[i].idNum == 4: #보스 이미지 고유번호
                    print('보스와 싸움!')
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, com)
                    player.position = [obj[i].position[0]-100,obj[i].position[1]]

        # 캐릭터 및 오브젝트 삽입
        screen.blit(background, (0, 0))
        screen.blit(player.image, tuple(player.position))
        for i in range(len(obj)):
            screen.blit(obj[i].image, tuple(obj[i].position))
        pygame.display.update()

        
        

if __name__ == '__main__':
    pygame.init()

    #배경 이미지 불러오기
    mainBackGround = pygame.image.load("mapImage/stage.jpg")
    BackGround1 = pygame.image.load("mapImage/testB1.jpg")
    BackGround2 = pygame.image.load("mapImage/testbackground.jpg")

    #화면 초기화
    screen, clock = background_init(mainBackGround)

    #요소(스프라이트)이미지 불러오기
    playerImg = pygame.transform.rotozoom(pygame.image.load("mapImage/character.png"),0 ,0.2) 
    portalImg = pygame.transform.rotozoom(pygame.image.load("mapImage/reset.png"),0 ,0.05)

    
    #요소(스프라이트)생성
    player = Sprite(playerImg, [200,350], 0) #(이미지, 초기좌표)
    portal1 = Sprite(portalImg, [650,300], 2) #보스로 가는문
    portal2 = Sprite(portalImg, [70,200], 3) #상점으로 가는문
    portal3 = Sprite(portalImg, [20, 350], 1) #보스룸에서 돌아오는문
    portal4 = Sprite(portalImg, [200, 580], 1) #상점에서 돌아오는문
    boss = Sprite(portalImg, [500, 350], 4) #보스


    room1Obj = [portal1, portal2]
    room2Obj = [portal3, boss]
    room3Obj = [portal4]

    #####################################################################################
    DISPLAYSURF = pygame.display.set_mode((700, 700)) #이미지 윈도우
    TEXTSURF = pygame.display.set_mode((700,700)) #텍스트 윈도우
    pygame.display.set_caption('Bokhakmon') #윈도우 이름
    fpsClock = pygame.time.Clock()
    FPS = 20
    font = pygame.font.SysFont('휴먼모음t', 20)
    #플레이어 및 컴퓨터 능력치 설정
    gamePlayer = Player("익현", "남", 500, 50, 70, 1000) #기본값 200,50,50,500 1스텟씩 올릴때마다 50,20,7,100씩 증가
    com = Com("전여자친구", "여", 200, 50, 50, 2500, [40,40,20])
    #####################################################################################

    #시작지점(메인룸)
    moveTo = 1
    while True:
        if moveTo == 1: #메인룸
            moveTo = room(player, screen, mainBackGround, clock, room1Obj)
        elif moveTo == 2: #보스룸
            player.position = [85,300]
            moveTo = room(player, screen, BackGround1, clock, room2Obj)
            player.position = [600,300]
        elif moveTo == 3: #상점
            player.position = [70,600]
            moveTo = room(player, screen, BackGround2, clock, room3Obj)
            player.position = [70,250]
        
