This project basically translates uploaded audio file into text and also converts live audio into text. This projects also predicts the mismatch based upon the translated text given in the text area.


For installing fastapi,yake,flask,whisper and pyaudio use the below command:-

pip3 install fastapi

pip3 install yake

pip3 install flask  

pip3 install whisper

pip3 install pyaduio


For running mismatchapi file you need to run the below command :-

uvicorn Match_Mismatch_API:app --host 127.0.0.1 --port 8092 --reload

For running uploadapi file you need to run the below command :-

uvicorn UploadFile_API:app --reload

For running app.py file we need to run the below command :-

python3 app.py
