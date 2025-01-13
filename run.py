import os
from config import DEBUG, PORT

if __name__ == "__main__":
    if DEBUG:
        os.system(f"uvicorn main:app --host 0.0.0.0 --port {PORT} --reload")
    else:
        os.system(f"uvicorn main:app --host 0.0.0.0 --port {PORT}")
