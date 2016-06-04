import pyaudio
import wave

SAMPLES_DIR = 'samples'
SAMPLES = ['snare', 'tom']


pyaudio = pyaudio.PyAudio()


class SoundSample:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sound_file = None

        self.width = None
        self.channels = []
        self.rate = None

        self.load()

        self.stream = None

    def load(self):
        sound_file = wave.open(self.filepath, 'rb')

        self.width = sound_file.getsampwidth()
        self.channels = sound_file.getnchannels()
        self.rate = sound_file.getframerate()

        self.sound_file = sound_file

    def play(self):
        def callback(in_data, frame_count, time_info, status):
            data = self.file.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = pyaudio.open(
            format=pyaudio.get_format_from_width(self.width),
            channels=self.channels,
            rate=self.rate,
            output=True,
            stream_callback=callback
        )

        stream.start_stream()
        self.stream = stream


if __name__ == '__main__':
    sample = SoundSample('samples/tom.wav')
    sample.play()

    while True:
        pass
