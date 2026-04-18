from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
import joblib
import pandas as pd

app = FastAPI()

# Load the model from the backend directory so startup works from any cwd.
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model (3).pkl"
model: Any | None = None
model_load_error: str | None = None


def load_model() -> Any | None:
    global model, model_load_error

    if model is not None:
        return model

    if not MODEL_PATH.exists():
        model_load_error = f"Model file not found at: {MODEL_PATH}"
        return None

    try:
        model = joblib.load(MODEL_PATH)
        model_load_error = None
        return model
    except Exception as exc:
        model_load_error = (
            f"{exc}. If this is a scikit-learn pickle compatibility issue, "
            "install the training-time version from Backend/requirements.txt."
        )
        return None


load_model()

@app.get("/")
def home():
    return {
        "message": "Loan Prediction API Running",
        "model_loaded": model is not None,
        "model_path": str(MODEL_PATH),
        "model_error": model_load_error,
    }


@app.post("/predict")
def predict(data: dict):
    loaded_model = load_model()

    if loaded_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model could not be loaded. {model_load_error}",
        )

    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([data])

        # Prediction
        proba = loaded_model.predict_proba(input_data)[:, 1]
        prediction = (proba > 0.4).astype(int)

        return {
            "prediction": int(prediction[0]),
            "probability": float(proba[0])
        }

    except Exception as e:
        return {"error": str(e)}
