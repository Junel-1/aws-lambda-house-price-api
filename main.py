from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from mangum import Mangum

# Setting root_path enables Swagger UI to work through AWS API Gateway stages
app = FastAPI(
    title="House Price Prediction API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Load model
model = joblib.load("house_price_model.joblib")

class HouseFeatures(BaseModel):
    sqft: float
    bedrooms: int
    bathrooms: float

@app.get("/")
def health_check():
    return {"status": "online", "message": "House Price Prediction API is active on AWS."}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    input_data = np.array([[features.sqft, features.bedrooms, features.bathrooms]])
    predicted_price = model.predict(input_data)[0]
    
    return {
        "input": features.model_dump(),
        "predicted_price_usd": round(float(predicted_price), 2)
    }

# Mangum handler with API Gateway HTTP API stage adaptation
handler = Mangum(app, api_gateway_base_path=None)