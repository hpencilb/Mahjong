import random
import time
from Player import Player

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
        self.state = False

    def game(self):
        self.start()
        self.state = True
        # 循环摸牌出牌
        count = 0
        while self.state:
            if count >= 4:
                count = 0
            self.draw(self.__player[count])
            self.show()
            # TODO 碰吃杠点炮规则没写
            if self.__player[count].hula:
                self.state = False
                print(f'Player {count} won!')
            # TODO 结算没写
            count += 1
            # 没牌可摸时结束
            if len(self.__hill) == 0:
                self.state = False
                print('========= Game Over =========')

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
            # sorted_dict = map(lambda x: {x: info[x]}, roles)
            self.__player[i].sort()
        self.show()

    def draw(self, player):
        player.hand.append(self.__hill.pop(self.__hill.index(random.choice(self.__hill))))
        player.check()
        self.show()
        # TODO 出牌没写
        self.__river.append(player.hand.pop(player.hand.index(random.choice(player.hand))))
        player.sort()

    def show(self):
        # TODO 盖牌输出没写
        # 清屏
        print('\x1b[2J\x1b[0;0H')
        # 输出0号玩家的牌
        print(' ' * 25, end='')
        for i in self.__player[0].hand:
            if i == '🀄':
                print(i, end='')
            else:
                print(i, end=' ')
        # 空行
        print('\r\x1b[2B')

        # 交替输出1、3号玩家的牌
        def show_line(head, middle, tail):
            print(head, end='')
            if head != '🀄':
                print(' ', end='')
            print('\x1b[17C', end='')
            if len(middle) > 0:
                for j in range(len(middle)):
                    if middle[j] == '🀄':
                        print(middle[j], end='')
                    else:
                        print(middle[j] + '\x1b[1C', end='')
            print(f'\x1b[{59 - len(middle) * 2}C', end='')
            print(tail)

        for i in range(14):
            l1 = len(self.__player[1].hand)
            l2 = len(self.__player[3].hand)
            if l1 <= i:
                h = ' '
            else:
                h = self.__player[1].hand[i]
            if i >= 5:
                j = i - 5
                if len(self.__river) > 21:
                    m = self.__river[j * 21:j * 21 + 21]
                else:
                    m = self.__river[j * 21:]
            else:
                m = ''
            if l2 <= 13 - i:
                t = ''
            else:
                t = self.__player[3].hand[13 - i]
            show_line(h, m, t)
        # 空行
        print('\r\x1b[1B')
        # 输出自己的牌
        print(' ' * 25, end='')
        for i in self.__player[2].hand:
            if i == '🀄':
                print(i, end='')
            else:
                print(i, end=' ')
        print('\r')
        time.sleep(0.5)


if __name__ == "__main__":
    # print(DICT)
    p0 = Player()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    g = Game([p0, p1, p2, p3])
    g.game()
    # print(g._Game__key)
