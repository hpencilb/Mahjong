import random
import time
from Player import Player, Bot

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
        self.has_peng = False
        self.has_chi = False
        self.count = 0

    def game(self):
        self.start()
        self.has_hu = True
        # 循环摸牌出牌
        self.count = 0
        while self.has_hu:
            if self.count >= 4:
                self.count -= 4
            # TODO 听牌检测没写
            if self.draw(self.__player[self.count]):
                # 自摸
                break
            if self.if_hu_gang_peng_chi(self.count):
                if not self.has_hu:
                    break
                if self.has_gang:
                    self.has_gang = False
                    continue
                if self.has_peng:
                    self.has_peng = False
                    continue
                if self.has_chi:
                    self.has_chi = False
                    continue
            # TODO 结算算番没写
            self.count += 1
            # 没牌可摸时结束
            if len(self.__hill) == 0:
                self.has_hu = False
                print('========= Game Over =========')

    def if_hu(self, player, item=''):
        if player.hu(item):
            return True
        else:
            return False

    def if_gang(self, player, item):
        if player.gang(item):
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

    def if_hu_gang_peng_chi(self, n):
        li = [0, 1, 2, 3]
        li.remove(n)
        for i in li:
            if self.if_hu(self.__player[i], self.__river[-1]):
                print(f'{self.__player[n].name} 放炮。')
                self.has_hu = False
                return True
        for i in li:
            if self.if_gang(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.has_gang = True
                self.count = i
                return True
        for i in li:
            if self.if_peng(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.show()
                self.has_peng = True
                item = self.__player[i].play()
                self.__river.append(item)
                self.__player[i].sort()
                self.show()
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
            item = self.__player[n].play()
            self.__river.append(item)
            self.__player[n].sort()
            self.show()
            self.count = n + 1
            return True
        return False

    def draw(self, player):
        # 先摸到牌
        player.hand.append(self.__hill.pop(self.__hill.index(random.choice(self.__hill))))
        self.show()
        # 看一下胡没胡
        if self.if_hu(player):
            print('自摸！')
            self.has_hu = False
            return True
        # TODO 主动杠加杠没写
        item = player.play()
        self.__river.append(item)
        # 理好牌
        player.sort()
        self.show()
        return False

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
        for i in self.__player:
            i.restart()


if __name__ == "__main__":
    gamer_name = input('输入你的名字：')
    p0 = Bot('Bot 0')
    p1 = Bot('Bot 1')
    p2 = Player(gamer_name)
    p3 = Bot('Bot 2')
    game_state = True
    g = Game([p0, p1, p2, p3])
    while game_state:
        g.game()
        flag = input('输入0结束，输入其他继续。')
        if flag == '0':
            game_state = False
        g.reset()
