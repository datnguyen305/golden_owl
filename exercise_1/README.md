# Cat and Dog Image Classification

This project classifies an input image as either `cat` or `dog`.

The solution includes:

- `result.ipynb`: training and experiment notebook
- `demo.ipynb`: notebook demo for image prediction
- `backend/`: FastAPI prediction API
- `frontend/`: static web UI
- `report.md`: short solution report

## 1. Environment Requirements

### For Running the API Locally

Use Python 3.11.

Install dependencies:

```bash
cd exercise_1/backend
pip install -r requirements.txt
```

## 2. How to Run Prediction in a Notebook

Open:

```text
exercise_1/demo.ipynb
```

Run all cells.

The notebook loads the default trained model and provides:

```python
predict_image_path("/path/to/image.jpg")
```

Example output:

```text
Prediction: dog
Confidence: 0.9700
```

## 3. How to Run the API Locally

Start the backend:

```bash
cd exercise_1/backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

Check that the API is running:

```bash
curl http://localhost:8000/health
```

Classify an image:

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@/path/to/image.jpg"
```

Example response:

```json
{
  "prediction": "dog",
  "confidence": 0.97,
  "scores": {
    "cat": 0.03,
    "dog": 0.97
  }
}
```

## 4. Web Demo

The frontend is a static website deployed on Netlify.

The backend is deployed on Render and Netlify:

```
https://goldenowldemo.netlify.app/
```

## 5. Notes

The training experiments include ViT-Small, but the deployed API uses MobileNetV3-Small because it is lightweight and fits Render free-tier memory limits better.
