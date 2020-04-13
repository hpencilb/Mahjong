from Player import *
from AI import AI

BACK = "🀫"


class Game:
    def __init__(self, player_list, HIDE=True):
        self.__player = player_list
        self.__hide = HIDE
        self.__info = ''
        self.__hill = Hill()
        self.__river = PaiList()
        self.__public = PaiList()
        self.__count = 0
        self.has_hu = False
        self.has_gang = False
        self.has_jiagang = False
        self.has_peng = False
        self.has_chi = False

    def game(self):
        self.start()
        # 循环摸牌出牌
        while not self.has_hu:
            if self.__count >= 4:
                self.__count -= 4
            if self.draw(self.__player[self.__count]):
                if self.has_hu:
                    break
                if self.has_gang or self.has_jiagang:
                    self.has_gang = False
                    self.has_jiagang = False
                    continue
            if self.if_hu_gang_peng_chi(self.__count):
                if self.has_hu:
                    break
                if self.has_gang or self.has_peng or self.has_chi:
                    self.has_gang = False
                    self.has_peng = False
                    self.has_chi = False
                    continue
            # TODO 结算算番没写
            self.__count += 1
            # 没牌可摸时结束
            if len(self.__hill) == 0:
                self.has_hu = True
                self.__info = '游戏结束，和局。'
        if self.has_hu:
            self.__hide = False
            self.show()
            print(self.__info)

    def draw(self, player):
        # 先摸牌
        player.hand.append(self.__hill.draw())
        self.show()
        # 看一下胡没胡
        if self.if_hu(player):
            self.__info += '自摸！'
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
        player.get_public(self.refresh_public())
        player.riichi()
        # 理好牌
        player.sort()
        self.show()
        return False

    def if_hu_gang_peng_chi(self, n):
        li = [0, 1, 2, 3]
        li.remove(n)
        for i in li:
            if self.if_hu(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.__info += f'{self.__player[n].name} 放铳。'
                self.__player[n].fangchong = True
                self.has_hu = True
                self.__count = i
                return True
        for i in li:
            if self.if_gang(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.show()
                self.has_gang = True
                # 杠完直接摸一张出一张 相当于跳到了杠的人的摸牌环节
                # count 指向杠的人
                self.__count = i
                return True
        for i in li:
            if self.if_peng(self.__player[i], self.__river[-1]):
                self.__river.pop(-1)
                self.show()
                self.has_peng = True
                # 碰完出一张牌
                item = self.__player[i].play()
                self.__river.append(item)
                # count 指向碰的人下家
                self.__count = i + 1
                self.__player[i].get_public(self.refresh_public())
                self.__player[i].riichi()
                self.__player[i].sort()
                self.show()
                # 再检测打出来的牌有没有胡杠碰吃
                self.if_hu_gang_peng_chi(i)
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
            # count 指向吃的人下家
            self.__count = n + 1
            self.__player[n].get_public(self.refresh_public())
            self.__player[n].riichi()
            self.__player[n].sort()
            self.show()
            # 再检测打出来的牌有没有胡杠碰吃
            self.if_hu_gang_peng_chi(n)
            return True
        return False

    def if_hu(self, player, item=None):
        player.get_public(self.refresh_public())
        # 可能自摸
        if player.hu(item):
            self.__info += f'{player.name} 胡啦! '
            return True
        else:
            return False

    def if_gang(self, player, item=None):
        player.get_public(self.refresh_public())
        # 可能自己杠
        if player.gang(item):
            return True
        else:
            return False

    def if_jiagang(self, player):
        player.get_public(self.refresh_public())
        if player.jiagang():
            return True
        else:
            return False

    def if_peng(self, player, item):
        player.get_public(self.refresh_public())
        if player.peng(item):
            return True
        else:
            return False

    def if_chi(self, player, item):
        player.get_public(self.refresh_public())
        if player.chi(item):
            return True
        else:
            return False

    def refresh_public(self):
        self.__public = copy.deepcopy(self.__river)
        li = []
        for i in range(4):
            if self.__player[i].side:
                li.extend(self.__player[i].side)
        if li:
            for i in li:
                self.__public.extend(i)

    def show(self):
        # 清屏
        print('\x1b[2J\x1b[0;0H')
        # 输出0号玩家的牌
        print('\x1b[20C', end='')
        if self.has_hu and self.__count == 0:
            print('♕\x1b[5C', end='')
        elif self.__player[0].fangchong:
            print('💔\x1b[4C', end='')
        else:
            print('\x1b[6C', end='')
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
            if self.__hide:
                print(BACK, end=' ')
            else:
                print(i, end='')
                if i != '🀄':
                    print(' ', end='')
        # 空行
        print('\r')
        if self.has_hu and self.__count == 1:
            print('♕\x1b[1B')
        elif self.__player[1].fangchong:
            print('💔\x1b[1B')
        else:
            print('\x1b[1B')

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
                        print(middle[j], end=' ')
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

        # 交替输出1、3号玩家的牌
        for i in range(14):
            l1 = len(self.__player[1].hand)
            s1 = len(self.__player[1].side)
            l2 = len(self.__player[3].hand)
            s2 = len(self.__player[3].side)
            h, t = ' ', ' '
            if s1 > 0:
                if i < s1:
                    for j in range(s1):
                        if i == j:
                            h = self.__player[1].side[j]
                elif s1 <= i < s1 + 2 or l1 + s1 + 2 <= i:
                    h = ' '
                elif self.__hide:
                    h = BACK
                else:
                    h = self.__player[1].hand[i - 2 - s1]
            else:
                if l1 <= i:
                    h = ' '
                elif self.__hide:
                    h = BACK
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
                elif self.__hide:
                    t = BACK
                else:
                    t = self.__player[3].hand[11 - i - s2]
            else:
                if l2 <= 13 - i:
                    t = ' '
                elif self.__hide:
                    t = BACK
                else:
                    t = self.__player[3].hand[13 - i]
            show_line(h, m, t)

        # 空行
        if self.has_hu and self.__count == 3:
            print('\x1b[1B\x1b[78C♕')
        elif self.__player[3].fangchong:
            print('\x1b[1B\x1b[78C💔')
        else:
            print('\x1b[1B')
        # 输出自己的牌
        print('\x1b[20C', end='')
        if self.has_hu and self.__count == 2:
            print('♕\x1b[5C', end='')
        elif self.__player[2].fangchong:
            print('💔\x1b[4C', end='')
        elif self.__player[2].ting:
            print('⚑\x1b[5C', end='')
        else:
            print('\x1b[6C', end='')
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
        # time.sleep(0.1)

    def start(self):
        # 发13张牌
        j = 0
        while j < 13:
            for i in range(4):
                self.__player[i].hand.append(self.__hill.draw())
            self.show()
            j += 1
        # 理牌
        for i in range(4):
            self.__player[i].sort()
        self.show()

    def reset(self, HIDE=True):
        self.__hill.reset()
        self.__river.clear()
        self.__info = ''
        self.__hide = HIDE
        self.__count = 0
        self.has_hu = False
        for i in self.__player:
            i.restart()


if __name__ == "__main__":
    gamer_name = input('输入你的名字：')
    P = Player(gamer_name)
    # P = AI(gamer_name)
    game_state = True
    hide = True
    g = Game([AI('Bot 0'), AI('Bot 1'), P, AI('Bot 2')], HIDE=hide)
    while game_state:
        g.game()
        flag = input('输入0结束，输入其他继续。')
        if flag == '0':
            game_state = False
        g.reset(HIDE=hide)
