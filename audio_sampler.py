import sys
import pyaudio
import wave
import thread

CHUNK_SIZE = 1024

SAMPLES = {
    'snare': 'samples/snare.wav',
    'tom':   'samples/tom.wav'
}


class Sound:
    def __init__(self, filepath):
        self.filepath = filepath
        self.channels = []
        self.rate = None
        self.samp_width = None
        self.data = []

        self.load()

    def load(self):
        print 'loading sample ' + self.filepath
        sound_file = wave.open(self.filepath, 'rb')
        print 'opened'

        self.channels = sound_file.getnchannels()
        self.rate = sound_file.getframerate()
        self.samp_width = sound_file.getsampwidth()
        print 'meta data collected'

        print 'reading...'
        data = sound_file.readframes(CHUNK_SIZE)
        while len(data) > 0:
            # print 'reading...'
            data = sound_file.readframes(CHUNK_SIZE)
            self.data.append(data)


class DrumSampler:
    def __init__(self):
        self.samples = {}
        self.audio = pyaudio.PyAudio()

        self.load_samples()

    def load_samples(self):
        for sample_name, sample_path in SAMPLES.iteritems():
            self.samples[sample_name] = Sound(sample_path)

    def play(self, sample_name):
        print 'playing ' + sample_name
        thread.start_new_thread(self.play_sample, (sample_name))

    def play_sample(sample_name):
        sample = self.samples[sample_name]

        stream = audio.open(
            format = audio.get_format_from_width(sample.width),
            channels = sample.channels,
            rate = sample.rate,
            output = True
        )

        for data in sample.data:
            stream.write(data)

        stream.stop_stream()
        stream.close()


if __name__ == '__main__':
    print 'starting sampler'
    drum_sampler = DrumSampler()
    print 'started sampler'

    drum_sampler.play('snare')
    drum_sampler.play('snare')
    drum_sampler.play('tom')
    drum_sampler.play('snare')
    drum_sampler.play('snare')
    drum_sampler.play('tom')
    drum_sampler.play('snare')
    drum_sampler.play('snare')
    drum_sampler.play('tom')
    drum_sampler.play('snare')
    drum_sampler.play('snare')
    drum_sampler.play('tom')
    drum_sampler.play('snare')
    drum_sampler.play('snare')
    drum_sampler.play('tom')

    while(True):
        pass
