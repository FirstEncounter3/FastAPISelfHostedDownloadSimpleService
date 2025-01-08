import os
import socket

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import qrcode
import base64
import io

import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


DOWNLOAD_DIRECTORY = "downloads"
PORT = 8000


def get_ip_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = "localhost"
    return ip_address


def generate_qr_code(url: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="#f5f5f5")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"


def create_download_directory():
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)


def get_all_files_from_download_directory():
    try:
        all_items = os.listdir(DOWNLOAD_DIRECTORY)
        files = [
            item
            for item in all_items
            if os.path.isfile(os.path.join(DOWNLOAD_DIRECTORY, item))
        ]
        return files
    except FileNotFoundError:
        return []


@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    list_of_files = get_all_files_from_download_directory()
    ip_address = get_ip_address()
    qr_code_img = generate_qr_code(f"http://{ip_address}:{PORT}")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "files": list_of_files, "qr_code": qr_code_img},
    )


@app.get("/download/{filename}")
async def root(filename: str):
    file_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="multipart/form-data")
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    create_download_directory()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
