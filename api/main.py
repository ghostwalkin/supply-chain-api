from fastapi import FastAPI, UploadFile
import os
from contextlib import asynccontextmanager
from utils import get_driver, upload_csv_to_neo4j, query_neo4j
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = get_driver()
    try:
        yield
    finally:
        driver.close()


app = FastAPI(lifespan=lifespan)


# helper to upload csv in neo4j


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile):
    # save the file to disk
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # upload the file to neo4j
    upload_csv_to_neo4j(file_path)
    # remove the file from disk
    os.remove(file_path)

    return {"message": "File uploaded successfully", "file_path": file_path}


@app.get("/query")
async def query(from_station: str, to_station: str):
    # query the neo4j database
    result = query_neo4j(from_station, to_station)
    if not result:
        return {"message": "No route found"}
    return {"message": "Route found", "data": result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
