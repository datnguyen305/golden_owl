import os
from pathlib import Path
from typing import Dict

import timm
import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from torchvision import transforms


IMG_SIZE = 224
MODEL_NAME = os.getenv("MODEL_NAME", "vit_small_patch16_224")
CHECKPOINT_PATH = Path(
    os.getenv(
        "CHECKPOINT_PATH",
        Path(__file__).resolve().parents[1] / "models_checkpoint" / "vit_small_head.pt",
    )
)
CLASS_NAMES = ["cat", "dog"]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


app = FastAPI(title="Cat vs Dog Classifier")

allowed_origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",")],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

preprocess = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

model = None


def load_checkpoint(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    try:
        return torch.load(path, map_location=DEVICE, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=DEVICE)


def extract_state_dict(checkpoint):
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        return checkpoint["model_state"]
    if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
        return checkpoint["state_dict"]
    return checkpoint


def create_model():
    classifier = timm.create_model(MODEL_NAME, pretrained=False, num_classes=len(CLASS_NAMES))
    checkpoint = load_checkpoint(CHECKPOINT_PATH)
    classifier.load_state_dict(extract_state_dict(checkpoint))
    classifier.to(DEVICE)
    classifier.eval()
    return classifier


@app.on_event("startup")
def startup_event():
    global model
    model = create_model()


@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "checkpoint": str(CHECKPOINT_PATH),
        "device": str(DEVICE),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is still loading")

    try:
        image = Image.open(file.file).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image") from exc

    with torch.no_grad():
        x = preprocess(image).unsqueeze(0).to(DEVICE)
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0].detach().cpu()

    scores = {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))}
    label = max(scores, key=scores.get)
    return {
        "prediction": label,
        "confidence": scores[label],
        "scores": scores,
    }
