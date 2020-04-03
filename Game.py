import random
import time
import copy
from Player import Player, Bot
from AI import AI

WAN = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"
TIAO = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"
TONG = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"
ELSE = "🀀🀁🀂🀃🀄🀅🀆"
DICT = dict(zip(WAN + TIAO + TONG + ELSE, range(34)))
BACK = "🀫"


class Game:
    def __init__(self, player_list):
        self.__hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)
        self.__player = player_list
        self.__river = []
        self.has_hu = False
        self.has_gang = False
        self.has_jiagang = False
        self.has_peng = False
        self.has_chi = False
        self.count = 0

    def game(self):
        self.start()
        # 循环摸牌出牌
        self.count = 0
        while not self.has_hu:
            if self.count >= 4:
                self.count -= 4
            if self.draw(self.__player[self.count]):
                if self.has_hu:
                    break
                if self.has_gang or self.has_jiagang:
                    self.has_gang = False
                    self.has_jiagang = False
                    continue
            if self.if_hu_gang_peng_chi(self.count):
                if self.has_hu:
                    break
                if self.has_gang or self.has_peng or self.has_chi:
                    self.has_gang = False
                    self.has_peng = False
                    self.has_chi = False
                    continue
            # TODO 结算算番没写
            self.count += 1
            # 没牌可摸时结束
            if len(self.__hill) == 0:
                self.has_hu = False
                print('========= Game Over =========')

    def draw(self, player):
        # 先摸到牌
        player.hand.append(self.__hill.pop(self.__hill.index(random.choice(self.__hill))))
        self.show()
        # 看一下胡没胡
        if self.if_hu(player):
            print('自摸！')
            self.has_hu = True
            return True
        if self.if_gang(player):
            self.has_gang = True
            self.show()
            # count不变 杠的人再进入到摸牌环节
            return True
        if self.if_jiagang(player):
            self.has_jiagang = True
            self.show()
            # count不变 杠的人再进入到摸牌环节
            return True
        item = player.play()
        self.__river.append(item)
        player.ting(self.get_face_down())
        # 理好牌
        player.sort()
        self.show()
        return False

    def if_hu_gang_peng_chi(self, n):
        li = [0, 1, 2, 3]
        li.remove(n)
        for i in li:
            if self.if_hu(self.__player[i], self.__river[-1]):
                print(f'{self.__player[n].name} 放炮。')
                self.has_hu = True
                return True
        for i in li:
            if self.if_gang(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.show()
                self.has_gang = True
                # 杠完直接摸一张出一张 相当于跳到了杠的人的摸牌环节
                # count 指向杠的人
                self.count = i
                return True
        for i in li:
            if self.if_peng(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.show()
                self.has_peng = True
                # 碰完出一张牌
                item = self.__player[i].play()
                self.__river.append(item)
                self.__player[i].ting(self.get_face_down())
                self.__player[i].sort()
                self.show()
                # count 指向碰的人下家
                self.count = i + 1
                return True
        if n + 1 >= 4:
            n = 0
        else:
            n = n + 1
        if self.if_chi(self.__player[n], self.__river[-1]):
            self.__river.pop(-1)
            self.show()
            self.has_chi = True
            # 吃完出一张牌
            item = self.__player[n].play()
            self.__river.append(item)
            self.__player[n].ting(self.get_face_down())
            self.__player[n].sort()
            self.show()
            # count 指向吃的人下家
            self.count = n + 1
            return True
        return False

    def if_hu(self, player, item=''):
        # 可能自摸
        if player.hu(item):
            return True
        else:
            return False

    def if_gang(self, player, item=''):
        # 可能自己杠
        if player.gang(item):
            return True
        else:
            return False

    def if_jiagang(self, player):
        if player.jiagang():
            return True
        else:
            return False

    def if_peng(self, player, item):
        if player.peng(item):
            return True
        else:
            return False

    def if_chi(self, player, item):
        if player.chi(item):
            return True
        else:
            return False

    def get_face_down(self):
        hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)
        face_up = copy.deepcopy(self.__river)
        li = []
        for i in range(4):
            li.extend(self.__player[i].side)
        for i in li:
            for j in i:
                face_up.extend(j)
        for i in face_up:
            hill.remove(i)
        return hill

    def show(self):
        # TODO 盖牌输出没写
        # 清屏
        print('\x1b[2J\x1b[0;0H')
        # 输出0号玩家的牌
        print('\x1b[26C', end='')
        if len(self.__player[0].side) != 0:
            print('\x1b[2D', end='')
            for i in self.__player[0].side:
                for j in i:
                    print(j, end='')
                    if j != '🀄':
                        print(' ', end='')
                print(' ', end='')
            print('\x1b[4C', end='')
        for i in self.__player[0].hand:
            print(i, end='')
            if i != '🀄':
                print(' ', end='')

        # 空行
        print('\r\x1b[2B')

        # 交替输出1、3号玩家的牌
        def show_line(head, middle, tail):
            if len(head) == 1:
                print(head, end='')
                if head != '🀄':
                    print(' ', end='')
                print(f'\x1b[{17}C', end='')
            else:
                for j in head:
                    print(j, end='')
                    if j != '🀄':
                        print(' ', end='')
                print(f'\x1b[{19 - 2 * len(head)}C', end='')

            if len(middle) > 0:
                for j in range(len(middle)):
                    if middle[j] == '🀄':
                        print(middle[j], end='')
                    else:
                        print(middle[j] + '\x1b[1C', end='')
            print(f'\x1b[{59 - len(middle) * 2}C', end='')
            if len(tail) == 1:
                print(tail)
            else:
                print(f'\x1b[{2 * len(tail) - 2}D', end='')
                for j in tail:
                    print(j, end='')
                    if j != '🀄':
                        print(' ', end='')
                print('\r')

        for i in range(14):
            l1 = len(self.__player[1].hand)
            s1 = len(self.__player[1].side)
            l2 = len(self.__player[3].hand)
            s2 = len(self.__player[3].side)
            if s1 > 0:
                if i < s1:
                    for j in range(s1):
                        if i == j:
                            h = self.__player[1].side[j]
                elif s1 <= i < s1 + 2 or l1 + s1 + 2 <= i:
                    h = ' '
                else:
                    h = self.__player[1].hand[i - 2 - s1]
            else:
                if l1 <= i:
                    h = ' '
                else:
                    h = self.__player[1].hand[i]

            if i >= 5:
                if len(self.__river) > 21:
                    m = self.__river[(i - 5) * 21:(i - 5) * 21 + 21]
                else:
                    m = self.__river[(i - 5) * 21:]
            else:
                m = ''

            if s2 > 0:
                if i > 13 - s2:
                    for j in range(s2):
                        if i == 13 - j:
                            t = self.__player[3].side[j]
                elif 13 - s2 >= i > 11 - s2 or 11 - l2 - s2 >= i:
                    t = ' '
                else:
                    t = self.__player[3].hand[11 - i - s2]
            else:
                if l2 <= 13 - i:
                    t = ' '
                else:
                    t = self.__player[3].hand[13 - i]

            show_line(h, m, t)
        # 空行
        print('\r\x1b[1B')
        # 输出自己的牌
        print('\x1b[26C', end='')
        if self.__player[2].ting_flag:
            print('\x1b[6D⚑\x1b[5C', end='')
        if len(self.__player[2].side) != 0:
            print('\x1b[2D', end='')
            for i in self.__player[2].side:
                for j in i:
                    print(j, end='')
                    if j != '🀄':
                        print(' ', end='')
                print(' ', end='')
            print('\x1b[4C', end='')
        for i in self.__player[2].hand:
            print(i, end='')
            if i != '🀄':
                print(' ', end='')
        print('\r')
        time.sleep(0.5)

    def start(self):
        # 发13张牌
        j = 0
        while j < 13:
            for i in range(4):
                self.__player[i].hand.append(self.__hill.pop(self.__hill.index(random.choice(self.__hill))))
            self.show()
            j += 1
        # 理牌
        for i in range(4):
            self.__player[i].sort()
        self.show()

    def reset(self):
        self.__hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)
        self.__river = []
        self.has_hu = False
        for i in self.__player:
            i.restart()


if __name__ == "__main__":
    gamer_name = input('输入你的名字：')
    p0 = AI('Bot 0')
    p1 = AI('Bot 1')
    p2 = Player(gamer_name)
    p3 = AI('Bot 2')
    game_state = True
    g = Game([p0, p1, p2, p3])
    while game_state:
        g.game()
        flag = input('输入0结束，输入其他继续。')
        if flag == '0':
            game_state = False
        g.reset()
