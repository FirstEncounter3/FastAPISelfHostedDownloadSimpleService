from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.router import router

import uvicorn

from config import PORT
from utilities.file_and_directory_handler import create_download_directory


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=router)


if __name__ == "__main__":
    create_download_directory()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
