#音律 = EqualTemperament
#基音Hz = 440Hz
#基音Id = A
#基音Pitch = 4
#Scale = Major
#ScaleKey = C
import MusicTheory.temperament.EqualTemperament
from MusicTheory.temperament.eq12scales.ScaleIntervals import ScaleIntervals

#12平均律における12音の名前指定で周波数を取得する
#音名(key),音高(pitch)から周波数を返す
class Scale:
    def __init__(self, temperament):
        self.__temperament = temperament
        self.__keyId = 0 # スケール(音階)のキー(調)
        self.__intervals = [2,2,1,2,2,2,1]
        self.__scaleTones = []

    @property
    def Temperament(self): return self.__temperament
    @Temperament.setter
    def Temperament(self, v): self.__temperament = v
    
    @property
    def Key(self): return self.__keyId
    @Key.setter
    def Key(self, v):
        if self.__keyId < self.__temperament.Denominator:
            self.__keyId = v
            self.Get(self.__keyId, self.__intervals)

    @property
    def Intervals(self): return self.__intervals
    @Intervals.setter
    def Intervals(self, v):
        if isinstance(v, str):
            if hasattr(ScaleIntervals, v):
                self.__intervals = getattr(ScaleIntervals, v)
                self.Get(self.__keyId, self.__intervals)
        elif isinstance(v, (list, tuple)):
            for a in v:
                if not isinstance(a, int): raise Exception('引数は[2,2,1,2,2,2,1]のような数値にしてください。1は半音、2は全音です。')
            self.__intervals = v
            self.Get(self.__keyId, self.__intervals)
        else: raise Exception('引数は[2,2,1,2,2,2,1]のようなlistか、MusicTheory.temperament.eq12scales.ScaleIntervalsの属性名にしてください。')

    @property
    def Tones(self): return self.__scaleTones
    
    """
    指定したスケール、キーの構成音を返す。return ((KeyId, Pitch, 周波数),(...),...)
    """
    def Get(self, scaleKeyId, intervals):
        if scaleKeyId < 0 or self.__temperament.Denominator <= scaleKeyId: raise Exception(f'scaleKeyIdは0〜{self.__temperament.Denominator-1}の整数値にしてください。')
#        tones = list(self.__GetScaleTones(scaleKeyId, intervals))        
#        scales = []

#        return list(self.__GetScaleTones(scaleKeyId, intervals))
        self.__scaleTones.clear()
        for tone in self.__GetScaleTones(scaleKeyId, intervals): self.__scaleTones.append(tone)
        return self.__scaleTones
    
    def __GetScaleTones(self, scaleKeyId, intervals):
        keyId = scaleKeyId
        l = [0]
        l.extend(intervals)
        for interval in l:
            keyId += interval
#            yield self.__temperament.Cycle(keyId)
            k, p = self.__temperament.Cycle(keyId)
            yield (k, p, self.__temperament.GetFrequency(k, self.__temperament.BaseKeyPitch + p))
#            yield (keyId, self.__temperament.BaseKeyPitch + pitch, self.__temperament.GetFrequency(keyId, self.__temperament.BaseKeyPitch + pitch))
    
    """
    #スケールキー音の周波数を取得する（基音とスケールキー音との差を考えて）
    #self.__BaseKeyId = 9
    #scaleKeyId = 0: -9
    #scaleKeyId = 11: +2
    #(scaleKeyId - self.__temperament.BaseKeyId) / self.Denominator
    def __GetScaleKeyFrequency(self, scaleKeyId):
        return self.__temperament.BaseFrequency * math.pow(2, (scaleKeyId - self.__temperament.BaseKeyId) / self.Denominator)
    def __GetOctaveFrequency(self):
        for tone in range(self.__temperament.Denominator):
            yield self.__temperament.BaseFrequency * math.pow(2, (tone + scaleKeyId - self.__temperament.BaseKeyId) /
    """
if __name__ == '__main__':
    scale = Scale()
    print(scale.Get(0, ScaleIntervals.Major))
    print(scale.Get(11, ScaleIntervals.Major))
