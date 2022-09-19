from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("img")
async def say_hello(file: UploadFile = File(...)):
    return {"message": f"Hello {name}"}
