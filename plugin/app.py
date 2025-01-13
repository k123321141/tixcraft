from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Captch solver Service", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your actual front-end origin
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define request and response models


class ImageRequest(BaseModel):
    img_b64str: str


@app.on_event("startup")
def load_model():
    pass


@app.post("/solve_captcha", response_model=dict)
def claim_reference(request: ImageRequest):
    print(request.img_b64str)
    if not request.img_b64str:
        raise HTTPException(status_code=400, detail="Text field is empty.")
    return {'result': 'ABCD'}


@app.get("/")
def read_root():
    return {"message": "Welcome to Captch solver Service"}
