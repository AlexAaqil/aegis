# AEGIS BIOMETRIC API — MOBILE INTEGRATION GUIDE

## Purpose
Enable mobile developers to capture a user’s **face** and **voice** and send them to the backend for biometric enrollment and verification.  
The backend handles all processing, encryption, and matching — the mobile app only uploads files.

---

## Base URL

**Local Development (default):**

http://127.0.0.1:8000


---

## API OVERVIEW

| Endpoint | Method | Purpose |
|-----------|---------|---------|
| `/biometric/enroll` | `POST` | Register a new biometric sample |
| `/biometric/verify` | `POST` | Compare a new sample with an enrolled one |
| `/health` | `GET` | Check backend service status |

---

## 1. ENROLL BIOMETRIC

**Endpoint**

POST /biometric/enroll


**Description:**  
Registers a new face or voice sample for the given user.

| Field | Type | Example | Description |
|-------|------|----------|-------------|
| `user_id` | Integer | `1` | ID of the user being enrolled |
| `modality` | String | `"face"` or `"voice"` | Type of biometric sample |
| `file` | File | (captured file) | Image (`JPEG/PNG`) or audio (`WAV`) |

**Example Request (using curl):**
```bash
curl -X POST http://127.0.0.1:8000/biometric/enroll \
  -F "user_id=1" \
  -F "modality=face" \
  -F "file=@/path/to/face.jpg"
```

Example Response:
```
{
  "user_id": 1,
  "modality": "face",
  "message": "face biometric enrolled",
  "path": "data/biometrics/user_1_face.bio"
}
```

## 2. VERIFY BIOMETRIC

Endpoint

POST /biometric/verify

Description:
Verifies a captured face or voice sample against the enrolled record.

Field	Type	Example	Description
user_id	Integer	1	ID of the user being verified
modality	String	"face" or "voice"	Type of biometric sample
file	File	(captured file)	Image (JPEG/PNG) or audio (WAV)


Example Request using Curl:
```
curl -X POST http://127.0.0.1:8000/biometric/verify \
  -F "user_id=1" \
  -F "modality=voice" \
  -F "file=@/path/to/voice.wav"
```

Example Response:
```
{
  "user_id": 1,
  "modality": "voice",
  "verified": true,
  "similarity": 0.94
}
```

RESPONSE DETAILS

- "verified": true → match is above the threshold (0.85)
- "similarity" → cosine similarity score between 0 and 1


FRONTEND DEVELOPER NOTES (Mobile)

Use your camera/mic capture APIs (e.g. react-native-camera, expo-av, MediaRecorder, etc.) to record.

Send the captured file using multipart/form-data.

You do not handle encryption or matching — backend takes care of that.

For real-time capture & feedback, you can poll or show the similarity score returned.