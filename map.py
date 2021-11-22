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
    character_speed = 0.3
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
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, boss)
                    player.position = [obj[i].position[0]-100,obj[i].position[1]] #플레이어 위치고정
                elif obj[i].idNum == 5: #학식당아줌마 이미지 고유번호
                    print('랜덤뽑기!')
                    player.position = [obj[i].position[0],obj[i].position[1]+100] #플레이어 위치고정
                elif obj[i].idNum == 6: #신입생 이미지 고유번호
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, newbe)
                    player.position = [obj[i].position[0],obj[i].position[1]+100] #플레이어 위치고정
                elif obj[i].idNum == 7: #라이벌 이미지 고유번호
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, rival)
                    player.position = [obj[i].position[0]-30,obj[i].position[1]-70] #플레이어 위치고정
                elif obj[i].idNum == 8: #복학생 이미지 고유번호
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, elder)
                    player.position = [obj[i].position[0],obj[i].position[1]+100] #플레이어 위치고정
                elif obj[i].idNum == 9: #전여친 이미지 고유번호
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, exgirlfriend)
                    player.position = [obj[i].position[0]-50,obj[i].position[1]-50] #플레이어 위치고정
                elif obj[i].idNum == 10: #F폭격기 교수님 이미지 고유번호
                    run.run(DISPLAYSURF, TEXTSURF, fpsClock, FPS, font, gamePlayer, professorF)
                    player.position = [obj[i].position[0],obj[i].position[1]+100] #플레이어 위치고정
                to_x = 0
                to_y = 0

        # 캐릭터 및 오브젝트 삽입
        screen.blit(background, (0, 0))
        screen.blit(player.image, tuple(player.position))
        for i in range(len(obj)):
            screen.blit(obj[i].image, tuple(obj[i].position))
        pygame.display.update()

        

if __name__ == '__main__':
    pygame.init()

    #배경 이미지 불러오기
    mainBackGround = pygame.image.load("mapImage/stage.jpg") #메인룸 배경
    BackGround1 = pygame.image.load("mapImage/testB1.jpg") #보스룸 배경
    BackGround2 = pygame.image.load("mapImage/학식당 배경.png") #상점 배경

    #화면 초기화
    screen, clock = background_init(mainBackGround)

    #요소(스프라이트)이미지 불러오기
    playerImg = pygame.transform.rotozoom(pygame.image.load("mapImage/character.png"),0 ,0.2) 
    portalImg = pygame.transform.rotozoom(pygame.image.load("mapImage/reset.png"),0 ,0.05)
    newbeImg = pygame.transform.rotozoom(pygame.image.load("mapImage/신입생 빌런.png"),0 ,0.2)  #신입생이미지
    rivalImg = pygame.transform.rotozoom(pygame.image.load("mapImage/라이벌 빌런.png"),0 ,0.2)  #라이벌이미지
    elderImg = pygame.transform.rotozoom(pygame.image.load("mapImage/복학생 빌런.png"),0 ,0.2)  #복학생 선배이미지
    exgirlfriendImg = pygame.transform.rotozoom(pygame.image.load("mapImage/전여친 빌런.png"),0 ,0.2)  #전여친이미지
    professorFImg = pygame.transform.rotozoom(pygame.image.load("mapImage/f교수빌런.png"),0 ,0.2)  #f폭격기 교수님이미지
    haksikImg = pygame.transform.rotozoom(pygame.image.load("mapImage/학식당 아주머니.png"),0 ,0.2)  #학식당 아주머니 이미지


    #요소(스프라이트)생성
    playerSprite = Sprite(playerImg, [200,350], 0) #(이미지, 초기좌표)
    portal1Sprite = Sprite(portalImg, [650,300], 2) #보스로 가는문
    portal2Sprite = Sprite(portalImg, [70,200], 3) #상점으로 가는문
    portal3Sprite = Sprite(portalImg, [20, 350], 1) #보스룸에서 돌아오는문
    portal4Sprite = Sprite(portalImg, [150, 550], 1) #상점에서 돌아오는문
    bossSprite = Sprite(portalImg, [500, 350], 4) #보스
    storeSprite = Sprite(haksikImg, [150,200], 5) #학식당아줌마(능력치 뽑기)
    newbeSprite = Sprite(newbeImg, [175,260], 6) #신입생
    rivalSprite = Sprite(rivalImg, [320,500], 7) #라이벌
    elderSprite = Sprite(elderImg, [355,200], 8) #복학생선배
    exgirlfriendSprite = Sprite(exgirlfriendImg, [540,420], 9) #전여친
    professorFSprite = Sprite(professorFImg, [590,130], 10) #f폭격기교수님
    


    room1Obj = [portal1Sprite, portal2Sprite, newbeSprite, 
                rivalSprite, elderSprite, exgirlfriendSprite, 
                professorFSprite] #메인 맵 스프라이트 그룹
    room2Obj = [portal3Sprite, bossSprite] #보스 맵 스프라이트 그룹
    room3Obj = [portal4Sprite, storeSprite] #상점 맵 스프라이트 그룹

    #####################################################################################
    DISPLAYSURF = pygame.display.set_mode((700, 700)) #이미지 윈도우
    TEXTSURF = pygame.display.set_mode((700,700)) #텍스트 윈도우
    pygame.display.set_caption('Bokhakmon') #윈도우 이름
    fpsClock = pygame.time.Clock()
    FPS = 20
    font = pygame.font.SysFont('휴먼모음t', 20)
    #플레이어 및 컴퓨터 능력치 설정
    gamePlayer = Player("익현", "남", 200, 50, 50, 500) #기본값 200,50,50,500 
    boss = Com("연구실 교수님", "남", 400, 200, 85, 2000, [80,80,50])
    newbe = Com("밥무새 신입생", "여", 100, 40, 60, 500,[40,30,70])
    rival = Com("라이벌 동기", "남", 130, 50, 40, 550,[20,70,30])
    elder = Com("꼰대 선배", "남", 180, 100, 50, 700,[60,20,80])
    exgirlfriend = Com("전 여자친구", "여", 250, 20, 80, 630, [50,50,10])
    professorF = Com("F폭격기 교수님", "남", 330, 80, 30, 1200, [100,30,70])
    #####################################################################################

    #시작지점(메인룸)
    moveTo = 1
    while True:
        if moveTo == 1: #메인룸
            moveTo = room(playerSprite, screen, mainBackGround, clock, room1Obj)
        elif moveTo == 2: #보스룸
            playerSprite.position = [85,320]
            moveTo = room(playerSprite, screen, BackGround1, clock, room2Obj)
            playerSprite.position = [600,300]
        elif moveTo == 3: #상점
            playerSprite.position = [150,470]
            moveTo = room(playerSprite, screen, BackGround2, clock, room3Obj)
            playerSprite.position = [70,250]
        
