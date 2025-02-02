import os
import uuid
from io import BytesIO

import pandas as pd
import requests

from rho_store.file_utils import get_relative_path


class UploadFileHttpAdapter:
    def __init__(self):
        self.session = requests.Session()

    def upload_file(self, url: str, file_data: bytes) -> None:
        headers = {
            "Content-Type": "application/octet-stream",
        }
        response = self.session.put(url, headers=headers, data=file_data)
        response.raise_for_status()

    def upload_dataframe(self, url: str, data: pd.DataFrame) -> None:
        buffer = BytesIO()
        data.to_parquet(buffer, engine="pyarrow")
        file_data = buffer.getvalue()
        self.upload_file(url, file_data)

    def upload_dataframe_using_file(self, url: str, data: pd.DataFrame) -> None:
        # 1. Dump file locally
        temp_file_path = f"temp/{str(uuid.uuid4())}.parquet"
        local_file_path = get_relative_path(temp_file_path, __file__)
        data.to_parquet(local_file_path)
        # 2. Read file and upload
        with open(local_file_path, "rb") as f:
            file_data = f.read()
        self.upload_file(url, file_data)
        # 3. delete file
        os.remove(local_file_path)


__all__ = ["UploadFileHttpAdapter"]
