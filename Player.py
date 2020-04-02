import random
import copy

WAN = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"  # 0-8
TIAO = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"  # 9-17
TONG = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"  # 18-26
ELSE = "🀀🀁🀂🀃🀄🀅🀆"  # 27-33
DICT = dict(zip(WAN + TIAO + TONG + ELSE, range(34)))
hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)


def get_key(dct, v):
    return list(filter(lambda x: dct[x] == v, dct))


def has_shunzi(l_s):
    temp = copy.deepcopy(l_s)
    L = len(l_s)
    # 如果进来的时候只有3个 直接判断
    if L == 3:
        if (temp[0] == temp[1] and temp[0] == temp[2]) or (temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2):
            return True
        else:
            return False
    # 其他情况先去掉所有刻子
    count = 0
    while count < L - 2:
        i = count
        if l_s[i] == l_s[i + 1] and l_s[i] == l_s[i + 2]:
            temp.remove(l_s[i])
            temp.remove(l_s[i])
            temp.remove(l_s[i])
            count += 3
        else:
            count += 1
    # 如果只有刻子 满足
    if len(temp) == 0:
        return True
    # 如果字牌有不是刻子的 不满足
    elif temp[0] >= 27:
        return False
    # 如果正好剩下3个是顺子
    elif len(temp) == 3:
        if temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2:
            return True
        else:
            return False
    # 如果剩下超过3个 去重先去掉最小的一组
    elif len(temp) > 3:
        s = list(set(l_s))
        s.sort()
        if s[0] == s[1] - 1 and s[0] == s[2] - 2:
            temp.remove(s[0])
            temp.remove(s[1])
            temp.remove(s[2])
            # 递归
            if has_shunzi(temp):
                return True
    return False


def has_quetou(l_q):
    temp = copy.deepcopy(l_q)
    for i in range(len(l_q) - 1):
        if l_q[i] == l_q[i + 1]:
            temp.remove(l_q[i])
            temp.remove(l_q[i])
            if len(temp) == 0:
                return True
            elif has_shunzi(temp):
                return True
            else:
                temp = copy.deepcopy(l_q)
    return False


def hulemei(hand_list):
    # TODO 特殊牌型胡牌没写
    l_W = []
    l_S = []
    l_P = []
    l_Z = []
    for i in hand_list:
        if 0 <= i <= 8:
            l_W.append(i)
        elif 9 <= i <= 17:
            l_S.append(i)
        elif 18 <= i <= 26:
            l_P.append(i)
        else:
            l_Z.append(i)
    L = [l_W, l_S, l_P, l_Z]
    # print(L)
    l_que_tou = []
    for i in L:
        le = len(i)
        if le == 1 or le == 4 or le == 7 or le == 10 or le == 13:
            return False
        elif le == 2 or le == 5 or le == 8 or le == 11 or le == 14:
            l_que_tou.append(i)
        else:
            if le > 0:
                if not has_shunzi(i):
                    return False
            else:
                continue
    if len(l_que_tou) != 1:
        return False
    if not has_quetou(l_que_tou[0]):
        return False
    return True


