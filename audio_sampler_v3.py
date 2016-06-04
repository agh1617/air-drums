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


wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()


class DrumSampler:
    def __init__(self):
        self.samples = {}
        self.audio = pyaudio.PyAudio()

        self.load_samples()

    def load_samples(self):
        for sample_name, sample_path in SAMPLES.iteritems():
            self.samples[sample_name] = Sound(sample_path)

    def play_sample(self, sample_name):
        sample = self.sapmles[sample_name]

        def callback(in_data, frame_count, time_info, status):
            data = sample.sound_file.readframes(frame_count)
            return (data, self.audio.paContinue)

        stream = self.audio.open(
            format=self.audio.get_format_from_width(sample.width),
            channels=sample.channels,
            rate=sample.rate,
            output=True,
            stream_callback=callback
        )

        stream.start_stream()

        w


    def play(self, sample_name):
        thread.start_new_thread(self.play_sample, sample_name)

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
