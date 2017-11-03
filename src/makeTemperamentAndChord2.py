#!python3.6
#coding:utf-8
import time
import Wave.Player
import Wave.Sampler
import Wave.BaseWaveMaker
import Wave.WaveFile
import MusicTheory.temperament.EqualTemperament
import MusicTheory.temperament.JustIntonation
import MusicTheory.temperament.PythagoreanTuning
from MusicTheory.temperament.eq12scales.ScaleIntervals import ScaleIntervals
#import MusicTheory.temperament.eq12scales.ScaleIntervals
import MusicTheory.temperament.eq12scales.Scale
import pathlib
import numpy

def GetKeyName(keyId): return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][keyId]
def GetScaleFilename(scaleName, keyId): return GetKeyName(keyId).replace('#','+')+scaleName

#音律の構成音データ生成
class ScaleTonesMaker:
    def __init__(self, wm:Wave.BaseWaveMaker.BaseWaveMaker):
        self.__wm = wm

#    def Scales(self, temperament):
#        for f0 in temperament.Frequencies:
#            yield self.__wm.Sin(a=1, fs=8000, f0=f0, sec=0.5)

    def Scales(self, temperament, keyId, intervals):
        scale = MusicTheory.temperament.eq12scales.Scale.Scale(temperament)
        for tones in scale.Get(keyId, intervals):
            yield self.__wm.Sin(a=1, fs=8000, f0=tones[2], sec=0.5)

    """
    def Scales(self, temperament, intervals):
        scale = MusicTheory.temperament.eq12scales.Scale.Scale(temperament)
        for keyId in range(temperament.Denominator):
#            print(scale.Get(keyId, intervals)[2][2])
            yield self.__wm.Sin(a=1, fs=8000, f0=scale.Get(keyId, intervals)[2][2], sec=0.5)
#            yield scale.Get(keyId, intervals)[2][2]
    """

#和音データ生成
class ChordMaker:
    def __init__(self, wm:Wave.BaseWaveMaker.BaseWaveMaker):
        self.__wm = wm

    #パワーコード（基音＋完全5度）
    def PowerChord(self, temperament):
        src = []
        src.append(self.__wm.Sin(a=1, fs=8000, f0=temperament.Frequencies[0], sec=4))
        src.append(self.__wm.Sin(a=1, fs=8000, f0=temperament.Frequencies[4], sec=4))
        res = numpy.array([0] * len(src[0])) #ダミーの空配列
        return self.__Addition(src)

    #長三和音（基音＋長3度＋完全5度）
    def MajorTriadChord(self, temperament):
        src = []
        src.append(self.__wm.Sin(a=1, fs=8000, f0=temperament.Frequencies[0], sec=4))
        src.append(self.__wm.Sin(a=1, fs=8000, f0=temperament.Frequencies[2], sec=4))
        src.append(self.__wm.Sin(a=1, fs=8000, f0=temperament.Frequencies[4], sec=4))
        res = numpy.array([0] * len(src[0])) #ダミーの空配列
        return self.__Addition(src)
        
    #波形の加算とクリッピング
    def __Addition(self, src):
        res = numpy.array([0] * len(src[0])) #ダミーの空配列
        for s in src:
            res = res + s
            res *= 0.5
        return res

    #四和音以上は平均律のときに有効な和音らしい。純正律は三和音が最も美しく響く音律らしい。

class PlayAndMaker:
    #再生とファイル生成
    @staticmethod
    def Run(temperament):
        wm = Wave.BaseWaveMaker.BaseWaveMaker()
        sampler = Wave.Sampler.Sampler()
        ji = MusicTheory.temperament.JustIntonation.JustIntonation()
        wf = Wave.WaveFile.WaveFile()
        p = Wave.Player.Player()
        p.Open()

        print(f'BaseFrequency: {temperament.BaseFrequency} Hz')
        print(temperament.Frequencies)
        """
        #コード生成
#        p.Play(sampler.Sampling(PATTERNS[pattern](wm, ji)))
        cm = ChordMaker(wm)
        wf.BasePath = pathlib.PurePath(f'../res/chords/power/{temperament.__class__.__name__}/')
        wf.Write(sampler.Sampling(cm.PowerChord(temperament)), filename=f'{temperament.BaseFrequency}')
        wf.BasePath = pathlib.PurePath(f'../res/chords/major/{temperament.__class__.__name__}/')
        wf.Write(sampler.Sampling(cm.PowerChord(temperament)), filename=f'{temperament.BaseFrequency}')
        """

        #スケールの構成音生成
        print('**********', f'{temperament.__class__.__name__} {temperament.BaseFrequency}Hz' , '**********')
        sm = ScaleTonesMaker(wm)
        for scaleName in ['Major','Minor','Diminished','HarmonicMinor','MelodicMinor','MajorPentaTonic','MinorPentaTonic','BlueNote','Chromatic']:
            wf.BasePath = pathlib.PurePath(f'../res/{temperament.BaseFrequency}/scales/{scaleName}/{temperament.__class__.__name__}/')
            print('=======', scaleName, '=======')
            for scaleKeyId in range(0, 1):#12調すべては多すぎるのでCのみにした。
#            for scaleKeyId in range(temperament.Denominator):
                print('-----', GetKeyName(scaleKeyId), '-----')
                wf.Write(b''.join([sampler.Sampling(f) for f in sm.Scales(temperament, scaleKeyId, getattr(ScaleIntervals, scaleName))]), filename=GetScaleFilename(scaleName, scaleKeyId))

        p.Close()


for temperament in [
    MusicTheory.temperament.EqualTemperament.EqualTemperament(), 
#    MusicTheory.temperament.JustIntonation.JustIntonation(), 
    MusicTheory.temperament.PythagoreanTuning.PythagoreanTuning()]:
    print('---------- ' + temperament.__class__.__name__ + ' ----------')
    for baseF in [440]:
#    for baseF in [432, 440, 444]:
        temperament.BaseFrequency = baseF
        PlayAndMaker.Run(temperament)
