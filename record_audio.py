import pyaudio
import wave

# Settings for recording
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono
RATE = 44100  # 44.1kHz sample rate
CHUNK = 1024  # Chunk size
RECORD_SECONDS = 5  # How long to record (seconds)
OUTPUT_FILENAME = "recorded_audio.wav"

# Initialize audio stream
audio = pyaudio.PyAudio()

# Start recording
print("Recording...")
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# Close stream and save file
print("Recording finished.")
stream.stop_stream()
stream.close()
audio.terminate()

with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {OUTPUT_FILENAME}")
