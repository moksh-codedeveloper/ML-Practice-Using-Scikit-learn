# main.py
from fastapi import FastAPI
from models import run_models
from train_models import train_model
import joblib
# from train_models import train_model
app = FastAPI()

# Load models once on startup
iso_model = joblib.load('./models/isolation_forest_model.pkl')
reg_model = joblib.load('./models/linear_regression_model.pkl')
    

@app.get("/predict")
def predict():
    result = run_models(iso_model, reg_model)
    train_model.log_event("IsoForest LinearRegressor", "success", "./models", "Prediction")
    return result

@app.get("/")
def read_root():
    return {"message": "Welcome to the Anomaly Detection API. Use /predict to get predictions."}
from pydantic import BaseModel

class RetrainRequest(BaseModel):
    n_samples: int
    model_name: str
@app.post("/retrain")
def retrain(request: RetrainRequest):
    if request.model_name == "isolation_forest":
        train_model.iso_model_training(request.n_samples)
        train_model.log_event("Isolation Forest", "retrained", "./models/isolation_forest_model.pkl", "Model retraining")
        return {"message": f"Isolation Forest model retrained with {request.n_samples} samples."}
    elif request.model_name == "linear_regression":
        train_model.regressor_training(request.n_samples)
        train_model.log_event("Linear Regression", "retrained", "./models/linear_regression_model.pkl", "Model Retraining")
        return {"message": f"Linear Regression model retrained with {request.n_samples} samples."}
    else:
        return {"error": "Invalid model name. Use 'isolation_forest' or 'linear_regression'."}

   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)