import requests

API_BASE_URL = "https://localhost:5001"  # Local API replace

TRANSCRIPTION_API_URL = f"{API_BASE_URL}/upload"
VALIDATION_API_URL = f"{API_BASE_URL}/validate"

def upload_audio(file):
    files = {"file": (file.filename, file.stream, file.mimetype)}
    response = requests.post(TRANSCRIPTION_API_URL, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API Error: {response.status_code}"}

def validate_text(formdata):
    response = requests.post(VALIDATION_API_URL, json=formdata)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API Error: {response.status_code}"}
