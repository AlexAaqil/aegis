import cv2
import numpy as np
import pyaudio
import wave
import requests
import tempfile

API_URL = "http://127.0.0.1:8000/biometric/enroll"
VERIFY_URL = "http://127.0.0.1:8000/biometric/verify"
USER_ID = 1


# ----------------------------
# FACE CAPTURE
# ----------------------------
def capture_face():
    print("Opening webcam... Press SPACE to capture or ESC to cancel.")
    cap = cv2.VideoCapture(0)
    face_captured = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found.")
            break

        cv2.imshow("Face Capture - Press SPACE to capture", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            print("Cancelled.")
            break
        elif key == 32:  # SPACE
            face_captured = frame
            print("Face captured.")
            break

    cap.release()
    cv2.destroyAllWindows()

    if face_captured is not None:
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cv2.imwrite(tmp_file.name, face_captured)
        print(f"Saved captured face to {tmp_file.name}")
        return tmp_file.name
    else:
        return None


# ----------------------------
# VOICE CAPTURE
# ----------------------------
def capture_voice(seconds=3):
    print(f"Recording {seconds} seconds of audio...")
    chunk = 1024
    fmt = pyaudio.paInt16
    channels = 1
    rate = 16000

    audio = pyaudio.PyAudio()
    stream = audio.open(format=fmt, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf = wave.open(tmp_file.name, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(fmt))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"Voice saved at {tmp_file.name}")
    return tmp_file.name


# ----------------------------
# SEND TO API
# ----------------------------
def upload(file_path, modality):
    with open(file_path, "rb") as f:
        res = requests.post(
            API_URL,
            files={"file": f},
            data={"user_id": USER_ID, "modality": modality},
        )
    print("API Response:", res.status_code, res.json())


def verify(file_path, modality):
    with open(file_path, "rb") as f:
        res = requests.post(
            VERIFY_URL,
            files={"file": f},
            data={"user_id": USER_ID, "modality": modality},
        )
    print("Verify Response:", res.status_code, res.json())


if __name__ == "__main__":
    print("=== FACE ENROLLMENT ===")
    face_path = capture_face()
    if face_path:
        upload(face_path, "face")
        verify(face_path, "face")

    print("\n=== VOICE ENROLLMENT ===")
    voice_path = capture_voice()
    if voice_path:
        upload(voice_path, "voice")
        verify(voice_path, "voice")

    print("\nDone.")
