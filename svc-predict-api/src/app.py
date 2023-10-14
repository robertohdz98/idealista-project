import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="IDEALISTA Rent Price Predictor API")


@app.get("/", include_in_schema=False)
def redirect_index():
    return RedirectResponse("/docs", status_code=307)


@app.post("/predict", status_code=200)
async def predict_(request: int):

    return request


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0",
                port=8080,
                log_level="debug",
                proxy_headers=True,
                # reload=True
                )
