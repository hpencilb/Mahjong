from Player import *
from AI import AI
import math

BACK = "🀫"


class Game:
    def __init__(self, player_list, HIDE=True):
        self.__player = player_list
        self.__dealer = None
        self.__winner = None
        self.__game_count = 0
        self.__win_count = 0
        self.__deal_count = 0
        self.__gang_count = 0
        self.__gang_player = []
        self.__table_wind = None
        self.__hide = HIDE
        self.__info = ''
        self.__hill = Hill()
        self.__wang = PaiList()
        self.__bao = PaiList()
        self.__river = PaiList()
        self.__public = PaiList()
        self.__turn = 0
        self.__last_tile = None
        self.has_hu = False
        self.has_gang = False
        self.has_jiagang = False
        self.has_peng = False
        self.has_chi = False

    def game(self):
        self.start()
        # 循环摸牌出牌
        while not self.has_hu:
            # 没牌可摸时结束
            if len(self.__hill) == 4 - self.__gang_count:
                self.__info = '游戏结束，流局。'
                break
            if self.__gang_count >= 4:
                if len(set(self.__gang_player)) > 1:
                    self.__info = '四杠散了，流局。'
                    break
            if self.__turn >= 4:
                self.__turn -= 4
            if self.draw(self.__player[self.__turn]):
                if self.has_hu:
                    break
                if self.has_gang or self.has_jiagang:
                    self.has_gang = False
                    self.has_jiagang = False
                    self.__gang_player.append(self.__turn)
                    continue
            if self.if_hu_gang_peng_chi(self.__turn):
                if self.has_hu:
                    break
                if self.has_gang or self.has_peng or self.has_chi:
                    if self.has_gang:
                        self.__turn += 1
                    self.has_gang = False
                    self.has_peng = False
                    self.has_chi = False
                    continue
            # TODO 结算算番没写
            self.__turn += 1
        if self.__winner == self.__dealer:
            self.__info += '连庄。'
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
            self.__winner = self.__player.index(player)
            return True
        if self.if_gang(player):
            self.has_gang = True
            self.__gang_count += 1
            self.show()
            # count不变 杠的人再进入到摸牌环节
            return True
        if self.if_jiagang(player):
            self.has_jiagang = True
            self.__gang_count += 1
            self.show()
            # count不变 杠的人再进入到摸牌环节
            return True
        item = player.play()
        self.__last_tile = item
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
            if self.if_hu(self.__player[i], self.__last_tile):
                self.__player[n].river_last_pop()
                self.__last_tile = None
                self.__info += f'{self.__player[n].name} 放铳。'
                self.__player[n].fangchong = True
                self.__winner = i
                self.has_hu = True
                self.__turn = i
                return True
        for i in li:
            if self.if_gang(self.__player[i], self.__last_tile):
                self.__player[n].river_last_pop()
                self.__last_tile = None
                # turn 指向杠的人
                self.__turn = i
                self.show()
                self.__gang_player.append(i)
                self.__gang_count += 1
                self.has_gang = True
                # 杠完直接摸一张出一张 相当于跳到了杠的人的摸牌环节
                return True
        for i in li:
            if self.if_peng(self.__player[i], self.__last_tile):
                self.__player[n].river_last_pop()
                self.__last_tile = None
                # 碰完出一张牌
                self.__turn = i
                self.show()
                self.has_peng = True
                item = self.__player[i].play()
                self.__last_tile = item
                self.__player[i].get_public(self.refresh_public())
                self.__player[i].riichi()
                self.__player[i].sort()
                # count 指向碰的人下家
                self.__turn += 1
                self.show()
                # 再检测打出来的牌有没有胡杠碰吃
                self.if_hu_gang_peng_chi(i)
                return True
        if n + 1 >= 4:
            n = 0
        else:
            n = n + 1
        if self.if_chi(self.__player[n], self.__last_tile):
            self.__player[n].river_last_pop()
            # 吃完出一张牌
            self.__turn = n
            self.show()
            self.has_chi = True
            item = self.__player[n].play()
            self.__last_tile = item
            self.__player[n].get_public(self.refresh_public())
            self.__player[n].riichi()
            self.__player[n].sort()
            # count 指向吃的人下家
            self.__turn = n + 1
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
        self.__river = PaiList()
        for player in self.__player:
            self.__river.extend(player.river)
        self.__public = copy.deepcopy(self.__river)
        li = []
        for i in range(4):
            if self.__player[i].side:
                li.extend(self.__player[i].side)
        if li:
            for i in li:
                self.__public.extend(i)

    def show(self):
        # 清屏, 光标移到第 1 行第 0 个字符位置
        print('\x1b[2J\x1b[0;0H')
        # 按从左往右分块输出
        # if self.has_hu and self.__count == 0:
        #     print('♕\x1b[5C', end='')
        # elif self.__player[0].fangchong:
        #     print('💔\x1b[4C', end='')
        # else:
        #     print('\x1b[6C', end='')

        # 输出1号的牌
        if len(self.__player[1].side) == 0:
            for i in range(len(self.__player[1].hand)):
                if self.__hide:
                    print(f'\x1b[{5 + i};{0}H{BACK}')
                else:
                    print(f'\x1b[{5 + i};{0}H{self.__player[1].hand[i]}')
        else:
            for i in range(len(self.__player[1].side)):
                print(f'\x1b[{4 + i + len(self.__player[1].side)};{0}H{self.__player[1].side[i]}')
            for i in range(len(self.__player[1].hand)):
                if self.__hide:
                    print(f'\x1b[{4 + 2 + 2 * len(self.__player[1].side) + i};{0}H{BACK}')
                else:
                    print(
                        f'\x1b[{4 + 2 + 2 * len(self.__player[1].side) + i};{0}H{self.__player[1].hand[i]}')

        # 输出3号的牌
        if len(self.__player[3].side) == 0:
            for i in range(len(self.__player[3].hand)):
                if self.__hide:
                    print(f'\x1b[{18 - i};{79}H{BACK}')
                else:
                    print(f'\x1b[{18 - i};{79}H{self.__player[3].hand[i]}')
        else:
            for i in range(len(self.__player[3].side)):
                print(
                    f'\x1b[{19 - len(self.__player[3].side) - i};{81 - 2 * len(self.__player[3].side[i])}H{self.__player[3].side[i]}')
            for i in range(len(self.__player[3].hand)):
                if self.__hide:
                    print(
                        f'\x1b[{19 - 2 - 2 * len(self.__player[3].side) - i};{79}H{BACK}')
                else:
                    print(
                        f'\x1b[{19 - 2 - 2 * len(self.__player[3].side) - i};{79}H{self.__player[3].hand[i]}')

        # 输出1号的河
        r1 = len(self.__player[1].river)
        if r1 > 0:
            for i in range(math.ceil(r1 / 5)):
                print(f'\x1b[{10 + i};{13}H{PaiList(self.__player[1].river[i * 5:i * 5 + 5])}')

        # 输出3号的河
        r3 = len(self.__player[3].river)
        if r3 > 0:
            for i in range(math.ceil(r3 / 5)):
                print(f'\x1b[{10 + i};{59}H{PaiList(self.__player[3].river[i * 5:i * 5 + 5])}')

        # 输出0号的牌
        if len(self.__player[0].side) == 0:
            if self.__hide:
                print(f'\x1b[{2};{28}H{(BACK+" ")*len(self.__player[0].hand)}')
            else:
                print(f'\x1b[{2};{28}H{self.__player[0].hand}')
        else:
            gap = 0
            for i in range(len(self.__player[0].side)):
                print(f'\x1b[{2};{24 + gap}H{self.__player[0].side[i]}   ')
                gap += (2 * len(self.__player[0].side[i]) + 2)
            if self.__hide:
                print(f'\x1b[{2};{26 + gap}H{(BACK+" ")*len(self.__player[0].hand)}')
            else:
                print(f'\x1b[{2};{26 + gap}H{self.__player[0].hand}')

        # 输出2号的牌
        if len(self.__player[2].side) == 0:
            print(f'\x1b[{21};{28}H{self.__player[2].hand}')
        else:
            gap = 0
            for i in range(len(self.__player[2].side)):
                print(f'\x1b[{21};{24 + gap}H{self.__player[2].side[i]}   ')
                gap += (2 * len(self.__player[2].side[i]) + 2)
            print(f'\x1b[{21};{26 + gap}H{self.__player[2].hand}')

        # 输出0号的河
        r0 = len(self.__player[0].river)
        if r0 > 0:
            for i in range(math.ceil(r0 / 10)):
                print(f'\x1b[{6 + i};{31}H{PaiList(self.__player[0].river[i * 10:i * 10 + 10])}')

        def Arrow(num):
            if num == 0:
                arr = '↑'
            elif num == 1:
                arr = '←'
            elif num == 2:
                arr = '↓'
            else:
                arr = '→'
            return arr

        def DealName(dc, gc, wc):
            if dc == 0:
                deal = '东'
            elif dc == 1:
                deal = '南'
            elif dc == 2:
                deal = '西'
            else:
                deal = '北'
            if gc == 0:
                count = '一'
            elif gc == 1:
                count = '二'
            elif gc == 2:
                count = '三'
            else:
                count = '四'
            if wc > 0:
                if wc == 1:
                    ben = '一本场'
                elif wc == 2:
                    ben = '二本场'
                elif wc == 3:
                    ben = '三本场'
                else:
                    ben = '四本场'
            else:
                ben = ''
            return deal + count + '局' + ben

        dealer_arr = Arrow(self.__dealer)
        turn_arr = Arrow(self.__turn)
        deal_name = DealName(self.__deal_count, self.__game_count, self.__win_count)
        print(f'\x1b[{9};{28}H' + '┏' + '━' * 23 + '┓')
        print(f'\x1b[{10};{28}H' + '┃' + ' ' * 4 + f'{turn_arr}  {deal_name}' + f'\x1b[{10};{52}H┃')
        print(f'\x1b[{11};{28}H' + '┃' + ' ' * 7 + f'{PaiList(self.__bao[:self.__gang_count + 1])}' + f' {BACK}' * (
                4 - self.__gang_count) + f'\x1b[{11};{52}H┃')
        print(f'\x1b[{12};{28}H' + '┃' + ' ' * 23 + '┃')
        print(
            f'\x1b[{13};{28}H' + '┃' + ' ' * 1 + f'庄 {dealer_arr}  场风  {self.__table_wind}  自风 {self.__player[2].wind}' + ' ' * 1 + '┃')
        print(f'\x1b[{14};{28}H' + '┗' + '━' * 23 + '┛')

        # 输出2号的河
        r2 = len(self.__player[2].river)
        if r2 > 0:
            for i in range(math.ceil(r2 / 10)):
                print(f'\x1b[{17 - i};{31}H{PaiList(self.__player[2].river[i * 10:i * 10 + 10])}')

        # 光标回正
        print('\x1b[21;0H')
        time.sleep(0.5)
        # time.sleep(0.1)

    def start(self):
        # 判断庄家位置
        if self.__dealer is None:
            self.__dealer = random.choice([0, 1, 2, 3])
        # 确定场风
        self.__table_wind = F(self.__deal_count + 1)
        # 庄家先出牌
        self.__turn = self.__dealer
        # 各自获得自风和场风
        for i in range(4):
            n = self.__dealer + i
            if n >= 4:
                n -= 4
            self.__player[n].get_wind(self.__table_wind, i)
        # 先确定14张王牌
        for i in range(10):
            self.__wang.append(self.__hill.draw())
        for i in range(5):
            self.__bao.append(self.__wang.pop(self.__wang.index(random.choice(self.__wang))))
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
        if self.__winner != self.__dealer:
            self.__game_count += 1
            self.__dealer += 1
            self.__win_count = 0
        else:
            self.__win_count += 1
        if self.__game_count >= 4:
            self.__game_count = 0
            self.__deal_count += 1
            if self.__deal_count >= 4:
                self.__deal_count = 0
        if self.__dealer >= 4:
            self.__dealer = 0
        self.__hill.reset()
        self.__wang.clear()
        self.__bao.clear()
        self.__river.clear()
        self.__info = ''
        self.__hide = HIDE
        self.__turn = 0
        self.__gang_count = 0
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
