import random

class Person:
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

    def heal(self):
        self.hp += self.hp*0.25
        if self.hp >= self.maxhp:
            self.hp = self.maxhp
            return "체력이 가득 찼습니다! "
        return f"체력이 {int(self.hp*0.25)} 회복되었습니다. "

    def state(self):
        print('[', self.name, ']')
        print('체력 : ', int(self.hp), '/', self.maxhp)
        print('공격 / 방어 / 운 : ', self.att, self.defence, self.luck, '\n')

class Player(Person):
    def __init__(self, name, sex, att, defence, luck, maxhp):
        super().__init__(name, sex, att, defence, luck, maxhp)
        self.coin = 40
        self.level = 1
        self.skill = [1,0,0,3,3]
        self.item = [0,0,0,0,0]
        self.poisonTurn = 0

    def poison(self, target, mode):# 미완성
        if mode == 0:
            if self.skill[0] == 0:
                return "", False, False
            if self.poisonTurn > 0:
                return "이미 독에 중독되어있습니다. ", True, True
            return "상대방이 독에 중독되었습니다. ", True, True
        
        percent = [0,0.05,0.07,0.1]
        if mode == 1:
            if self.poisonTurn == 3:
                self.poisonTurn = 0
                return "", False
            target.hp -= target.maxhp*percent[self.skill[0]]
            self.poisonTurn += 1
            return f"독 데미지 {int(target.maxhp*percent[self.skill[0]])} ", True

    def def_decrease(self, target):
        if self.skill[1] == 0:
            return "", False
        percent = [0,0.1,0.3,0.5]
        target.defence -= target.defence*percent[self.skill[1]]
        return f"상대 방어력 {100*percent[self.skill[1]]}% 감소! ", True

    def att_decrease(self, target):
        if self.skill[2] == 0:
            return "", False
        percent = [0,0.1,0.2,0.3]
        target.att -= target.att*percent[self.skill[2]]
        return f"상대 공격력 {100*percent[self.skill[2]]}% 감소! ", True

    def reflect(self, target, targetDmg):
        if self.skill[3] == 0:
            return "", False
        percent = [0,0.5,0.75,1]
        if random.random() < percent[self.skill[3]]:
            self.hp += targetDmg
            if self.hp >= self.maxhp: self.hp = self.maxhp
            dmg = targetDmg - target.defence
            target.hp -= dmg
            return f"반사 성공! 체력 회복! 데미지 {int(dmg)} ", True
        else: return "반사를 실패했습니다.. ", True

    def absoluteAtt(self, target):
        if self.skill[4] == 0:
            return "", False
        percent = [0,0.2,0.3,0.5]
        dmg = target.hp*percent[self.skill[4]]
        target.hp -= dmg
        return f"방어력 무시! 데미지 {int(dmg)} ", True


class Com(Person):
    def __init__(self, name, sex, att, defence, luck, maxhp, pos): #pos는 특성을 나타냄([일반공격, 크리티컬 공격, 회복])
        super().__init__(name, sex, att, defence, luck, maxhp)
        self.pos = pos

        total = 0
        for p in pos:
            total += p
        self.pos = [p / total for p in pos]
        for i in range(1, len(self.pos)):
            self.pos[i] += self.pos[i - 1]

    def action_ai(self, target):
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
