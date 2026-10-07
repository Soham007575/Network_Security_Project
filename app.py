import sys
import pandas as pd

from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from uvicorn import run as app_run

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# CORS
# --------------------------------------------------

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory="./templates"
)


# --------------------------------------------------
# Home Route
# --------------------------------------------------

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


# --------------------------------------------------
# Prediction Route
# --------------------------------------------------

@app.post("/predict")
async def predict_route(
    request: Request,
    file: UploadFile = File(...)
):
    try:

        # Read uploaded CSV
        df = pd.read_csv(file.file)

        # Load preprocessor
        preprocessor = load_object(
            "final_model/preprocessor.pkl"
        )

        # Load trained model
        final_model = load_object(
            "final_model/model.pkl"
        )

        # Create network model
        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        # Make prediction
        y_pred = network_model.predict(df)

        # Add prediction column
        df["predicted_column"] = y_pred

        # Convert result to HTML
        table_html = df.to_html(
            classes="table table-striped",
            index=False
        )

        # Return HTML result
        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={
                "table": table_html
            }
        )

    except Exception as e:

        raise NetworkSecurityException(
            e,
            sys
        )


# --------------------------------------------------
# Local Development
# --------------------------------------------------

if __name__ == "__main__":

    app_run(
        app,
        host="0.0.0.0",
        port=8000
    )