from fastapi import APIRouter, UploadFile, File, Form
from app.services.biometric_service import enroll_user_biometric, verify_user_biometric

router = APIRouter(prefix="/biometric", tags=["Biometric"])

@router.post("/enroll")
async def enroll_biometric(user_id: int = Form(...), modality: str = Form(...), file: UploadFile = File(...)):
    data = await file.read()
    result = enroll_user_biometric(user_id, data, modality)
    return {"user_id": user_id, "modality": modality, **result}

@router.post("/verify")
async def verify_biometric(user_id: int = Form(...), modality: str = Form(...), file: UploadFile = File(...)):
    data = await file.read()
    result = verify_user_biometric(user_id, data, modality)
    return {"user_id": user_id, "modality": modality, **result}

