from MusicTheory.temperament.EqualTemperament import EqualTemperament
from MusicTheory.temperament.PythagoreanTuning import PythagoreanTuning
from MusicTheory.temperament.JustIntonation import JustIntonation
from MusicTheory.temperament.eq12scales.ScaleIntervals import ScaleIntervals
from MusicTheory.temperament.eq12scales.Scale import Scale
import Wave.Player
import Wave.Sampler
import Wave.BaseWaveMaker
import Wave.WaveFile
import pathlib

def GetToneName(keyId): return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][keyId]
def GetScaleFilename(scaleName, keyId): return GetToneName(keyId).replace('#','+')+scaleName

class PlayAndMaker:
    #再生とファイル生成
    @staticmethod
    def Run(temperament, scale, scaleName):
        wm = Wave.BaseWaveMaker.BaseWaveMaker()
        sampler = Wave.Sampler.Sampler()
        wf = Wave.WaveFile.WaveFile()
#        p = Wave.Player.Player()
#        p.Open()

        #スケールの構成音生成
        wf.BasePath = pathlib.PurePath(f'../res/440/{temperament.__class__.__name__}/scales/{scaleName}/')
        wav = []
        for f0 in scale.Tones:
            wav.append(sampler.Sampling(wm.Sin(a=1, fs=8000, f0=f0[2], sec=0.5)))
        wf.Write(b''.join(wav), filename=GetToneName(scale.Key).replace('#','+'))
        wav.clear()
#        p.Close()

if __name__ == '__main__':
    #平均律とピタゴラス音律
    def run(temperament):
        if isinstance(temperament, EqualTemperament): temperament.Denominator = 12
        temperament.SetBaseKey(keyId=9, pitch=4, hz=440)
        scale = Scale(temperament)# scale.Temperament = et
        print(f'BaseKey: {GetToneName(temperament.BaseKeyId)}{temperament.BaseKeyPitch} {temperament.BaseFrequency}Hz')
        print(f'========== {temperament.Denominator} {temperament.__class__.__name__} ==========')
        for scale_name in ['Major', 'Minor', 'Diminished', 'HarmonicMinor', 'MelodicMinor', 'MajorPentaTonic', 'MinorPentaTonic', 'BlueNote']:
            print('----------', scale_name, '----------')
            scale.Intervals = getattr(ScaleIntervals, scale_name)
            for scaleKeyId in range(temperament.Denominator):
                scale.Key = scaleKeyId
                for tone in scale.Tones: print('{:2}'.format(GetToneName(tone[0])), end=' ')        
                print()
                PlayAndMaker.Run(temperament, scale, scale_name)
    run(EqualTemperament())
    run(PythagoreanTuning())

    #純正律
    def PlayAndMakeJustIntonation(temperaments):
        if not isinstance(temperaments, JustIntonation): raise Exception(f'このメソッドの引数temperamentsはJustIntonation型のみ対応です。')
        wm = Wave.BaseWaveMaker.BaseWaveMaker()
        sampler = Wave.Sampler.Sampler()
        wf = Wave.WaveFile.WaveFile()
        wf.BasePath = pathlib.PurePath(f'../res/440/JustIntonation/scales/{temperaments.Scale}')
        wav = []
        for f0 in temperaments.Frequencies:
            wav.append(sampler.Sampling(wm.Sin(a=1, fs=8000, f0=f0, sec=0.5)))
        wf.Write(b''.join(wav), filename=GetScaleFilename(temperaments.Scale, temperaments.BaseKeyId))    

    temperament = JustIntonation()
    print(f'BaseKey: {GetToneName(temperament.BaseKeyId)}{temperament.BaseKeyPitch} {temperament.BaseFrequency}Hz')
    print(f'========== {temperament.__class__.__name__} ==========')
    for scale_name in ['Major', 'Minor']:
        temperament.Scale = scale_name
        print('----------',temperament.Scale,'----------')
        for key in range(12):
            temperament.BaseKeyId = key
            print('key:{:2} {}'.format(GetToneName(temperament.BaseKeyId), temperament.Frequencies))
            PlayAndMakeJustIntonation(temperament)

