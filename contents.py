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
                target.hp -= (self.att - target.defence)
                return f"일반공격 성공! 데미지 {self.att - target.defence} "
            else:
                return "공격이 무시되었습니다. "
        else:
            return "일반 공격을 실패했습니다. "

    def criticalAttack(self, target): #크리티컬공격
        if random.randint(1,100) in range(1,self.luck-11): #(luck-10)% 확률로 크리티컬 공격 성공
            if self.att*3 >= target.defence: #내 공격력이 상대 방어력보다 높아야 공격가능
                target.hp -= (self.att*3 - target.defence)
                return f"크리티컬 공격 성공! 데미지 {self.att*3 - target.defence} "
            else:
                return "공격이 무시되었습니다. "
        else:
            return "크리티컬 공격을 실패했습니다. "

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
        #크리티컬
        elif p > self.pos[0]:
            actionNum = 1
            msg = self.criticalAttack(target)
        #일반공격
        else:
            actionNum = 0
            msg = self.normalAttack(target)
        return actionNum, msg
