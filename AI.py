from Player import Bot
import random

WAN = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"  # 0-8
TIAO = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"  # 9-17
TONG = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"  # 18-26
ELSE = "🀀🀁🀂🀃🀄🀅🀆"  # 27-33
DICT = dict(zip(WAN + TIAO + TONG + ELSE, range(34)))
hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)


class AI(Bot):
    def __init__(self, name='AI'):
        super().__init__(name=name)

    # TODO AI 强化
    def action_play(self):
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
            for i in set(s):
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
            for i in set(s):
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
            choose = random.choice(l_Z)
            return self.hand.index(self.get_key(DICT, choose)[0])
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
        return self.hand.index(self.get_key(DICT, choose)[0])

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
        return True

    def action_chiwhich(self, l_chi):
        return l_chi.index(random.choice(l_chi))
