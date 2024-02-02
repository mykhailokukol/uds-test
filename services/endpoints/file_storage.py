import os
import pandas as pd
from openpyxl import Workbook
from fastapi import UploadFile, Response

from config.conf import settings
from config.database import create_query, read_query


async def upload_file_to_storage(file: UploadFile, path: str = None) -> dict:
    """Upload a file to server media directory and save it's path to DB"""

    # Upload to storage part
    if not path:
        file_path = os.path.join(settings.MEDIA_DIR, file.filename)
    else:
        path_to_save = os.path.join(settings.MEDIA_DIR, path)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file_path = os.path.join(path_to_save, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    file_path = file_path.split(f"{file.filename}")[0]

    # Store in DB part
    file_exists = read_query(
        """
        select id from files where name = '%s'
        """
        % (file.filename,)
    )
    if file_exists:
        create_query(
            """
            update files
            set updated_at = now()
            where filepath = '%s'
            """
            % (file_path,)
        )
    else:
        create_query(
            """
            insert into files (filepath, name, size, updated_at)
            values ('%s', '%s', %s, now())
            """
            % (file_path, file.filename, file.size)
        )

    response = {"file": file_path}
    return response


async def read_file_info_from_storage(id: int):
    """Return file info from database"""
    response = read_query(
        """
        select * from files
        where id = %s
        """
        % (id,)
    )[0]
    if not response:
        return

    headers = {
        "id": str(response[0]),
        "filepath": response[1],
        "name": response[2],
        "size": str(response[3]),
        "updated_at": str(response[4]),
    }
    return headers


async def set_headers(headers: dict, response: Response) -> Response:
    for key in headers.keys():
        response.headers[key] = headers[key]
    return response


async def get_top_10_files(dir_name: str = None) -> dict:
    """Returns top 10 by size files in media directory or provided directory"""
    response = {
        "top10FilesBySize": [],
    }

    if not dir_name:
        query = read_query(
            """
            select * from files
            where filepath ~ '%s'
            order by size desc
            limit 10
            """
            % (f"^{settings.MEDIA_DIR}\\\\$",)
        )
    else:
        query = read_query(
            """
            select * from files
            where filepath ~ '%s'
            order by size desc
            limit 10
            """
            % (f"^{settings.MEDIA_DIR}\\\\{dir_name}\\\\$",)
        )

    keys = ["id", "filepath", "name", "size", "updated_at"]
    for file in query:
        file = dict(zip(keys, map(str, file)))
        response["top10FilesBySize"].append(file)

    return response


async def download_file(id: int):
    file_path = read_query(
        """
        select filepath, name from files
        where id = %s
        """
        % (id,)
    )
    file_name = file_path[0][1]
    file_path = f"{file_path[0][0]}{file_name}"
    return file_path, file_name


async def download_xlsx_report(file_id: int) -> str:
    """Opens .txt file, makes it .xslx and adds operation result"""
    filepath = read_query(
        """
        select filepath, name from files
        where id = %s
        """
        % (file_id,)
    )[0]
    result_filename = f"{filepath[1][:-4]}.xlsx"
    filepath = os.path.join(filepath[0], filepath[1])

    df = pd.read_csv(filepath, delimiter=" ", header=None, names=["Місяць", "Значення"])
    new_row = {"Місяць": "Результат", "Значення": " "}
    df.loc[len(df)] = new_row

    operation_index = df[df["Місяць"] == "Операція"].index[0]
    operation = df.at[operation_index, "Значення"]
    formula = operation.join("B" + str(i + 2) for i in range(operation_index))
    df.at[df.index[-1], "Значення"] = f"={formula}"

    filepath_xlsx = f"{filepath[:-4]}.xlsx"
    df.to_excel(filepath_xlsx, index=False, engine="openpyxl")
    return filepath_xlsx, result_filename
