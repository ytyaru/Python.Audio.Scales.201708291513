#!python3.6
#coding:utf-8
#https://ja.wikipedia.org/wiki/%E7%B4%94%E6%AD%A3%E5%BE%8B
#http://www.asahi-net.or.jp/~HB9T-KTD/music/Japan/Research/Genre/Tuning/tuning_just.html
#http://musica.art.coocan.jp/enharmonic.htm
#純正律(算出方法はメジャースケールの場合である)
#基音はラ(A4)だが、構成音はCからはじまる幹音(C,D,E,F,G,A,B)で構成したい

class JustIntonation:
    def __init__(self):
        self.__DENOMINATOR = 7
        self.__BaseFrequency = 440 #基準となる音をA4(ラ)とし、周波数を440として算出する
        self.__BaseKeyId = 9 #A (1オクターブ12音なら0〜11の値。[C,C#,D,D#,E,F,F#,G,G#,A,A#,B]の12音とすると9=A)
        self.__BaseKeyPitch = 4 #-1〜9（A4=440Hz。A3は220Hzになるし、A5は880Hzになる）
        self.__Frequencies = [] #C,D,E,F,G,A,Bの7音の周波数
        #C〜Bの12音における周波数。超適当。とりあえず2進数, 偶数っぽくした。
        self.__BaseFreuencies = [256, 272, 288, 308, 326, 348, 370, 392, 414, 440, 466, 492]#http://www.asahi-net.or.jp/~HB9T-KTD/music/Japan/Research/DTM/freq_map.html
        self.__scale_name = 'Major'
        self.__Scales = {'Major': [1,9/8,5/4,4/3,3/2,5/3,15/8,2], 'Minor': [1,9/8,6/5,4/3,3/2,8/5,9/5,2]}
#        self.__RateMajor = [1,9/8,5/4,4/3,3/2,5/3,15/8,2]#基音=C
#        self.__RateMinor = [1,9/8,6/5,4/3,3/2,8/5,9/5,2]#基音=A
#        self.__Rate = [1,9/8,6/5,4/3,3/2,8/5,9/5,2]#ラ(A4)を基音とした幹音7音の比。http://www.gabacho-net.jp/whims/whim0010.html
#        self.__Rate = [1,9/8,6/5,4/3,3/2,8/5,9/5,2]#ラ(A4)を基音とした幹音7音の比。http://www.gabacho-net.jp/whims/whim0010.html
#        self.__Rate = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8] #メジャースケールにおける7音の比率
#        self.__Rate = [3/5,5/8,16/25,2/3,25/36,18/25,3/4,25/32,96/125,4/5,5/6,108/125,9/10,15/16,24/25,1,25/24,27/25,9/8,25/192] #http://www.moge.org/okabe/temp/scale/node24.html
#        self.__Rate = [1,25/24,16/15,10/9,125/108,6/5,5/4,125/96,32/25,4/3,25/18,36/25,3/2,25/16,8/5,5/3,125/72,9/5,15/8,125/64,48/25,2] #http://www.moge.org/okabe/temp/scale/node24.html
        self.__calcFrequencies()
    @property
    def Denominator(self): return self.__DENOMINATOR
    @property
    def BaseKeyId(self): return self.__BaseKeyId
    @BaseKeyId.setter
    def BaseKeyId(self, v):
        if 0 <= v and v < len(self.__BaseFreuencies):
            self.__BaseKeyId = v
            self.__BaseFrequency = self.__BaseFreuencies[v]
            self.__calcFrequencies()
    @property
    def BaseKeyPitch(self): return self.__BaseKeyPitch
    def SetBaseKey(self, keyId, pitch, hz):
#        if not (isinstance(keyId, int) and -1 < keyId and keyId < self.Denominator): raise Exception(f'keyIdは0〜{self.Denominator-1}の整数値(int型)にしてください。')
#        if not isinstance(pitch, int): raise Exception('pitchはint型にしてください。')
#        if hz <= 0: raise Exception('hzは0より大きい数値にしてください。')
        self.__BaseKeyId = keyId
        self.__BaseKeyPitch = pitch
        self.BaseFrequency = hz
    @property
    def BaseFrequency(self): return self.__BaseFrequency
    @BaseFrequency.setter
    def BaseFrequency(self, v):
        if 0 < v:
            self.__BaseFrequency = v
            self.__calcFrequencies()
    @property
    def Frequencies(self): return self.__Frequencies
#    def __calcFrequencies(self):
#        self.Frequencies.clear()
#        for rate in self.__Rate: self.Frequencies.append(self.__BaseFrequency * rate)
    def __calcFrequencies(self):
        self.Frequencies.clear()
        for rate in self.__Scales[self.Scale]: self.Frequencies.append(self.__BaseFrequency * rate)
    @property
    def Scale(self): return self.__scale_name
    @Scale.setter
    def Scale(self, v):
        if v in self.__Scales.keys():
            self.__scale_name = v
            self.__calcFrequencies()
        
if __name__ == '__main__':
    def GetKeyName(keyId): return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][keyId]

    ji = JustIntonation()
    print(ji.Frequencies)
    print('---------- 1オクターブ下 ----------')
    print([f/2 for f in ji.Frequencies])
    print('---------- 1オクターブ上 ----------')
    print([f*2 for f in ji.Frequencies])

    scaleKeyId = 9
    ji.SetBaseKey(scaleKeyId, 4, 432)
    keyName = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][scaleKeyId]
    print(f"Key: {keyName}, Pitch: {ji.BaseKeyPitch}, Frequency: {ji.BaseFrequency}Hz")
    print(ji.Frequencies)
    
    scaleKeyId = 0
    ji.SetBaseKey(scaleKeyId, 3, 128)# C3=128Hz
    keyName = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][scaleKeyId]
    print(f"Key: {keyName}, Pitch: {ji.BaseKeyPitch}, Frequency: {ji.BaseFrequency}Hz")
    print(ji.Frequencies)
    print([f*2 for f in ji.Frequencies])
    print([f*3 for f in ji.Frequencies])

    ji.Scale = 'Major'
    print('==========',ji.Scale,'==========')
    for key in range(12):
        ji.BaseKeyId = key
        print('key:{:2} {}'.format(GetKeyName(ji.BaseKeyId), ji.Frequencies))
    ji.Scale = 'Minor'
    print('==========',ji.Scale,'==========')
    for key in range(12):
        ji.BaseKeyId = key
        print('key:{:2} {}'.format(GetKeyName(ji.BaseKeyId), ji.Frequencies))
