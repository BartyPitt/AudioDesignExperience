import pyaudio
import numpy as np

class AudioGenerator():
    def __init__(self,volume = 0.5 , SampleRate = 44100):
        '''Sets up the AudioGenerator'''

        self.p = pyaudio.PyAudio()
        self.p.get_default_output_device_info()

        self.volume = volume    # range [0.0, 1.0]
        self.fs = SampleRate      # sampling rate, Hz, must be integer

    def PlaySineTone(self,duration ,frequency):
        '''Plays a sine tone'''

        f = frequency
        
        #duration = 1.0   # in seconds, may be float
        #f = 440.0        # sine frequency, Hz, may be float

        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(self.fs*duration)*f/self.fs)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        for i in range(10):
            stream = self.p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=self.fs,
                            output=True)

        # play. May repeat with different volume values (if done interactively) 
            stream.write(self.volume*samples)

        stream.write(self.volume*samples)
        stream.stop_stream()
        stream.close()

        p.terminate()

if __name__ == '__main__':
    TestGenerator = AudioGenerator()
    TestGenerator.PlaySineTone(2,440)
