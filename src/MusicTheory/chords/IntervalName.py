#音程名。スケール構成音のどの位置の音であるかを特定する。
#Id: 0〜11。
#Name: P1, m2, M2, m3, M3, P4, d5, a4, P5
#完全系: 1, 4, 5 (8, 11, 12)
#長短系: 2, 3, 6, 7 (9, 10, 13, 14)
#増減系: (完全系: 1, 4, 5 よりも半音[高/低]い) (長短系: 増: 長よりも半音高い, 減: 短よりも半音低い)
#https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1365320628
#https://okwave.jp/qa/q6858420.html
class IntervalName:
    prefix = {'P': {'jp':'完全', 'en':'Perfect'}, 'm': {'jp':'短', 'en':'Minor'}, 'M': {'jp':'長', 'en':'Major'}, 'a': {'jp':'増', 'en':'Augment'}, 'd': {'jp':'減', 'en':'Diminish'}}
    #音程名から半音いくつ分であるかを返す
    @classmethod
    def GetHalfNum(cls, name):
        if name[0] == 'P': return cls.GetHalfNumPerfect(name)
        elif name[0] == 'm': return cls.GetHalfNumMinor(name)
        elif name[0] == 'M': return cls.GetHalfNumMajor(name)
        elif name[0] == 'a': return cls.GetHalfNumAugment(name)
        elif name[0] == 'd': return cls.GetHalfNumDiminish(name)
        else: raise Exception(f'1字目のprefixは{cls.prefix.keys()}のいずれかにしてください。: {name}')
#        if name[0] not in prefix.keys(): raise Exception(f'1字目のprefixは{prefix.keys()}のいずれかにしてください。: {name}')
    @classmethod
    def GetHalfNumPerfect(cls, name):
#        if name[0] == 'P' and if int(name[1]) in [1, 4, 5, 8, 1, 12]
        if name[0] == 'P':
            interval_num = int(name[1:])
            if 1 == interval_num: return 0
            elif 4 == interval_num: return 5
            elif 5 == interval_num: return 7
            elif 1+7 == interval_num: return 0+12
            elif 4+7 == interval_num: return 5+12
            elif 5+7 == interval_num: return 7+12
            else: raise Exception('2字目の度数は1,4,5,8,11,12のいずれかにしてください。')
    @classmethod
    def GetHalfNumMinor(cls, name):
        if name[0] == 'm':
            interval_num = int(name[1:])
            if 2 == interval_num: return 1
            elif 3 == interval_num: return 3
            elif 6 == interval_num: return 8
            elif 7 == interval_num: return 10
            if 2+7 == interval_num: return 1+12
            elif 3+7 == interval_num: return 3+12
            elif 6+7 == interval_num: return 8+12
            elif 7+7 == interval_num: return 10+12
            else: raise Exception('2字目の度数は2,3,6,7,9,10,13,14のいずれかにしてください。')
    @classmethod
    def GetHalfNumMajor(cls, name):
        if name[0] == 'M':
            interval_num = int(name[1:])
            if 2 == interval_num: return 2
            elif 3 == interval_num: return 4
            elif 6 == interval_num: return 9
            elif 7 == interval_num: return 11
            if 2+7 == interval_num: return 2+12
            elif 3+7 == interval_num: return 4+12
            elif 6+7 == interval_num: return 9+12
            elif 7+7 == interval_num: return 11+12
            else: raise Exception('2字目の度数は2,3,6,7,9,10,13,14のいずれかにしてください。')
    @classmethod
    def GetHalfNumAugment(cls, name):
        if name[0] == 'a':
            interval_num = int(name[1:])
            if 1 == interval_num: return 0+1
            elif 2 == interval_num: return 2+1
            elif 3 == interval_num: return 4+1
            elif 4 == interval_num: return 5+1
            elif 5 == interval_num: return 7+1
            elif 6 == interval_num: return 9+1
            elif 7 == interval_num: return 11+1
            elif 1+7 == interval_num: return 0+1+12
            elif 2+7 == interval_num: return 2+1+12
            elif 3+7 == interval_num: return 4+1+12
            elif 4+7 == interval_num: return 5+1+12
            elif 5+7 == interval_num: return 7+1+12
            elif 6+7 == interval_num: return 9+1+12
            elif 7+7 == interval_num: return 11+1+12
            else: raise Exception('2字目の度数は1〜14の自然数にしてください。')
    @classmethod
    def GetHalfNumDiminish(cls, name):
        if name[0] == 'd':
            interval_num = int(name[1:])
            if 1 == interval_num: return 0-1
            elif 2 == interval_num: return 1-1
            elif 3 == interval_num: return 3-1
            elif 4 == interval_num: return 5-1
            elif 5 == interval_num: return 7-1
            elif 6 == interval_num: return 8-1
            elif 7 == interval_num: return 10-1
            elif 1+7 == interval_num: return 0-1+12
            elif 2+7 == interval_num: return 1-1+12
            elif 3+7 == interval_num: return 3-1+12
            elif 4+7 == interval_num: return 5-1+12
            elif 5+7 == interval_num: return 7-1+12
            elif 6+7 == interval_num: return 8-1+12
            elif 7+7 == interval_num: return 10-1+12
            else: raise Exception('2字目の度数は1〜14の自然数にしてください。')

