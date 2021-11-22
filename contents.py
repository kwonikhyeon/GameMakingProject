import random

class Person: #플레이어와 AI에게 공통적으로 들어가는 요소들을 담은 클래스
    def __init__(self, name, sex, att, defence, luck, maxhp):
        self.name = name
        self.sex = sex
        self.att = att
        self.defence = defence
        self.luck = luck
        self.maxhp = maxhp
        self.hp = maxhp
        
    def normalAttack(self, target): #일반공격
        if random.randint(1,10) in range(1,10): #90% 확률로 일반공격 성공
            if self.att >= target.defence: #내 공격력이 상대 방어력보다 높아야 공격가능
                dmg = self.att - target.defence
                target.hp -= dmg
                return f"일반공격 성공! 데미지 {int(dmg)} ", dmg
            else:
                return "공격이 무시되었습니다. ", 0
        else:
            return "일반 공격을 실패했습니다. ", 0

    def criticalAttack(self, target): #크리티컬공격
        if random.randint(1,100) in range(1,self.luck-11): #(luck-10)% 확률로 크리티컬 공격 성공
            if self.att*3 >= target.defence: #내 공격력이 상대 방어력보다 높아야 공격가능
                dmg = self.att*3 - target.defence
                target.hp -= dmg
                return f"크리티컬 공격 성공! 데미지 {int(dmg)} ", dmg
            else:
                return "공격이 무시되었습니다. ", 0
        else:
            return "크리티컬 공격을 실패했습니다. ", 0

    def heal(self): #회복
        self.hp += self.hp*0.3 #현재 체력의 30%만큼 회복
        if self.hp >= self.maxhp:
            self.hp = self.maxhp
            return "체력이 가득 찼습니다! "
        return f"체력이 {int(self.hp*0.3)} 회복되었습니다. "

class Player(Person): #플레이어 클래스(특수능력과 이를 이용하기 위한 변수 추가)
    def __init__(self, name, sex, att, defence, luck, maxhp):
        super().__init__(name, sex, att, defence, luck, maxhp)
        self.coin = 40
        self.level = 1
        self.skill = [0,1,1,3,3] #스킬 레벨(상점에서 올릴수 있음)
        self.item = [0,0,0,0,0]
        self.poisonTurn = 0

    def poison(self, target, mode): #독 공격(스킬레벨 인덱스 0)
        if mode == 0:
            if self.skill[0] == 0:
                return "", False, False
            if self.poisonTurn > 0:
                return "이미 독에 중독되어있습니다. ", True, True
            return "상대방이 독에 중독되었습니다. ", True, True
        
        percent = [0,0.05,0.07,0.1] #스킬레벨이 증가할수록 피해량 증가
        if mode == 1:
            if self.poisonTurn == 3:
                self.poisonTurn = 0
                return "", False
            target.hp -= target.maxhp*percent[self.skill[0]]
            self.poisonTurn += 1
            return f"독 데미지 {int(target.maxhp*percent[self.skill[0]])} ", True

    def def_decrease(self, target): #방어력 감소(스킬레벨 인덱스 1)
        if self.skill[1] == 0:
            return "", False
        percent = [0,0.1,0.3,0.5] #스킬레벨이 증가할수록 감소량 증가
        target.defence -= target.defence*percent[self.skill[1]]
        return f"상대 방어력 {100*percent[self.skill[1]]}% 감소! ", True

    def att_decrease(self, target): #공격력 감소(스킬레벨 인덱스 2)
        if self.skill[2] == 0:
            return "", False
        percent = [0,0.1,0.2,0.3] #스킬레벨이 증가할수록 감소량 증가
        target.att -= target.att*percent[self.skill[2]]
        return f"상대 공격력 {100*percent[self.skill[2]]}% 감소! ", True

    def reflect(self, target, targetDmg): #반사(스킬레벨 인덱스 3)
        if self.skill[3] == 0:
            return "", False
        percent = [0,0.5,0.75,1] #스킬레벨이 증가할수록 성공확률 증가
        if random.random() < percent[self.skill[3]]:
            self.hp += targetDmg
            if self.hp >= self.maxhp: self.hp = self.maxhp
            dmg = targetDmg - target.defence
            target.hp -= dmg
            return f"반사 성공! 체력 회복! 데미지 {int(dmg)} ", True
        else: return "반사를 실패했습니다.. ", True

    def absoluteAtt(self, target): #방어력 무시 공격(스킬레벨 인덱스 4)
        if self.skill[4] == 0:
            return "", False
        percent = [0,0.2,0.3,0.5] #스킬레벨이 증가할수록 피해량 증가
        dmg = target.hp*percent[self.skill[4]]
        target.hp -= dmg
        return f"방어력 무시! 데미지 {int(dmg)} ", True


class Com(Person): #AI클래스
    def __init__(self, name, sex, att, defence, luck, maxhp, pos): #pos는 특성을 나타냄([일반공격, 크리티컬 공격, 회복])
        super().__init__(name, sex, att, defence, luck, maxhp)
        self.pos = pos

        total = 0
        for p in pos: #특성 표준화 ex) pos = [20,30,50]이라면 [20/100,30/100,50/100]으로 표준화 시킨 후 랜덤값으로 이를 추출하기 위해
            total += p 
        self.pos = [p / total for p in pos]
        for i in range(1, len(self.pos)):
            self.pos[i] += self.pos[i - 1] #현재 인덱스의 값에다가 이전 인덱스의 값을 추가 ex) pos = [0.2,0.3,0.5]라면 [0.2,0.5,1]로 변환

    def action_ai(self, target): #변환한 특성값을 통해 랜덤으로 기술 선택
        p = random.random()
        #회복
        if p > self.pos[1]:
            actionNum = 2
            msg = self.heal()
            dmg = 0
        #크리티컬
        elif p > self.pos[0]:
            actionNum = 1
            msg, dmg = self.criticalAttack(target)
        #일반공격
        else:
            actionNum = 0
            msg, dmg = self.normalAttack(target)
        return actionNum, msg, dmg
