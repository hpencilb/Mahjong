import copy
import time
from PaiBasic import *


def ask_input(index, string):
    while True:
        content = input(f'{string}')
        if content.isnumeric():
            if type(index[0]) == int:
                content = int(content)
        if content in index:
            return content
        else:
            print('\x1b[1A\x1b[2K', end='')


class Player:
    def __init__(self, NAME='Player'):
        if NAME == '':
            NAME = 'Player'
        self.__name = NAME
        self.public = PaiList()
        self.hand = PaiList()
        self.river = PaiList()
        self.side = []
        self.wind = None
        self.table_wind = None
        self.ting = False
        self.riichi_flag = False
        self.riichi_list = []
        self.ting_item = ''
        self.fangchong = False
        self.hula = False
        self.face_down = PaiList()

    def play(self):
        index = self.action_play()
        item = self.hand.pop(index)
        self.river.append(item)
        return item

    def hu(self, item=None):
        if item is not None:  # 自摸不需要加一张
            self.hand.append(item)
        temp = copy.deepcopy(self.hand)
        if self.hulemei(temp):
            if self.action_hu():
                self.hula = True
                return True
        if item is not None:
            self.hand.remove(item)
            self.sort()
        return False

    def riichi(self):
        li = self.check_ting()
        if len(li) > 0:
            self.ting = True
            # if self.action_ting():
            return True
        else:
            self.ting = False
            return False

    def gang(self, item):
        if item is not None:
            if self.hand.count(item) == 3:
                if self.action_chigang(item):
                    block = PaiList(
                        [copy.deepcopy(item), copy.deepcopy(item), copy.deepcopy(item), copy.deepcopy(item)])
                    self.side.append(block)
                    self.hand.remove(item)
                    self.hand.remove(item)
                    self.hand.remove(item)
                    return True
        else:
            for i in self.hand.set():
                if self.hand.count(i) == 4:
                    if self.action_zigang(i):
                        block = PaiList([copy.deepcopy(i), copy.deepcopy(i), copy.deepcopy(i), copy.deepcopy(i)])
                        self.side.append(block)
                        self.hand.remove(i)
                        self.hand.remove(i)
                        self.hand.remove(i)
                        self.hand.remove(i)
                        return True
        return False

    def jiagang(self):
        if self.side:
            for i in self.hand.set():
                for j in range(len(self.side)):
                    if self.side[j].count(i) == 3:
                        if self.action_jiagang(i, j):
                            self.side[j].append(i)
                            self.hand.remove(i)
                            return True
        return False

    def peng(self, item):
        if self.hand.count(item) == 2:
            if self.action_peng(item):
                block = PaiList([copy.deepcopy(item), copy.deepcopy(item), copy.deepcopy(item)])
                self.side.append(block)
                self.hand.remove(item)
                self.hand.remove(item)
                return True
        return False

    def chi(self, item):
        l_chi = []
        can_chi = False
        n = item.n
        # 字牌没有吃
        if item.kind == 'Y' or item.kind == 'F':
            return False
        else:
            # 边张只有一种吃法
            if n == 1:
                if item + 1 in self.hand and item + 2 in self.hand:
                    l_chi.append(PaiList([item + 1, item + 2]))
                    can_chi = True
            elif n == 9:
                if item - 1 in self.hand and item - 2 in self.hand:
                    l_chi.append(PaiList([item - 2, item - 1]))
                    can_chi = True
            # 边二张有两种吃法
            elif n == 2:
                if item + 1 in self.hand and item + 2 in self.hand:
                    l_chi.append(PaiList([item + 1, item + 2]))
                    can_chi = True
                if item - 1 in self.hand and item + 1 in self.hand:
                    l_chi.append(PaiList([item - 1, item + 1]))
                    can_chi = True
            elif n == 8:
                if item - 1 in self.hand and item - 2 in self.hand:
                    l_chi.append(PaiList([item - 2, item - 1]))
                    can_chi = True
                if item - 1 in self.hand and item + 1 in self.hand:
                    l_chi.append(PaiList([item - 1, item + 1]))
                    can_chi = True
            # 一般张有三种吃法
            else:
                if item - 1 in self.hand and item - 2 in self.hand:
                    l_chi.append(PaiList([item - 2, item - 1]))
                    can_chi = True
                if item - 1 in self.hand and item + 1 in self.hand:
                    l_chi.append(PaiList([item - 1, item + 1]))
                    can_chi = True
                if item + 1 in self.hand and item + 2 in self.hand:
                    l_chi.append(PaiList([item + 1, item + 2]))
                    can_chi = True
            if can_chi:
                if self.action_chi(item, l_chi):
                    if len(l_chi) == 1:
                        l_chi = l_chi[0]
                        for i in l_chi:
                            self.hand.remove(i)
                        l_chi.append(item)
                        l_chi.sorted()
                        self.side.append(l_chi)
                    else:
                        n = self.action_chiwhich(l_chi)
                        l_chi = l_chi[n]
                        for i in l_chi:
                            self.hand.remove(i)
                        l_chi.append(item)
                        l_chi.sorted()
                        self.side.append(l_chi)
                    return True
        return False

    def sort(self):
        p = PaiList([i for i in self.hand if i.kind == 'P']).sorted()
        s = PaiList([i for i in self.hand if i.kind == 'S']).sorted()
        m = PaiList([i for i in self.hand if i.kind == 'M']).sorted()
        f = PaiList([i for i in self.hand if i.kind == 'F']).sorted()
        y = PaiList([i for i in self.hand if i.kind == 'Y']).sorted()
        self.hand.clear()
        self.hand.extend(m)
        self.hand.extend(s)
        self.hand.extend(p)
        self.hand.extend(f)
        self.hand.extend(y)

    def river_last_pop(self):
        if len(self.river) > 0:
            return self.river.pop(-1)

    def check(self):
        hand = copy.deepcopy(self.hand)
        if self.hulemei(hand):
            return True
        else:
            return False

    def check_ting(self):
        h = self.face_down
        li = PaiList()
        hand = copy.deepcopy(self.hand)
        for i in h.sorted():
            hand.append(i)
            if self.hulemei(hand):
                li.append(i)
            hand.remove(i)
        self.sort()
        li.sorted()
        return li

    def get_face(self, v):
        return list(filter(lambda x: x.n == v, self.hand))[0]

    def has_quetou(self, l_q):
        temp = copy.deepcopy(l_q)
        for i in range(len(l_q) - 1):
            if l_q[i] == l_q[i + 1]:
                temp.remove(l_q[i])
                temp.remove(l_q[i])
                if len(temp) == 0:
                    return True
                elif self.has_shunzi(temp):
                    return True
            temp = copy.deepcopy(l_q)
        return False

    def has_shunzi(self, l_s):
        if len(l_s) % 3 != 0:
            return False
        temp = copy.deepcopy(l_s)
        le = len(l_s)
        # 如果进来的时候只有3个 直接判断
        if le == 3:
            if temp[0] == temp[1] and temp[0] == temp[2]:
                return True
            elif temp[0].kind == 'Y' or temp[0].kind == 'F':
                return False
            elif temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2:
                return True
            else:
                return False
        # 其他情况先去掉所有刻子
        count = 0
        while count < le - 2:
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
        elif temp[0].kind == 'Y' or temp[0].kind == 'F':
            return False
        # 如果正好剩下3个是顺子
        elif len(temp) == 3:
            if temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2:
                return True
            else:
                return False
        # 如果剩下超过3个 去重先去掉最小的一组
        elif len(temp) > 3:
            s = PaiList(PaiList(temp).set()).sorted()
            if s[0] == s[1] - 1 and s[0] == s[2] - 2:
                temp.remove(s[0])
                temp.remove(s[1])
                temp.remove(s[2])
                # 递归
                if self.has_shunzi(temp):
                    return True
        return False

    def hulemei(self, hand):
        # TODO 特殊牌型胡牌没写
        p = PaiList([i for i in hand if i.kind == 'P']).sorted()
        s = PaiList([i for i in hand if i.kind == 'S']).sorted()
        m = PaiList([i for i in hand if i.kind == 'M']).sorted()
        f = PaiList([i for i in hand if i.kind == 'F']).sorted()
        y = PaiList([i for i in hand if i.kind == 'Y']).sorted()
        L = [p, s, m, f, y]
        l_que_tou = []
        for i in L:
            le = len(i)
            if le == 0:
                continue
            elif le == 1 or le == 4 or le == 7 or le == 10 or le == 13:
                return False
            elif le == 2 or le == 5 or le == 8 or le == 11 or le == 14:
                l_que_tou.append(i)
            else:
                if not self.has_shunzi(i):
                    return False
                continue
        if len(l_que_tou) != 1:
            return False
        if not self.has_quetou(l_que_tou[0]):
            return False
        return True

    def get_public(self, public=None):
        if public is None:
            public = PaiList()
        self.public = public
        self.public.extend(self.hand)
        h = Hill().hill
        for i in self.public:
            h.remove(i)
        self.face_down = h

    def get_wind(self, W, n):
        self.table_wind = W
        self.wind = F(n + 1)

    def restart(self):
        self.hand.clear()
        self.river.clear()
        self.side = []
        self.public.clear()
        self.face_down.clear()
        self.ting = False
        self.ting_item = ''
        self.fangchong = False
        self.hula = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def action_play(self):
        print('\x1b[3C', end='')
        for i in range(len(self.hand)):
            print(f'{i + 1}{self.hand[i]}', end='  ')
            if self.hand[i] != '🀄':
                print(' ', end='')
        print('')
        # n = int(input('选择你要出的牌：')) - 1
        n = ask_input([i for i in range(0, 15)], '选择你要出的牌：') - 1
        return n

    def action_hu(self):
        flag = ask_input(['y', 'n'], '能胡，胡不? (y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_riichi(self):
        flag = ask_input(['y', 'n'], '能立直，立直不? (y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_tingwhich(self):
        pass

    def action_chigang(self, item):
        flag = ask_input(['y', 'n'], '能杠，杠不？(y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_zigang(self, item):
        flag = ask_input(['y', 'n'], '能杠，杠不？(y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_jiagang(self, i, j):
        flag = ask_input(['y', 'n'], '能杠，杠不？(y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_peng(self, item):
        flag = ask_input(['y', 'n'], '能碰，碰不？(y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_chi(self, it, l_chi):
        flag = ask_input(['y', 'n'], '能吃，吃不？(y/n):')
        if flag == 'y':
            return True
        else:
            return False

    def action_chiwhich(self, l_chi):
        print('多种吃法 ', end='')
        for i in range(len(l_chi)):
            print(f'{i + 1}-{l_chi[i]}', end='     ')
        n = ask_input([i + 1 for i in range(len(l_chi))], '怎么吃:') - 1
        return n


class Bot(Player):
    def __init__(self, NAME='Bot', think_time=1):
        super().__init__(NAME=NAME)
        self.__think_time = think_time

    def think(self):
        # 假装思考
        time.sleep(random.random() * self.__think_time)

    def action_play(self):
        self.think()
        return self.hand.index(random.choice(self.hand))

    def action_hu(self):
        self.think()
        return True

    def action_chigang(self, item):
        self.think()
        return True

    def action_zigang(self, item):
        self.think()
        return True

    def action_jiagang(self, i, j):
        """

        :param i: 能加杠的牌在hand的位置
        :param j: 碰的牌堆在side的位置
        :return:
        """
        self.think()
        return True

    def action_peng(self, item):
        self.think()
        return True

    def action_chi(self, it, l_chi):
        """

        :param it: 能吃的牌的DICT字典编号
        :param l_chi: 能吃的牌的字典编号组成的list
        :return:
        """
        self.think()
        return True

    def action_chiwhich(self, l_chi):
        self.think()
        return l_chi.index(random.choice(l_chi))


if __name__ == '__main__':
    a = P(1)
    b = PaiList([copy.deepcopy(a), copy.deepcopy(a)])

    b[0] = P(2)
    del a
    print(b)
    # p = Bot()
    # for i in range(20):
    #     p.hand = random.choices(hill, k=14)
    # p.hand = ['🀈', '🀈', '🀉', '🀊', '🀋', '🀖', '🀗', '🀘', '🀛', '🀜', '🀝', '🀃', '🀃', '🀃']
    # p.hand = ['🀉', '🀉', '🀑', '🀒', '🀓', '🀔', '🀖', '🀛', '🀜', '🀝', '🀆', '🀆', '🀆', '🀕']
    # p.hand = ['🀈', '🀈', '🀍', '🀍', '🀎', '🀎', '🀏', '🀙', '🀚', '🀛', '🀟', '🀟', '🀟']  # , '🀏']
    # p.hand = ['🀌', '🀎', '🀒', '🀓', '🀓', '🀔', '🀕', '🀘', '🀘', '🀑']
    # for i in range(10):
    # p.hand = ['🀐', '🀑', '🀒', '🀖', '🀘', '🀞', '🀟', '🀠', '🀀', '🀀', '🀀', '🀆', '🀆']  # , '🀆']
    #     p.play()
    #     print(p.hand)
    # print(p.riichi(hill))
    # print(p.hu())
    # print(p.hand)
    # print(hulemei([5, 5, 5,6,6]))
