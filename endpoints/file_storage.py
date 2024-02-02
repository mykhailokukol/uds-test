from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter, File, UploadFile, Response, HTTPException

from services.endpoints.file_storage import (
    upload_file_to_storage,
    read_file_info_from_storage,
    get_top_10_files,
    set_headers,
    download_file,
)


router = APIRouter()


@router.post("/files/{dir_name}")
async def upload_file_to_dir(dir_name: str, file: UploadFile = File(...)):
    response = await upload_file_to_storage(file, dir_name)
    return JSONResponse(response, status_code=201)


@router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    response = await upload_file_to_storage(file)
    return JSONResponse(response, status_code=201)


@router.get("/files/{id}")
async def read_file(id: int):
    file_path, file_name = await download_file(id)
    try:
        return FileResponse(file_path, filename=file_name, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not found")


@router.head("/files/{id}")
async def read_file_info(id: int, response: Response):
    headers = await read_file_info_from_storage(id)
    await set_headers(headers, response)
    return None


@router.get("/top")
async def read_top_10_files():
    response = await get_top_10_files()
    return JSONResponse(response, status_code=200)


@router.get("/top/{dir_name}")
async def read_top_10_files_in_dir(dir_name: str):
    response = await get_top_10_files(dir_name)
    return JSONResponse(response, status_code=200)
