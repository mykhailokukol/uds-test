from fastapi import APIRouter, File, UploadFile


router = APIRouter()


@router.post("files/{dir_name}/")
async def upload_file_to_dir(dir_name: str, file: UploadFile = File(...)):
    ...


@router.post("files/")
async def upload_file(file: UploadFile = File(...)):
    ...


@router.get("files/{id}/")
async def read_file(id: str):
    ...


@router.head("files/{id}/")
async def read_file_info(id: str):
    ...


@router.get("top/")
async def read_top_10_files():
    ...


@router.get("top/{dir_name}/")
async def read_top_10_files_in_dir(dir_name: str):
    ...
