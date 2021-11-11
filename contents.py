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
            else:
                print("공격이 무시되었습니다.")
        else:
            print("일반 공격을 실패했습니다.")

    def criticalAttack(self, target): #크리티컬공격
        if random.randint(1,100) in range(1,self.luck-11): #(luck-10)% 확률로 크리티컬 공격 성공
            if self.att*3 >= target.defence: #내 공격력이 상대 방어력보다 높아야 공격가능
                target.hp -= (self.att*3 - target.defence)
            else:
                print("공격이 무시되었습니다.")
        else:
            print("크리티컬 공격을 실패했습니다.")

    def heal(self):
        self.hp += self.hp*0.25