from fastapi import FastAPI

from app.v1.endpoints import tesseract_ocr

app = FastAPI(
    # dependencies=[Depends(get_settings)]
)

app.include_router(tesseract_ocr.router)
