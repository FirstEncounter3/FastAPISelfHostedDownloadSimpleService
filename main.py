from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.router import router

from utilities.file_and_directory_handler import create_download_and_upload_directory


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=router)
create_download_and_upload_directory()
