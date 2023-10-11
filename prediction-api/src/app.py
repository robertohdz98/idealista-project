import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import os
from utils.schema import Cities
from pred.predict import infer_prediction


# TODO: add FastAPI doc
app = FastAPI(title="IDEALISTA Rent Price Predictor")


@app.get("/", include_in_schema=False)
def index_redirection():
    return RedirectResponse(url="/docs", status_code=302)

@app.post("/predict", status_code=200)
def predict_rent_price(city: Cities,
                       rooms: int = 2, #default
                       bathrooms: int = 1):

    if rooms > 10:
        raise HTTPException(status_code=400,
                            detail="Rooms should be maximum 10.")

    # TODO: basic flow
    features = {"rooms": rooms, "bathrooms": bathrooms}
    prediction = infer_prediction(features)

    return prediction


if __name__ == "__main__":

    uvicorn.run("app:app", host="0.0.0.0",
                port=8001, log_level="debug",
                proxy_headers=True, reload=True)
