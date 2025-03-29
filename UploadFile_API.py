from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import os
import whisper
import pyaudio
import wave
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def transcribe_audio(file_path: str, model_size: str = "base") -> str:
    """
    Transcribes an audio file using OpenAI's Whisper model.
    
    :param file_path: Path to the audio file.
    :param model_size: Whisper model size to load (default is "base").
    :return: Transcribed text from the audio file.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    print(result["text"])
    return result["text"]

@app.post("/convert-audio-to-text/")
async def convert_audio(file: UploadFile = File(...)):
    try:
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        converted_text = transcribe_audio(file_location)
        return {"converted_text": converted_text}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/record-live-audio/")
def record_live_audio(duration: int = 60, model_size: str = "base"):
    """
    Captures live audio from the microphone, saves it to a file, and transcribes it.
    
    :param duration: Duration of the recording in seconds (default is 10 seconds).
    :param model_size: Whisper model size to load (default is "base").
    :return: Transcribed text from the recorded audio.
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    file_path = "uploads/live_recording.wav"
    os.makedirs("uploads", exist_ok=True)
    
    audio = pyaudio.PyAudio()
    
    print("Recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recorded audio
    with wave.open(file_path, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
    
    # Transcribe the recorded audio
    converted_text = transcribe_audio(file_path, model_size)
    return {"converted_text": converted_text}





