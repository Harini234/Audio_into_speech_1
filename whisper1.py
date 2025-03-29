import whisper
import pyaudio
import wave
import numpy as np

def transcribe_audio(file_path: str, model_size: str = "base") -> str:
    """
    Transcribes an audio file using OpenAI's Whisper model.
    
    :param file_path: Path to the audio file.
    :param model_size: Whisper model size to load (default is "base").
    :return: Transcribed text from the audio file.
    """
    model = whisper.load_model(model_size)
    print("Model loaded successfully")
    result = model.transcribe(file_path)
    return result["text"]

def transcribe_live_audio(duration: int = 30, model_size: str = "base") -> str:
    """
    Captures live audio from the microphone and transcribes it using Whisper.
    
    :param duration: Duration of the recording in seconds (default is 5 seconds).
    :param model_size: Whisper model size to load (default is "base").
    :return: Transcribed text from the recorded audio.
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
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
    file_path = "live_audio1.wav"
    wave_file = wave.open(file_path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
    
    # Transcribe the recorded audio
    return transcribe_audio(file_path, model_size)

# Example usage
if __name__ == "__main__":
    audio_path = "/Users/hariniviswanathan/Desktop/Innovation/live_audio1.wav"
    transcription = transcribe_audio(audio_path)
    print("File Transcription:", transcription)
    
    live_transcription = transcribe_live_audio()
    print("Live Transcription:", live_transcription)