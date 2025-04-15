import pyaudio
import wave
import whisper
import keyboard
import time
import os
from datetime import datetime

# === Load Whisper Model Once ===
print("Loading Whisper Large model...")
model = whisper.load_model("large")
print("Model loaded.")

# === Audio Settings ===
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    recording = True
    paused = False

    print("Recording... Press [W] to pause/resume, [Q] to stop.")

    while recording:
        if keyboard.is_pressed("q"):
            print("Stopping recording...")
            break
        elif keyboard.is_pressed("w"):
            paused = not paused
            print("Paused." if paused else "Resumed.")
            time.sleep(0.5)  # debounce

        if not paused:
            data = stream.read(CHUNK)
            frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {filename}")
    return filename, timestamp

def transcribe_audio(file_path, timestamp):
    print(f"Transcribing {file_path}...")

    # Add the initial_prompt for medical transcription
    initial_prompt = (
        "This is a doctor's clinical note dictation. The transcription will "
        "contain medical terminology including symptoms, diagnoses, medications, "
        "and patient conditions. Expect terms like hypertension, diabetes, "
        "metformin, lisinopril, amoxicillin, pneumonia, etc."
    )

    result = model.transcribe(file_path, initial_prompt=initial_prompt)
    text = result["text"]
    lang = result["language"]

    # Save transcription to a .txt file with the timestamp
    text_filename = f"transcription_{timestamp}.txt"
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(f"[Detected Language: {lang}]\n\n")
        f.write(text)

    print(f"Transcription saved as {text_filename}")

# === Main Loop ===
print("\nPress [R] to start a new recording, [ESC] to exit.\n")

while True:
    if keyboard.is_pressed("r"):
        audio_path, timestamp = record_audio()
        transcribe_audio(audio_path, timestamp)
        print("\nPress [R] to start another recording, [ESC] to exit.\n")
        time.sleep(1)  # avoid double-trigger
    elif keyboard.is_pressed("esc"):
        print("Exiting...")
        break


