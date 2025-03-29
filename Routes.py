from flask import Flask, render_template, request, jsonify
import api
from echo import app

@app.route("/", methods=["GET", "POST"])
def default_home():
    return render_template("home.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No File Uploaded"}), 400

    file = request.files["file"]
    transcription_result = api.upload_audio(file)

    return jsonify(transcription_result)

@app.route("/validate", methods=["POST"])
def validate_transcription():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    print(data)
    validation_result = api.validate_text(data)

    return jsonify(validation_result)
