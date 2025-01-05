import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DOWNLOAD_DIRECTORY = "downloads"

def create_download_directory():
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)

def get_all_files_from_download_directory():
    try:
        return os.listdir(DOWNLOAD_DIRECTORY)
    except FileNotFoundError:
        return []

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    list_of_files = get_all_files_from_download_directory()
    return templates.TemplateResponse("index.html", {"request": request, "files": list_of_files})


@app.get("/download/{filename}")
async def root(filename: str):
    file_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type='multipart/form-data')
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    create_download_directory()
    uvicorn.run(app, host="127.0.0.1", port=8000)