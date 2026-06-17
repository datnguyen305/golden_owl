# Render API

This FastAPI service loads `models_checkpoint/vit_small_head.pt` by default and exposes:

- `GET /health`
- `POST /predict` with multipart field `file`

Render start command:

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

Optional environment variables:

- `CHECKPOINT_PATH`: absolute or relative checkpoint path
- `MODEL_NAME`: defaults to `vit_small_patch16_224`
- `CORS_ORIGINS`: comma-separated allowed frontend origins, defaults to `*`
