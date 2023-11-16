import logging
import os

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from src.modules.docs import API_CONTACT, API_LICENSE, API_TAGS

app = FastAPI(
    title="IDEALISTA Rent Price Predictor API",
    summary="IDEALISTA Rent Price Predictor Application Programming Interface (API).",
    description="This is intended to be a POC for predicting homes prices based on user inputs.",
    openapi_tags=API_TAGS,
    contact=API_CONTACT,
    license_info=API_LICENSE,
)


@app.get("/", include_in_schema=False)
def redirect_index():
    return RedirectResponse("/docs", status_code=307)


@app.post(
    "/predict",
    status_code=200,
    tags=["Rent"],
    description="Endpoint to estimate rent price given several parameters.",
)
async def predict_rent_price(
    city: str = Query(
        enum=["Madrid", "Barcelona", "Valencia", "Sevilla"],
        description="Municipality of the home.",
    ),
    num_rooms: int = Query(
        ge=1, lt=7, description="Number of desired rooms in the home."
    ),
    num_bathrooms: int = Query(
        ge=1, lt=5, description="Number of desired bathrooms in the home."
    ),
    has_lift: bool = Query(
        default=None, description="Whether if the home includes lift or not."
    ),
):
    # FIXME: transform input features here for inference
    price = num_rooms * num_bathrooms
    logging.info(f"User request: {num_rooms} rooms, {num_bathrooms} bathrooms.")

    response = f"The estimated price is {price} €."

    return response


if __name__ == "__main__":
    API_PORT = os.environ.get("API_PORT", 8081)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=API_PORT,
        log_level="debug",
        proxy_headers=True,
        # reload=True
    )
