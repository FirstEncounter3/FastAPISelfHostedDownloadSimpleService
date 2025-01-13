import os
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    File,
    UploadFile,
)
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from config import DOWNLOAD_DIRECTORY, UPLOAD_DIRECTORY, PORT, DEBUG
from utilities.get_ip import get_ip_address
from utilities.qr_code_creator import generate_qr_code
from utilities.file_and_directory_handler import get_all_files_from_download_directory


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def hello(request: Request) -> HTMLResponse:
    list_of_files = get_all_files_from_download_directory()
    ip_address = get_ip_address()
    qr_code_img = generate_qr_code(f"http://{ip_address}:{PORT}", debug=DEBUG)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "files": list_of_files, "qr_code": qr_code_img},
    )


@router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str) -> FileResponse:
    file_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="multipart/form-data")
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename}
