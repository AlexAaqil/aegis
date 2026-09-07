import cv2
import numpy as np
from pathlib import Path
from app.security import fernet
from io import BytesIO
from PIL import Image
import tempfile
import wave
from skimage.feature import local_binary_pattern

BIOMETRIC_DIR = Path("./data/biometrics")
BIOMETRIC_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------
# FACE BIOMETRIC
# --------------------------
# def extract_face_vector(image_bytes: bytes) -> np.ndarray:
#     """Convert a face image to a simple normalized color histogram feature."""
#     image = Image.open(BytesIO(image_bytes)).convert("RGB")
#     img = np.array(image)
#     img = cv2.resize(img, (100, 100))
#     hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8],
#                         [0, 256, 0, 256, 0, 256])
#     hist = cv2.normalize(hist, hist).flatten()
#     return hist

def extract_face_vector(image_bytes: bytes) -> np.ndarray:
    image = Image.open(BytesIO(image_bytes)).convert("L")
    img = np.array(image)
    img = cv2.resize(img, (100, 100))
    lbp = local_binary_pattern(img, P=8, R=1, method="uniform")
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(59))
    hist = hist.astype("float")
    hist /= np.linalg.norm(hist) or 1.0
    return hist



# --------------------------
# VOICE BIOMETRIC
# --------------------------
def extract_voice_vector(audio_bytes: bytes) -> np.ndarray:
    """Extract basic energy features from voice waveform."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        with wave.open(tmp.name, "rb") as wf:
            frames = wf.readframes(-1)
            waveform = np.frombuffer(frames, dtype=np.int16)
    if len(waveform) == 0:
        raise ValueError("Empty audio input")
    energy = np.abs(waveform)
    hist, _ = np.histogram(energy, bins=64, range=(0, np.max(energy)))
    hist = hist / np.linalg.norm(hist)
    return hist


# --------------------------
# ENROLL + VERIFY
# --------------------------
def enroll_user_biometric(user_id: int, sample_bytes: bytes, modality: str):
    """Enroll a user's biometric sample (face or voice)."""
    if modality == "face":
        vector = extract_face_vector(sample_bytes)
    elif modality == "voice":
        vector = extract_voice_vector(sample_bytes)
    else:
        raise ValueError("Unsupported modality")

    encrypted = fernet.encrypt(vector.tobytes())
    path = BIOMETRIC_DIR / f"user_{user_id}_{modality}.bio"
    path.write_bytes(encrypted)
    return {"message": f"{modality} biometric enrolled", "path": str(path)}


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute safe cosine similarity, trimming to same length."""
    min_len = min(len(vec1), len(vec2))
    if min_len == 0:
        return 0.0
    v1, v2 = vec1[:min_len], vec2[:min_len]
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2)) or 1.0
    return float(np.dot(v1, v2) / denom)


def verify_user_biometric(user_id: int, sample_bytes: bytes, modality: str):
    """Verify new biometric sample against stored one."""
    path = BIOMETRIC_DIR / f"user_{user_id}_{modality}.bio"
    if not path.exists():
        return {"verified": False, "reason": "no enrollment"}

    # decrypt and rebuild stored vector
    stored_vector = np.frombuffer(
        fernet.decrypt(path.read_bytes()), dtype=np.float64
    )

    # extract new vector
    if modality == "face":
        new_vector = extract_face_vector(sample_bytes)
    elif modality == "voice":
        new_vector = extract_voice_vector(sample_bytes)
    else:
        raise ValueError("Unsupported modality")

    # --- FIX: Align dimensions and compute cosine similarity ---
    similarity = cosine_similarity(stored_vector, new_vector)

    verified = similarity > 0.85
    print(
        f"[DEBUG] compared {modality} vectors "
        f"(stored={len(stored_vector)}, new={len(new_vector)}, sim={similarity:.3f})"
    )

    return {"verified": verified, "similarity": similarity}

