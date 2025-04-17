import whisper
import os
from datetime import datetime
from tkinter import filedialog, Tk

# === Load Whisper Model Once ===
print("Loading Whisper Large model...")
model = whisper.load_model("large")
print("Model loaded.")

def transcribe_audio(file_path):
    print(f"Transcribing {file_path}...")

    # Improved prompt to preserve symbols in medical transcriptions
    initial_prompt = (
        "This is a doctor's clinical note dictation. The transcription should preserve "
        "verbatim formatting and include symbols as spoken, such as slashes (/), dashes (-), "
        "colons (:), and decimal points (.). For example, blood pressure readings like "
        "'one-forty over seventy' should be transcribed as '140/70', and 'twenty dash five' "
        "should be '20-5'. Use numeric and symbolic representation where applicable. The content "
        "will include medical terminology like hypertension, diabetes, metformin, lisinopril, "
        "amoxicillin, pneumonia, etc."
    )

    result = model.transcribe(file_path, initial_prompt=initial_prompt)
    text = result["text"]
    lang = result["language"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filename = f"transcription_{timestamp}.txt"
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(f"[Detected Language: {lang}]\n\n")
        f.write(text)

    print(f"Transcription saved as {text_filename}")

# === File Selection Loop ===
print("\nSelect an audio file to transcribe or close the dialog to exit.\n")

while True:
    # Open file dialog to choose an audio file
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav *.m4a *.flac"),
            ("MP3", "*.mp3"),
            ("WAV", "*.wav"),
            ("M4A", "*.m4a"),
            ("FLAC", "*.flac"),
            ("All Files", "*.*")
        ]
    )
    root.destroy()

    if not file_path:
        print("No file selected. Exiting...")
        break

    transcribe_audio(file_path)
