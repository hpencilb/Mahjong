import random


class Pai:
    def __init__(self):
        self.is_shupai = False
        self.is_zipai = False
        self.is_zhongzhang = False
        self.is_yaojiu = False
        self.is_laotou = False
        self.face = ''
        self.kind = 'default'
        self.n = 0

    def __iter__(self):
        return self.face

    def __str__(self):
        return self.face

    def __len__(self):
        return 1

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, str):
            return self.face == other
        else:
            return self.n == other.n and self.kind == other.kind

    def __ne__(self, other):
        if isinstance(other, str):
            return self.face != other
        else:
            return self.n != other.n or self.kind != other.kind

    def __lt__(self, other):
        return self.n < other.n

    def __gt__(self, other):
        return self.n > other.n

    def __le__(self, other):
        return self.n <= other.n

    def __ge__(self, other):
        return self.n >= other.n


class P(Pai):
    def __init__(self, n):
        super().__init__()
        self.kind = 'P'
        self.n = n
        if 1 <= n <= 9:
            self.face = "🀙🀚🀛🀜🀝🀞🀟🀠🀡"[n - 1]
        else:
            self.face = "🀫"
        self.is_shupai = True
        if n == 1 or n == 9:
            self.is_yaojiu = True
            self.is_laotou = True
        else:
            self.is_zhongzhang = True

    def __add__(self, other):
        return P(self.n + other)

    def __sub__(self, other):
        return P(self.n - other)


class S(Pai):
    def __init__(self, n):
        super().__init__()
        self.kind = 'S'
        self.n = n
        if 1 <= n <= 9:
            self.face = "🀐🀑🀒🀓🀔🀕🀖🀗🀘"[n - 1]
        else:
            self.face = "🀫"
        self.is_shupai = True
        if n == 1 or n == 9:
            self.is_yaojiu = True
            self.is_laotou = True
        else:
            self.is_zhongzhang = True

    def __add__(self, other):
        return S(self.n + other)

    def __sub__(self, other):
        return S(self.n - other)


class M(Pai):
    def __init__(self, n):
        super().__init__()
        self.kind = 'M'
        self.n = n
        if 1 <= n <= 9:
            self.face = "🀇🀈🀉🀊🀋🀌🀍🀎🀏"[n - 1]
        else:
            self.face = "🀫"
        self.is_shupai = True
        if n == 1 or n == 9:
            self.is_yaojiu = True
            self.is_laotou = True
        else:
            self.is_zhongzhang = True

    def __add__(self, other):
        return M(self.n + other)

    def __sub__(self, other):
        return M(self.n - other)


class F(Pai):
    def __init__(self, n):
        super().__init__()
        self.kind = 'F'
        self.n = n
        self.face = "🀀🀁🀂🀃"[n - 1]
        self.is_zipai = True
        self.is_yaojiu = True


class Y(Pai):
    def __init__(self, n):
        super().__init__()
        self.kind = 'Y'
        self.n = n
        self.face = "🀄🀆🀅"[n - 1]
        self.is_zipai = True
        self.is_yaojiu = True


class Hill:
    def __init__(self):
        self.__hill = PaiList()
        for i in range(4):
            for j in range(9):
                self.__hill.append(P(j + 1))
                self.__hill.append(S(j + 1))
                self.__hill.append(M(j + 1))
            for j in range(4):
                self.__hill.append(F(j + 1))
            for j in range(3):
                self.__hill.append(Y(j + 1))

    def __len__(self):
        return len(self.__hill)

    def draw(self):
        return self.hill.pop(self.hill.index(random.choice(self.hill.li)))

    @property
    def hill(self):
        return self.__hill

    def get_P(self):
        return [i for i in self.__hill if i.kind == 'P']

    def get_S(self):
        return [i for i in self.__hill if i.kind == 'S']

    def get_M(self):
        return [i for i in self.__hill if i.kind == 'M']

    def get_F(self):
        return [i for i in self.__hill if i.kind == 'F']

    def get_Y(self):
        return [i for i in self.__hill if i.kind == 'Y']

    def get_shupai(self):
        return [i for i in self.__hill if i.is_shupai]

    def get_zipai(self):
        return [i for i in self.__hill if i.is_zipai]

    def get_zhongzhang(self):
        return [i for i in self.__hill if i.is_zhongzhang]

    def get_yaojiu(self):
        return [i for i in self.__hill if i.is_yaojiu]

    def get_laotou(self):
        return [i for i in self.__hill if i.is_laotou]

    def reset(self):
        self.__hill.clear()
        for i in range(4):
            for j in range(9):
                self.__hill.append(P(j + 1))
                self.__hill.append(S(j + 1))
                self.__hill.append(M(j + 1))
            for j in range(4):
                self.__hill.append(F(j + 1))
            for j in range(3):
                self.__hill.append(Y(j + 1))


class PaiList:
    def __init__(self, li=None):
        if li is None:
            li = []
        self.li = li

    def __str__(self):
        rep = ''
        for i in self.li:
            rep += str(i)
        return rep

    def __iter__(self):
        return iter(self.li)

    def __contains__(self, item):
        for i in self.li:
            if item == i:
                return True
        return False

    def __len__(self):
        return len(self.li)

    def __getitem__(self, item):
        return self.li[item]

    def __setitem__(self, key, value):
        self.li[key] = value

    def index(self, item):
        for i in range(len(self.li)):
            if item == self.li[i]:
                return i

    def get_n(self):
        return [i.n for i in self.li]

    def append(self, item):
        self.li.append(item)

    def extend(self, other):
        self.li.extend(other.li)

    def remove(self, item):
        self.li.pop(self.index(item))

    def count(self, item):
        c = 0
        for i in self.li:
            if i == item:
                c += 1
        return c

    def pop(self, index):
        return self.li.pop(index)

    def sorted(self):
        for i in range(len(self.li) - 1):
            for j in range(len(self.li) - i - 1):
                if self.li[j] > self.li[j + 1]:
                    tmp = self.li[j]
                    self.li[j] = self.li[j + 1]
                    self.li[j + 1] = tmp
        return self

    def set(self):
        temp = PaiList()
        for i in self.li:
            if i not in temp:
                temp.append(i)
        temp.sorted()
        return temp

    def clear(self):
        self.li = []

    def is_empty(self):
        if len(self.li) == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    l = PaiList([P(1), P(2), P(3), P(4), P(5), P(6), P(7), P(8), P(9)])
    print(l)
    print(random.choice(l))
    # print(l[0])
    # a = PaiList()
    # b = []
    # b.append(a)
    # print(len(b))
    # a = P(1)
    # alist = PaiList([a + 1, a + 2, a + 3])
    # alist.remove(P(3))
    # b = PaiList(alist)
    # print(b)
    # l.set()
    # h = Hill()
    # print(h.draw())
