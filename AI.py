from Player import *
import random
import copy

WAN = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"  # 0-8
TIAO = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"  # 9-17
TONG = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"  # 18-26
ELSE = "🀀🀁🀂🀃🀄🀅🀆"  # 27-33
DICT = dict(zip(WAN + TIAO + TONG + ELSE, range(34)))
HILL = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)


class AI(Bot):
    def __init__(self, NAME='AI'):
        super().__init__(NAME=NAME)
        self.last_ting_count = 0
        self.chi_num = 0

    # TODO AI 强化
    def action_play(self):
        hand = copy.deepcopy(self.hand)
        m = 0
        if not self.face_down.is_empty():
            choose = random.choice(self.hand)
            for i in hand.set():
                hand.remove(i)
                l_t = self.get_ting_list(hand, self.face_down)
                c = self.count_ting(l_t, self.face_down)
                if c > m:
                    m = c
                    choose = i
                hand.append(i)
            if m > self.last_ting_count:
                self.last_ting_count = m
            if self.ting:
                return self.hand.index(choose)
        p = PaiList([i for i in self.hand if i.kind == 'P']).sorted()
        s = PaiList([i for i in self.hand if i.kind == 'S']).sorted()
        m = PaiList([i for i in self.hand if i.kind == 'M']).sorted()
        f = PaiList([i for i in self.hand if i.kind == 'F']).sorted()
        y = PaiList([i for i in self.hand if i.kind == 'Y']).sorted()

        def r_dup(s, n):
            for i in s.set():
                c = s.count(i)
                if c == n:
                    for j in range(c):
                        s.remove(i)

        def r_shunzi(s):
            for i in s.set():
                if i in s and i - 1 in s and i + 1 in s:
                    s.remove(i)
                    s.remove(i - 1)
                    s.remove(i + 1)
                if i in s and i - 2 in s and i - 1 in s:
                    s.remove(i)
                    s.remove(i - 1)
                    s.remove(i - 2)
                if i in s and i + 1 in s and i + 2 in s:
                    s.remove(i)
                    s.remove(i + 1)
                    s.remove(i + 2)

        def r_shunzi_possible(s):
            for i in s.set():
                if i in s and i - 2 in s:
                    s.remove(i)
                    s.remove(i - 2)
                if i in s and i - 1 in s:
                    s.remove(i)
                    s.remove(i - 1)
                if i in s and i + 1 in s:
                    s.remove(i)
                    s.remove(i + 1)
                if i in s and i + 2 in s:
                    s.remove(i)
                    s.remove(i + 2)

        # 先考虑字牌
        r_dup(f, 3)
        r_dup(f, 2)
        r_dup(y, 3)
        r_dup(y, 2)
        if len(f) > 0:
            k = random.random()
            if k >= 0.1:
                choose = random.choice(f)
                return self.hand.index(choose)
        if len(y) > 0:
            k = random.random()
            if k >= 0.1:
                choose = random.choice(y)
                return self.hand.index(choose)
        # 去顺子
        choose_list = []
        r_shunzi(m)
        choose_list.append(copy.deepcopy(m))
        r_shunzi(s)
        choose_list[0].extend(s)
        r_shunzi(p)
        choose_list[0].extend(p)
        # 再去刻子
        r_dup(m, 3)
        choose_list.append(copy.deepcopy(m))
        r_dup(s, 3)
        choose_list[1].extend(s)
        r_dup(p, 3)
        choose_list[1].extend(p)
        # 再去雀头
        r_dup(m, 2)
        choose_list.append(m)
        r_dup(s, 2)
        choose_list[2].extend(s)
        r_dup(p, 2)
        choose_list[2].extend(p)
        # 再去可能是顺子的
        r_shunzi_possible(m)
        choose_list.append(m)
        r_shunzi_possible(s)
        choose_list[3].extend(s)
        r_shunzi_possible(p)
        choose_list[3].extend(p)
        if len(choose_list[3]) != 0:
            choose = random.choice(choose_list[3])
        elif len(choose_list[2]) != 0:
            choose = random.choice(choose_list[2])
        elif len(choose_list[1]) != 0:
            choose = random.choice(choose_list[1])
        elif len(choose_list[0]) != 0:
            choose = random.choice(choose_list[0])
        else:
            choose = random.choice(hand)
        return self.hand.index(choose)

    def action_hu(self):
        return True

    def action_chigang(self, item):
        return True

    def action_zigang(self, item):
        return True

    def action_jiagang(self, i, j):
        """

        :param i: 能加杠的牌在hand的位置
        :param j: 碰的牌堆在side的位置
        :return:
        """
        return True

    def action_peng(self, item):
        return True

    def action_chi(self, it, chi):
        """

        :param it: 能吃的牌 Pai
        :param chi: 手牌中能与能吃的牌组合的牌的组合的 list
        :return:
        """
        self.chi_num = 0
        t = it.kind
        L = PaiList([i for i in self.hand if i.kind == t]).sorted()

        for i in chi:
            if i[0] == i[1] - 1:
                if i[0] - 1 in L or i[1] + 1 in L:
                    return False
            if i[0] == i[1] - 2:
                if i[0] - 1 in L or i[1] + 1 in L:
                    self.chi_num = 0
                else:
                    self.chi_num = chi.index(i)
                return True
        return True

    def action_chiwhich(self, l_chi):
        return l_chi.index(random.choice(l_chi))

    def count_ting(self, l, h):
        count = 0
        for i in l:
            count += h.count(i)
        return count

    def get_ting_list(self, hand, h):
        li = PaiList()
        for i in h.set():
            hand.append(i)
            if self.hulemei(hand):
                li.append(i)
            hand.remove(i)
        li.sorted()
        return li

    def restart(self):
        super().restart()
        self.last_ting_count = 0
        self.chi_num = 0


if __name__ == '__main__':
    p = AI()
    # p.hand = '🀋 🀏 🀑 🀒 🀕 🀗 🀘 🀙 🀛 🀝 🀡 🀁 🀆 🀈'.split(' ')
    p.hand = PaiList([S(2), P(6), M(6), P(7), S(7), M(7), P(8), M(8), S(9), S(2), S(2)])
    p.sort()
    print(p.hand)
    print(p.hu())
