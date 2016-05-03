import sys
import pyaudio
import wave

CHUNK_SIZE = 1024

def play_sample(sample_filepath, chunk_size=CHUNK_SIZE):
    '''
    Play (on the attached system sound device) the WAV file
    named sample_filepath.
    '''

    try:
        print 'Trying to play file ' + sample_filepath
        wf = wave.open(sample_filepath, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + sample_filepath + '\n' + \
        str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + sample_filepath + '\n' + \
        str(eofe) + '. Skipping.\n')
        return

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    p.terminate()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python audio_sampler.py sample_path'
        exit(1)

    play_sample(sys.argv[1])