if __name__ == '__main__':
    import copy
    #完全系
    test_data_p = [['1', 0], ['4', 5], ['5', 7]]
    test_data_p += [[str(int(d[0])+7), d[1]+12] for d in test_data_p]
    for d in test_data_p: d[0] = 'P' + d[0]
    print(test_data_p)
    for d in test_data_p:
#        print(d, IntervalName.GetHalfNum(d[0]))
        assert(IntervalName.GetHalfNum(d[0]) == d[1])

    #長短系
    test_data_mM = [['2', 1], ['3', 3], ['6', 8], ['7', 10]]
    test_data_mM += [[str(int(d[0])+7), d[1]+12] for d in test_data_mM]
    test_data_m = copy.deepcopy(test_data_mM)
    for d in test_data_m:
        d[0] = 'm' + d[0]
    test_data_M = copy.deepcopy(test_data_mM)
    for d in test_data_M:
        d[0] = 'M' + d[0]
        d[1] += 1
    print(test_data_m)
    for d in test_data_m: assert(IntervalName.GetHalfNum(d[0]) == d[1])
    print(test_data_M)
    for d in test_data_M: assert(IntervalName.GetHalfNum(d[0]) == d[1])

    #増減系(完全系)
    test_data_p = [['1', 0], ['4', 5], ['5', 7]]
    test_data_p += [[str(int(d[0])+7), d[1]+12] for d in test_data_p]
    test_data_pa = copy.deepcopy(test_data_p)
    for d in test_data_pa:
        d[0] = 'a' + d[0]
        d[1] += 1
    print(test_data_pa)
    for d in test_data_pa: assert(IntervalName.GetHalfNum(d[0]) == d[1])
    test_data_pd = copy.deepcopy(test_data_p)
    for d in test_data_pd:
        d[0] = 'd' + d[0]
        d[1] -= 1
    print(test_data_pd)
    for d in test_data_pd: assert(IntervalName.GetHalfNum(d[0]) == d[1])

    #減系(短系)
    test_data_md = copy.deepcopy(test_data_m)
    for d in test_data_md:
        d[0] = 'd' + d[0][1:]
        d[1] -= 1
    print(test_data_md)
    for d in test_data_md: assert(IntervalName.GetHalfNum(d[0]) == d[1])

    #増系(長系)
    test_data_Ma = copy.deepcopy(test_data_M)
    for d in test_data_Ma:
        d[0] = 'a' + d[0][1:]
        d[1] += 1
    print(test_data_Ma)
    for d in test_data_Ma: assert(IntervalName.GetHalfNum(d[0]) == d[1])

