# Render API

This FastAPI service loads `models_checkpoint/mobilenet_v3_small_head.pt` by default on Render to fit the free instance memory limit. The ViT checkpoint is still available for notebook/Colab demos.

- `GET /health`
- `POST /predict` with multipart field `file`

Render start command:

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

Optional environment variables:

- `CHECKPOINT_PATH`: absolute or relative checkpoint path
- `MODEL_NAME`: defaults to `mobilenet_v3_small`
- `CORS_ORIGINS`: comma-separated allowed frontend origins, defaults to `*`
