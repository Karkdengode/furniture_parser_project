from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Literal
import logging
import shutil
import uuid
from pathlib import Path

from furniture_parser.pdf_parser import parse_pdf


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/parse")
async def parse_file(
    file: UploadFile = File(...),
    type: Literal["pdf", "ifc"] = Form(...)
):
    # Lagre opplastet fil midlertidig
    suffix = Path(file.filename).suffix
    temp_filename = f"/tmp/{uuid.uuid4()}{suffix}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if type == "pdf":
        result = parse_pdf(temp_filename)
    elif type == "ifc":
    from furniture_parser.ifc_parser import parse_ifc_file
    result = parse_ifc_file(temp_filename)

    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    return result


