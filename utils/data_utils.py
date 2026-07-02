from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import io
import msoffcrypto
import threading
import polars as pl
from utils.file_handler import FileHelper


class DataIngestor:
    def __init__(self, paths_map: dict[str, str] | None, raw_file=False):
        self.raw_file = raw_file

        if not self.raw_file:
            self.paths_map: dict[str, str] = paths_map
            self.paths_folder_locals: set[str] = set(
                [os.path.dirname(v) for k, v in paths_map.items()]
            )
            self.file_error: list[str] = []

    def load_data_raw_file(self, file_path: str):
        if not self.raw_file:
            raise RuntimeError("Chức năng không khả dụng")

        return pl.read_excel(file_path, engine="calamine")

    def ingest_data(self) -> pl.DataFrame:
        if self.raw_file:
            raise RuntimeError("Chức năng không khả dụng")

        if len(self.paths_map) == 1:
            s, d = list(self.paths_map.items())[0]
            data_single: pl.DataFrame = self.load_single_file(s, d)

            if data_single is None:
                raise FileNotFoundError(
                    "Load single data failed! Có thể đường dẫn nguồn không tồn tại!"
                )

            FileHelper.remove_folder(d)
            return data_single

        data: pl.DataFrame = self.load_multiple_files()

        for i in self.paths_folder_locals:
            FileHelper.remove_folder(i)

        return data

    def load_single_file(self, src_p: str, dest_p: str) -> pl.DataFrame | None:
        if self.raw_file:
            raise RuntimeError("Chức năng không khả dụng")

        try:
            if os.path.exists(src_p):
                FileHelper.create_folder(dest_p)
                FileHelper.file_transfer(src_p, dest_p)

                data: io.BytesIO = self._load_data_with_key(dest_p, "J@bil2022")
                data.seek(0)

                df: pl.DataFrame = pl.read_excel(
                    data,
                    infer_schema_length=0,
                    has_header=False,
                    engine="calamine",
                )

                df = df.slice(1)

                df = df.filter(~pl.all_horizontal(pl.all().is_null()))

                df = df.select(df.columns[:14])
                df.columns = [
                    "GRN",
                    "MPN",
                    "DC",
                    "LOT (1T)",
                    "Qty",
                    "User/Time",
                    "MPN SAP",
                    "DC SAP",
                    "LOT SAP (1T)",
                    "MPN Verify",
                    "DC Verify",
                    "LOT Verify",
                    "Stk Placement",
                    "Qty Ver",
                ]

                if df is not None and not df.is_empty():
                    return df
                

                raise RuntimeError(f"File không có data hợp lệ: {dest_p}")

            else:
                return None

        except Exception as e:
            raise RuntimeError(f"Load single file thất bại: {src_p} -> {dest_p}") from e

    def load_multiple_files(self) -> pl.DataFrame:
        if self.raw_file:
            raise RuntimeError("Chức năng không khả dụng")

        data_list: list[pl.DataFrame] = []

        try:
            with ThreadPoolExecutor(max_workers=10) as exe:
                futures = [
                    exe.submit(self.load_single_file, src, dest)
                    for src, dest in self.paths_map.items()
                ]

                for f in as_completed(futures):
                    if f.result() is not None:
                        data_list.append(f.result())

            if not len(data_list):
                raise FileNotFoundError(
                    "Vui lòng kiểm tra lại sự tồn tại của file nguồn hoặc file đích"
                )

            return pl.concat(data_list, rechunk=True, strict=True, parallel=True)

        except Exception as e:
            raise RuntimeError("Load multiple files thất bại") from e

    def _load_data_with_key(self, path: str, p: str) -> io.BytesIO:
        if self.raw_file:
            raise RuntimeError("Chức năng không khả dụng")

        with open(path, "rb") as file:
            office_file: msoffcrypto.OfficeFile = msoffcrypto.OfficeFile(file)

            if office_file.is_encrypted():
                office_file.load_key(p)
                decrypted: io.BytesIO = io.BytesIO()
                office_file.decrypt(decrypted)
                return decrypted

            else:
                file.seek(0)
                return io.BytesIO(file.read())