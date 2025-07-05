from importlib import reload
from fastapi import FastAPI
from ml_engine.model_runner import test_iso_models, test_kmeans_models, regressor_model
from core.feature_extracter import load_csv_as_dataframe
import uvicorn
app = FastAPI()

@app.get("/")
def main():
    return {"message":"this is the network scanner runmning"}
@app.get("/test_iso")
def train_iso():
    test_iso_models()
    return{"message": "this is the testing of the iso model using the scanned data"}

@app.get("/test_kmeans")
def test_kmeans():
    test_kmeans_models()
    return{"message": "this is the message from the kmeans model which is that the testing of the model is successful"}

@app.get("/test_regressor")
def test_regressor():
    regressor_model()
    return {"message": "this is the message from the regressor model which is that the testing of the model is successful"}
if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, reload=True)