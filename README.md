# Credit Risk Prediction

This project is split into:

- `Frontend/`: Streamlit app
- `Backend/`: FastAPI prediction API

The intended deployment is:

- Frontend on Streamlit Cloud
- Backend on Render

## Project Structure

```text
CRC_proj/
|-- Frontend/
|   |-- app.py
|   `-- requirements.txt
|-- Backend/
|   |-- app.py
|   |-- requirements.txt
|   `-- model (3).pkl
|-- render.yaml
`-- .env.example
```

## Local Run

### Backend

```bash
cd Backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

### Frontend

```bash
cd Frontend
pip install -r requirements.txt
streamlit run app.py
```

The frontend uses `BACKEND_URL` if provided. Without it, it falls back to `http://127.0.0.1:8000`.

## Deploy Backend on Render

You can deploy from the repo root using the included [render.yaml](/c:/Users/Nipun/CRC_proj/render.yaml:1).

Render settings:

- Service type: `Web Service`
- Root directory: `Backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

After deployment, copy the Render backend URL, for example:

```text
https://crc-backend.onrender.com
```

## Deploy Frontend on Streamlit Cloud

Use this repo and set the app file to:

```text
Frontend/app.py
```

In Streamlit Cloud, add this secret:

```toml
BACKEND_URL = "https://your-render-service.onrender.com"
```

The frontend will call:

```text
${BACKEND_URL}/predict
```

## Requirements Notes

- `Frontend/requirements.txt` only includes the packages the Streamlit app actually uses.
- `Backend/requirements.txt` includes `xgboost`, which is required for loading the trained model pickle.
- `uvicorn[standard]` is used for a more reliable production backend runtime on Render.

## Deployment Checklist

- Keep `Backend/model (3).pkl` committed in the repo so Render can load it.
- Set `BACKEND_URL` in Streamlit Cloud secrets.
- Confirm the Render backend root URL opens and returns a JSON health response.
- Make sure both `Frontend/requirements.txt` and `Backend/requirements.txt` are present in the deployed repo.

## Known Risk

The backend model file was trained with a dependency stack that likely includes `xgboost`. If Render fails while loading the model, the most likely cause is a version mismatch between the training environment and the deployed environment. In that case, pin the exact `xgboost` version used during training in `Backend/requirements.txt`.
