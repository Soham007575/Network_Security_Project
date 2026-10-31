
import os
import sys

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREPROCESSOR_PATH = os.path.join(
    BASE_DIR, "final_model", "preprocessor.pkl"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "final_model", "model.pkl"
)

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


# Initialize FastAPI
app = FastAPI(
    title="Phishing Website Detection System",
    description="Machine Learning Based Network Security System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


# HTML templates
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# Load model and make predictions
def run_model(df: pd.DataFrame):

    # Remove target column if present
    if "Result" in df.columns:
        df = df.drop(columns=["Result"])

    # Load saved preprocessing and model objects
    preprocessor = load_object(PREPROCESSOR_PATH)
    final_model = load_object(MODEL_PATH)

    # Initialize network model
    network_model = NetworkModel(
        preprocessor=preprocessor,
        model=final_model
    )

    # Generate predictions
    predictions = network_model.predict(df)

    # Convert predictions to a flat NumPy array
    predictions = np.asarray(predictions).reshape(-1)

    # Debug information in Vercel Runtime Logs
    print("Raw predictions:", repr(predictions))
    print("Prediction shape:", predictions.shape)
    print("Prediction dtype:", predictions.dtype)

    return df, predictions


# Convert model prediction to readable label
def get_prediction_label(prediction):

    # Convert NumPy scalar to regular Python scalar
    if isinstance(prediction, np.generic):
        prediction = prediction.item()

    # Handle numeric labels
    try:
        prediction = int(prediction)
    except (TypeError, ValueError, OverflowError):
        return "Unknown"

    # Expected model encoding:
    #  1  = Legitimate
    # -1  = Phishing
    if prediction == 1:
        return "Legitimate"

    elif prediction == -1:
        return "Phishing"

    else:
        return "Unknown"


# Home page
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# Optional UI route
@app.get("/ui")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# CSV prediction route: Returns HTML table
@app.post("/predict")
async def predict_route(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        df = pd.read_csv(file.file)

        df, y_pred = run_model(df)

        labels = [
            get_prediction_label(prediction)
            for prediction in y_pred
        ]

        df["Prediction"] = labels

        table_html = df.to_html(
            classes="table table-striped",
            index=False
        )

        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={
                "table": table_html
            }
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# CSV prediction route: Returns readable JSON
@app.post("/predict_json")
async def predict_json(
    file: UploadFile = File(...)
):
    try:
        df = pd.read_csv(file.file)

        # Preserve website information if available
        website_column = next(
            (
                column for column in df.columns
                if column.lower() in ["url", "website", "domain"]
            ),
            None
        )

        df, y_pred = run_model(df)

        labels = [
            get_prediction_label(prediction)
            for prediction in y_pred
        ]

        results = []

        for index, prediction in enumerate(labels):

            # Display URL/domain when available
            if website_column and website_column in df.columns:
                website = str(df.iloc[index][website_column])
            else:
                website = f"Website #{index + 1}"

            if prediction == "Phishing":
                message = "Potentially malicious website detected"

            elif prediction == "Legitimate":
                message = "Classified as legitimate"

            else:
                message = "Prediction could not be identified"

            results.append({
                "website": website,
                "prediction": prediction,
                "message": message
            })

        return {
            "total_scanned": len(results),
            "phishing_count": labels.count("Phishing"),
            "legitimate_count": labels.count("Legitimate"),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process this file: {e}"
        )


# Run application locally
if __name__ == "__main__":
    app_run(
        app,
        host="0.0.0.0",
        port=8000
    )
