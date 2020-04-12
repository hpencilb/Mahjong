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
        choose = random.choice(self.hand)
        for i in set(hand):
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
        hand_list = [DICT[i] for i in self.hand]
        hand_list.sort()
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

        def r_dup(s, n):
            for i in set(s):
                c = s.count(i)
                if c == n:
                    for j in range(c):
                        s.remove(i)

        def r_shunzi(s):
            temp = list(set(s))
            temp.sort()
            for i in temp:
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
            temp = list(set(s))
            temp.sort()
            for i in temp:
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
        r_dup(l_Z, 3)
        r_dup(l_Z, 2)
        if len(l_Z) > 0:
            k = random.random()
            if k >= 0.1:
                choose = random.choice(l_Z)
                return self.hand.index(self.get_key(DICT, choose))
        # 去顺子
        choose_list1 = []
        r_shunzi(l_W)
        choose_list1.extend(l_W)
        r_shunzi(l_S)
        choose_list1.extend(l_S)
        r_shunzi(l_P)
        choose_list1.extend(l_P)
        # 再去刻子
        choose_list2 = []
        r_dup(l_W, 3)
        choose_list2.extend(l_W)
        r_dup(l_S, 3)
        choose_list2.extend(l_S)
        r_dup(l_P, 3)
        choose_list2.extend(l_P)
        # 再去雀头
        choose_list3 = []
        r_dup(l_W, 2)
        choose_list3.extend(l_W)
        r_dup(l_S, 2)
        choose_list3.extend(l_S)
        r_dup(l_P, 2)
        choose_list3.extend(l_P)
        # 再去可能是顺子的
        choose_list4 = []
        r_shunzi_possible(l_W)
        choose_list4.extend(l_W)
        r_shunzi_possible(l_S)
        choose_list4.extend(l_S)
        r_shunzi_possible(l_P)
        choose_list4.extend(l_P)
        if len(choose_list4) != 0:
            choose = random.choice(choose_list4)
        elif len(choose_list3) != 0:
            choose = random.choice(choose_list3)
        elif len(choose_list2) != 0:
            choose = random.choice(choose_list2)
        elif len(choose_list1) != 0:
            choose = random.choice(choose_list1)
        else:
            choose = random.choice(hand_list)
        return self.hand.index(self.get_key(DICT))

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

    def action_chi(self, it, l_chi):
        """

        :param it: 能吃的牌的DICT字典编号
        :param l_chi: 能吃的牌的字典编号组成的list
        :return:
        """
        self.chi_num = 0
        chi = copy.deepcopy(l_chi)
        hand_list = [DICT[i] for i in self.hand]
        if it <= 8:
            n = 0
        elif it <= 17:
            n = 1
        else:
            n = 2
        l_W = []
        l_S = []
        l_P = []
        for i in hand_list:
            if 0 <= i <= 8:
                l_W.append(i)
            elif 9 <= i <= 17:
                l_S.append(i)
            elif 18 <= i <= 26:
                l_P.append(i)
        L = [l_W, l_S, l_P][n]
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

    def get_ting_list(self, hand, hill):
        li = []
        for i in PaiList(hill).set():
            hand.append(i)
            if self.hulemei(hand):
                li.append(i)
            hand.remove(i)
        for i in range(len(li) - 1):
            for j in range(len(li) - i - 1):
                if DICT[li[j]] > DICT[li[j + 1]]:
                    tmp = li[j]
                    li[j] = li[j + 1]
                    li[j + 1] = tmp
        return li


if __name__ == '__main__':
    p = AI()
    p.hand = '🀋 🀏 🀑 🀒 🀕 🀗 🀘 🀙 🀛 🀝 🀡 🀁 🀆 🀈'.split(' ')
    print(p.hand)
    print(p.hu())