class Player:
    def __init__(self, name='Player'):
        self.__name = name
        self.hand = []
        self.hula = False
        self.side = []

    def play(self):
        print('  ', end='')
        for i in range(len(self.hand)):
            print(f'{i}-{self.hand[i]}', end=' ')
            if self.hand[i] != '🀄':
                print(' ', end='')
        print('\r')
        item = int(input('选择你要出的牌：'))
        return self.hand.pop(item)

    def hu(self, item):
        if item != '':  # 自摸不需要加一张
            self.hand.append(item)
        hand_list = [DICT[i] for i in self.hand]
        hand_list.sort()
        if hulemei(hand_list):
            flag = input('能胡，胡不？(y/n)：')
            if flag == 'y':
                self.hula = True
                print(f'Player {self.name} 胡啦! ', end='')
                return True
        if item != '':
            self.hand.remove(item)
            self.sort()
        return False

    def gang(self, item):
        if self.hand.count(item) == 3:
            flag = input('能杠，杠不？(y/n)：')
            if flag == 'y':
                self.side.append(item * 4)
                self.hand.remove(item)
                self.hand.remove(item)
                self.hand.remove(item)
                return True
        return False

    def peng(self, item):
        if self.hand.count(item) == 2:
            flag = input('能碰，碰不？(y/n)：')
            if flag == 'y':
                self.side.append(item * 3)
                self.hand.remove(item)
                self.hand.remove(item)
                return True
        return False

    def chi(self, item):
        l_chi = []
        can_chi = False
        it = DICT[item]
        hand_list = [DICT[i] for i in self.hand]
        # 字牌没有吃
        if it >= 27:
            return False
        else:
            # 边张只有一种吃法
            if it == 0 or it == 9 or it == 18:
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
            elif it == 8 or it == 17 or it == 26:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 2, it - 1])
                    can_chi = True
            # 边二张有两种吃法
            elif it == 1 or it == 10 or it == 19:
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
            elif it == 7 or it == 16 or it == 25:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 1, it - 2])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
            # 一般张有三种吃法
            else:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 2, it - 1])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
            if can_chi:
                flag = input('能吃，吃不？(y/n)：')
                if flag == 'y':
                    if len(l_chi) == 1:
                        l_chi = l_chi[0]
                        for i in l_chi:
                            self.hand.remove(get_key(DICT, i)[0])
                        l_chi.append(it)
                        l_chi.sort()
                        block = ''
                        for i in l_chi:
                            block += get_key(DICT, i)[0]
                        self.side.append(block)
                    else:
                        print('多种吃法', end='')
                        for i in range(len(l_chi)):
                            print(f'{i}-', end='')
                            for j in l_chi[i]:
                                print(f'{get_key(DICT, j)[0]}', end='')
                                if get_key(DICT, j)[0] != '🀄':
                                    print(' ', end='')
                            print('   ', end='')
                        n = input('怎么吃：')
                        l_chi = l_chi[int(n)]
                        for i in l_chi:
                            self.hand.remove(get_key(DICT, i)[0])
                        l_chi.append(it)
                        l_chi.sort()
                        block = ''
                        for i in l_chi:
                            block += get_key(DICT, i)[0]
                        self.side.append(block)
                    return True
        return False

    def sort(self):
        for i in range(len(self.hand) - 1):
            for j in range(len(self.hand) - i - 1):
                if DICT[self.hand[j]] > DICT[self.hand[j + 1]]:
                    tmp = self.hand[j]
                    self.hand[j] = self.hand[j + 1]
                    self.hand[j + 1] = tmp

    def check(self):
        hand_list = [DICT[i] for i in self.hand]
        hand_list.sort()
        if hulemei(hand_list):
            return True
        else:
            return False

    def restart(self):
        self.hand = []
        self.hula = False
        self.side = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class Bot(Player):
    def __init__(self, name='Bot'):
        super().__init__(name)

    # TODO AI 没写
    def play(self):
        return self.hand.pop(self.hand.index(random.choice(self.hand)))

    def hu(self, item):
        if item != '':
            self.hand.append(item)
        hand_list = [DICT[i] for i in self.hand]
        hand_list.sort()
        if hulemei(hand_list):
            self.hula = True
            print(f'Player {self.name} 胡啦! ', end='')
            return True
        else:
            if item != '':
                self.hand.remove(item)
                self.sort()
            return False

    def gang(self, item):
        if self.hand.count(item) == 3:
            self.side.append(item * 4)
            self.hand.remove(item)
            self.hand.remove(item)
            self.hand.remove(item)
            return True
        else:
            return False

    def peng(self, item):
        if self.hand.count(item) == 2:
            self.side.append(item * 3)
            self.hand.remove(item)
            self.hand.remove(item)
            return True
        else:
            return False

    def chi(self, item):
        l_chi = []
        can_chi = False
        it = DICT[item]
        hand_list = [DICT[i] for i in self.hand]
        if it >= 27:
            return False
        else:
            if it == 0 or it == 9 or it == 18:
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
            elif it == 8 or it == 17 or it == 26:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 2, it - 1])
                    can_chi = True
            elif it == 1 or it == 10 or it == 19:
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
            elif it == 7 or it == 16 or it == 25:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 1, it - 2])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
            else:
                if it - 1 in hand_list and it - 2 in hand_list:
                    l_chi.append([it - 2, it - 1])
                    can_chi = True
                if it - 1 in hand_list and it + 1 in hand_list:
                    l_chi.append([it - 1, it + 1])
                    can_chi = True
                if it + 1 in hand_list and it + 2 in hand_list:
                    l_chi.append([it + 1, it + 2])
                    can_chi = True
            if can_chi:
                l_chi = l_chi[0]
                for i in l_chi:
                    self.hand.remove(get_key(DICT, i)[0])
                l_chi.append(it)
                l_chi.sort()
                block = ''
                for i in l_chi:
                    block += get_key(DICT, i)[0]
                self.side.append(block)
                return True
        return False


if __name__ == '__main__':
    p = Bot()
    # for i in range(20):
    #     p.hand = random.choices(hill, k=14)
    # p.hand = ['🀈', '🀈', '🀉', '🀊', '🀋', '🀖', '🀗', '🀘', '🀛', '🀜', '🀝', '🀃', '🀃', '🀃']
    # p.hand = ['🀉', '🀉', '🀑', '🀒', '🀓', '🀔', '🀖', '🀛', '🀜', '🀝', '🀆', '🀆', '🀆', '🀕']
    # p.hand = ['🀈', '🀈', '🀍', '🀍', '🀎', '🀎', '🀏', '🀏', '🀙', '🀚', '🀛', '🀟', '🀟', '🀟']
    # for i in range(10):
    p.hand = ['🀐', '🀑', '🀒', '🀖', '🀘', '🀞', '🀟', '🀠', '🀀', '🀀', '🀀', '🀆', '🀆', '🀆']
    #     p.play()
    #     print(p.hand)

    print(p.check())
    print(p.hand)
    # print(hulemei([5, 5, 5,6,6]))
