import copy

pai_kinds = (
    [f"{num}{kind}" for kind in "mps" for num in range(1, 10)]
    + [f"{num}z" for num in range(1, 8)]
    + [f"{num}g" for num in range(1, 10)]
    + ["mt"]
)


class tehai:
    def __init__(self, pai_list):
        self.paishi = [0] * 44
        self.n_pai = 0
        self.add(pai_list)

    def convert(self, pai_list):
        ans = []
        for pai in pai_list:
            assert len(pai) == 2
            pai_num = int(pai[0]) if pai != "mt" else -1
            if pai[1] == "m":
                ans.append(pai_num - 1)
            elif pai[1] == "p":
                ans.append(pai_num + 9 - 1)
            elif pai[1] == "s":
                ans.append(pai_num + 18 - 1)
            elif pai[1] == "z":
                ans.append(pai_num + 27 - 1)
            elif pai[1] == "g":
                ans.append(pai_num + 34 - 1)
            elif pai == "mt":
                ans.append(43)
            else:
                raise ValueError
        return ans

    def add(self, pai_list):
        for pai in self.convert(pai_list):
            self.paishi[pai] += 1
            self.n_pai += 1

    def check(self, pai_list):
        tmp_paishi = self.paishi[:]
        for pai in self.convert(pai_list):
            tmp_paishi[pai] -= 1
        for pai in tmp_paishi:
            if pai < 0:
                return False
        return True

    def elim(self, pai_list):
        tmp_paishi = self.paishi[:]

        ans_list = []

        for pai in self.convert(pai_list):
            pai_num_mps = 0 if pai > 26 else pai % 9 + 1
            if tmp_paishi[pai] > 0:
                tmp_paishi[pai] -= 1
                ans_list.append(pai_kinds[pai])
            elif pai_num_mps > 0 and tmp_paishi[pai_num_mps + 34 - 1] > 0:
                tmp_paishi[pai_num_mps + 34 - 1] -= 1
                ans_list.append(pai_kinds[pai_num_mps + 34 - 1])
            elif tmp_paishi[43] > 0:
                tmp_paishi[43] -= 1
                ans_list.append(pai_kinds[43])

            else:
                return []

        self.paishi = tmp_paishi[:]
        self.n_pai -= len(pai_list)
        return ans_list

    def sample(self):
        for pai, n_pai in enumerate(self.paishi):
            if n_pai > 0:
                return pai_kinds[pai]
        return -1


def tehai_kaitou(tehai_zip):
    ans = []
    tmp = []
    ind = 0
    #     cnt = 0
    while ind < len(tehai_zip):
        if tehai_zip[ind] in "123456789":
            tmp.append(tehai_zip[ind])
        else:
            for num in tmp:
                ans.append(num + tehai_zip[ind])
            tmp = []
        ind += 1
    #         print(tmp)
    #         cnt += 1
    #         if cnt == 100:
    #             break
    for i in range(len(ans)):
        if ans[i] == "1t":
            ans[i] = "mt"
    return ans


def all_pattern(pai):
    pattern = [[pai] * 2, [pai] * 3]
    if pai[1] == "z" or pai == "mt":
        return pattern
    num = int(pai[0])
    k = pai[1]
    for shift in range(-2, 1):
        if 1 <= num + shift <= 7:
            pattern.append([f"{num + shift}{k}", f"{num + shift + 1}{k}", f"{num + shift + 2}{k}"])
    return pattern


def valid(tehai, n_mentsu, n_janto):
    #     print(tehai.paishi[:5],  n_mentsu, n_janto, tehai.n_pai)

    if n_mentsu == 0 and n_janto == 0:
        #         print("tehai.n_pai",tehai.n_pai)
        if tehai.n_pai == 0:
            return True, []
        return False, []
    if n_mentsu < 0 or n_janto < 0:
        return False, []
    ans = False
    ans_list = []
    #     print(tehai.paishi[0])
    for pat in all_pattern(tehai.sample()):
        #         print(pat)
        pat_elim = tehai.elim(pat)
        if pat_elim:
            if len(pat_elim) == 2:
                ans1, list1 = valid(copy.copy(tehai), n_mentsu, n_janto - 1)
            else:
                ans1, list1 = valid(copy.copy(tehai), n_mentsu - 1, n_janto)
            if ans1:
                ans = True
                if len(list1) > 0:
                    for item in list1:
                        ans_list.append(item[:] + [pat_elim[:]])
                else:
                    ans_list.append([pat_elim[:]])
            tehai.add(pat_elim)
    #     print(ans_list)
    return ans, ans_list


def get_result(tehai_zip):
    t = tehai(tehai_kaitou(tehai_zip))
    waits = []
    agarikeis = {}
    for agaripai in pai_kinds:
        t.add([agaripai])
        ans, ans_list = valid(t, t.n_pai // 3, int(t.n_pai % 3 == 2))
        for i in range(len(ans_list)):
            ans_list[i].sort()
            ans_list[i] = tuple([tuple(j) for j in ans_list[i]])

        ans_list = set(ans_list)
        if len(ans_list) > 0:
            agarikeis[agaripai] = ans_list
            waits.append(agaripai)
        t.elim([agaripai])

    agarikei_str = ["\n"]
    for k in agarikeis.keys():
        agarikei_str.append(k)
        agarikei_str.append("\n")
        for agarikei in agarikeis[k]:
            agarikei_str.append(str(agarikei))
            agarikei_str.append("\n")
    agarikei_str = "".join(agarikei_str)
    return waits, agarikei_str
