import random
import copy

WAN = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"  # 0-8
TIAO = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"  # 9-17
TONG = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"  # 18-26
ELSE = "🀀🀁🀂🀃🀄🀅🀆"  # 27-33
DICT = dict(zip(WAN + TIAO + TONG + ELSE, range(34)))
hill = list(WAN * 4 + TIAO * 4 + TONG * 4 + ELSE * 4)


def has_shunzi(l_s):
    temp = copy.deepcopy(l_s)
    L = len(l_s)
    if L == 3:
        if (temp[0] == temp[1] and temp[0] == temp[2]) or (temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2):
            return True
        else:
            return False
    # 先去刻子
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
    # 再看是不是顺子
    if temp[0] >= 27:
        return False
    if len(temp) == 3:
        if (temp[0] == temp[1] and temp[0] == temp[2]) or (temp[0] == temp[1] - 1 and temp[0] == temp[2] - 2):
            return True
        else:
            return False
    if len(temp) > 3:
        s = list(set(l_s))
        s.sort()
        if s[0] == s[1] - 1 and s[0] == s[2] - 2:
            temp.remove(s[0])
            temp.remove(s[1])
            temp.remove(s[2])
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
    def __init__(self, name='Default'):
        self.__name = name
        self.hand = []
        self.hula = False

    def play(self):
        if self.name == 'Default':
            return self.hand.pop(self.hand.index(random.choice(self.hand)))
        else:
            for i in range(len(self.hand)):
                print(f'{i}-{self.hand[i]}', end=' ')
                if self.hand[i] != '🀄':
                    print(' ', end='')
            print('\r')
            item = int(input('选择你要出的牌：'))
            return self.hand.pop(item)

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
        self.hula = hulemei(hand_list)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


if __name__ == '__main__':
    p = Player()
    # for i in range(20):
    #     p.hand = random.choices(hill, k=14)
    # p.hand = ['🀈', '🀈', '🀉', '🀊', '🀋', '🀖', '🀗', '🀘', '🀛', '🀜', '🀝', '🀃', '🀃', '🀃']
    # p.hand = ['🀉', '🀉', '🀑', '🀒', '🀓', '🀔', '🀖', '🀛', '🀜', '🀝', '🀆', '🀆', '🀆', '🀕']
    p.hand = ['🀈', '🀈', '🀍', '🀍', '🀎', '🀎', '🀏', '🀏', '🀙', '🀚', '🀛', '🀟', '🀟', '🀟']
    p.check()
    print(p.hula)
    print(p.hand)
    # print(hulemei([5, 5, 5,6,6]))
