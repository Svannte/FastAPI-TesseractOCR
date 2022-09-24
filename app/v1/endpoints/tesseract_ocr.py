import io
import pathlib
import uuid

import pytesseract
from fastapi import APIRouter, Depends, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image, UnidentifiedImageError

from app.core.settings import UPLOAD_DIR, Settings, get_settings, templates

router = APIRouter(prefix="/v1", tags=["Tesseract-OCR"])


def verify_auth(
    access_token: str = Header(None), settings: Settings = Depends(get_settings)
):
    if settings.debug and settings.skip_auth:
        return
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized user.")
    if access_token != settings.app_auth_token:
        raise HTTPException(status_code=401, detail="Unauthorized user.")


@router.get("/", response_class=HTMLResponse, dependencies=[Depends(verify_auth)])
async def root(request: Request):
    return templates.TemplateResponse(
        name="home.html", context={"request": request, "abc": 123}
    )


@router.post("/img", response_class=FileResponse, dependencies=[Depends(verify_auth)])
async def img_echo(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    if not settings.echo_active:
        raise HTTPException(status_code=400, detail="Invalid endpoint.")
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image.")
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest


@router.post("/predict")
async def predict_view(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
    access_token: str = Header(None),
):
    verify_auth(access_token, settings)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image.")
    pred = pytesseract.image_to_string(img)
    predictions = [x for x in pred.split("\n")]
    return {"result": predictions, "original": pred}
