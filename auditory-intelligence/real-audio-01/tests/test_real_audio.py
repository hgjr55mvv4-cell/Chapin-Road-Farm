import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from real_audio import features,excerpt,goertzel,cosine,classify,mix,train,RATE

class RealAudioDevTests(unittest.TestCase):
    def test_goertzel(self):
        x=[.5*math.sin(2*math.pi*400*i/RATE) for i in range(800)]
        self.assertGreater(goertzel(x,400),goertzel(x,250)*100)
    def test_features(self):
        x=[.2*math.sin(2*math.pi*400*i/RATE) for i in range(6400)]
        self.assertEqual(len(features(x)),11)
    def test_energy_segment_determinism(self):
        x=[0.]*6400+[.1]*6400+[0.]*6400
        segment,start=excerpt(x)
        self.assertEqual(start,.75)
        self.assertEqual(len(segment),6400)
    def test_distinct_training_sources_required(self):
        a=[.1]*6400;b=[.2]*6400
        info={'a':{'role':'train','filename':'a','category':'dog','source_id':'1'},
              'b':{'role':'eval','filename':'b','category':'chainsaw','source_id':'2'}}
        with self.assertRaises(ValueError):train({'a':(a,0,''),'b':(b,0,'')},info)
    def test_known_slot_mixing(self):
        signal=[.1]*6400
        mixed,clipped=mix(('dog','none'),{'dog':signal,'chainsaw':signal},[0.]*6400,.5)
        self.assertFalse(clipped)
        self.assertGreater(sum(abs(v) for v in mixed[int(.4*RATE):int(1.2*RATE)]),100)
        self.assertEqual(sum(abs(v) for v in mixed[int(1.6*RATE):int(2.4*RATE)]),0)
    def test_cosine(self):
        self.assertAlmostEqual(cosine([1.,0.],[1.,0.]),1,places=8)
        self.assertAlmostEqual(cosine([1.,0.],[0.,1.]),0,places=8)
    def test_quiet_input(self):
        proto={'dog':[1.]*11,'chainsaw':[0.]*11}
        self.assertEqual(classify([0.]*6400,proto),'none')
    def test_real_files_required(self):
        from real_audio import evaluate
        with self.assertRaises(FileNotFoundError):evaluate('missing_corpus','sources.json')

if __name__=="__main__":unittest.main()
