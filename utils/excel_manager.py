import os
import time
from typing import Any

import xlwings as xw
from polars import DataFrame
from pywintypes import com_error


EXCEL_BUSY_ERRORS = (
    -2146777998,  # OLE error 0x800ac472 - Excel busy / COM rejected
    -2147418111,
    -2147417846,
)


def retry_excel_com(action, retries: int = 40, delay: float = 0.5):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            return action()

        except com_error as e:
            last_error = e

            if e.hresult in EXCEL_BUSY_ERRORS:
                print(f"Excel đang bận, thử lại {attempt}/{retries}...")
                time.sleep(delay)
                continue

            raise

    raise RuntimeError(f"Excel vẫn đang bận sau {retries} lần thử") from last_error


class WorkSheetsManager:
    def __init__(self, sheet_name: str, wb: "WorkBookManager"):
        self.wb: WorkBookManager = wb
        self.sheet: xw.Sheet = retry_excel_com(
            lambda: self.wb.sheets[sheet_name],
            retries=20,
            delay=0.5,
        )

    def write(self, place: tuple[DataFrame | Any, str]) -> None:
        data, rng = place

        try:
            self.wb.enter_fast_mode()

            def write_data():
                if isinstance(data, DataFrame):
                    self.sheet.range(rng).value = data.to_numpy()
                else:
                    self.sheet.range(rng).value = data

            retry_excel_com(write_data, retries=40, delay=0.5)
            self.wb.save_workbook()

        except Exception as e:
            raise RuntimeError(f"Ghi dữ liệu Excel thất bại tại vùng {rng}") from e

        finally:
            self.wb.restore_user_mode()

    def delete_data(self, rng: str | tuple[str, str]) -> bool:
        try:
            self.wb.enter_fast_mode()

            if isinstance(rng, str):
                retry_excel_com(
                    lambda: self.sheet.range(rng).clear_contents(),
                    retries=30,
                    delay=0.5,
                )
                return True

            if isinstance(rng, tuple):
                s_p, e_p = rng
                retry_excel_com(
                    lambda: self.sheet.range(f"{s_p}:{e_p}").clear_contents(),
                    retries=30,
                    delay=0.5,
                )
                return True

            raise TypeError("Sai kiểu dữ liệu truyền vào!")

        except Exception as e:
            raise RuntimeError(f"Xóa dữ liệu Excel thất bại tại vùng {rng}") from e

        finally:
            self.wb.restore_user_mode()

    def get_data_range(
        self,
        rng: str,
        get_only_endpoint: bool = False,
    ) -> tuple[str, str] | int:
        try:
            point: list[str] = rng.split(":")

            if len(point) > 2:
                raise ValueError("Vui lòng truyền đúng định dạng 'start:end'")

            start_p, end_p = point

            last_row: int = retry_excel_com(
                lambda: self.sheet.range(
                    f"A{self.sheet.cells.last_cell.row}"
                ).end("up").row,
                retries=30,
                delay=0.5,
            )

            if get_only_endpoint:
                return last_row

            end_p += str(last_row)
            return start_p, end_p

        except Exception as e:
            raise RuntimeError(f"Lấy vùng dữ liệu Excel thất bại với range {rng}") from e

    def delete_row(self, rng_row: tuple[int, int]) -> None:
        try:
            self.wb.enter_fast_mode()

            from_row, to_row = rng_row

            if to_row < from_row:
                return

            retry_excel_com(
                lambda: self.sheet.range(f"{from_row}:{to_row}").delete(),
                retries=30,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError(f"Xóa dòng Excel thất bại với range {rng_row}") from e

        finally:
            self.wb.restore_user_mode()

    def delete_to_last_row(self, start_index: int) -> None:
        try:
            self.wb.enter_fast_mode()

            last_row: int = retry_excel_com(
                lambda: self.sheet.range(
                    "A" + str(self.sheet.cells.last_cell.row)
                ).end("up").row,
                retries=30,
                delay=0.5,
            )

            if start_index >= last_row:
                return

            retry_excel_com(
                lambda: self.sheet.range(f"{start_index}:{last_row}").delete(),
                retries=30,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError(f"Xóa từ dòng {start_index} tới dòng cuối thất bại") from e

        finally:
            self.wb.restore_user_mode()

    def range_copy(self, rng: str) -> None:
        try:
            self.wb.enter_fast_mode()

            retry_excel_com(
                lambda: self.sheet.range(rng).copy(),
                retries=30,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError(f"Copy range Excel thất bại tại vùng {rng}") from e

        finally:
            self.wb.restore_user_mode()

    def format_col(self, fm: str, col_or_range: str | list[str]) -> None:
        try:
            self.wb.enter_fast_mode()

            if fm not in ("@", "dd/mm/yyyy"):
                return

            if isinstance(col_or_range, str):
                retry_excel_com(
                    lambda: setattr(
                        self.sheet.range(col_or_range),
                        "number_format",
                        fm,
                    ),
                    retries=30,
                    delay=0.5,
                )
                return

            if isinstance(col_or_range, list):
                for col in col_or_range:
                    retry_excel_com(
                        lambda c=col: setattr(
                            self.sheet.range(f"{c}:{c}"),
                            "number_format",
                            fm,
                        ),
                        retries=30,
                        delay=0.5,
                    )
                return

            raise TypeError("Sai kiểu dữ liệu truyền vào format_col")

        except Exception as e:
            raise RuntimeError(f"Format column Excel thất bại với {col_or_range}") from e

        finally:
            self.wb.restore_user_mode()

    def copy_to_last_row(self, rng_to_range: str, index_start: int) -> None:
        try:
            self.wb.enter_fast_mode()

            from_rng, to_rng = rng_to_range.split(":")

            last_row: int = retry_excel_com(
                lambda: self.sheet.range(
                    f"A{self.sheet.cells.last_cell.row}"
                ).end("up").row,
                retries=30,
                delay=0.5,
            )

            if index_start >= last_row:
                return

            retry_excel_com(
                lambda: self.sheet.range(
                    f"{from_rng}{index_start}:{to_rng}{last_row}"
                ).copy(),
                retries=30,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError(
                f"Copy tới dòng cuối thất bại với range {rng_to_range}"
            ) from e

        finally:
            self.wb.restore_user_mode()

    def close(self) -> None:
        self.wb.close()


class WorkBookManager:
    def __init__(self, path: str, on_screen: bool = True):
        self.path: str = path

        if not os.path.exists(path):
            raise FileNotFoundError(f"Đường dẫn không tồn tại: {path}")

        self.app: xw.App | None = None
        self.wb: xw.Book | None = None
        self.sheets = None

        for app in xw.apps:
            for wb in app.books:
                try:
                    wb_fullname = retry_excel_com(
                        lambda w=wb: w.fullname,
                        retries=10,
                        delay=0.5,
                    )

                    if os.path.normcase(wb_fullname) == os.path.normcase(path):
                        self.app = app
                        self.wb = wb
                        self.sheets = wb.sheets

                        # Đảm bảo Excel không bị kẹt trạng thái cũ
                        self.restore_user_mode()
                        break

                except Exception:
                    continue

            if self.app and self.wb:
                break

        if not self.app or not self.wb:
            self.app = xw.App(visible=on_screen, add_book=False)

            self.wb = retry_excel_com(
                lambda: self.app.books.open(path, update_links=False),
                retries=40,
                delay=0.5,
            )

            self.sheets = self.wb.sheets

            # Mở xong thì để Excel ở trạng thái user nhìn ổn
            self.restore_user_mode()

    def enter_fast_mode(self) -> None:
        """
        Chế độ thao tác nhanh.
        Chỉ bật trong lúc automation đang chạy.
        """
        if not self.app:
            return

        try:
            retry_excel_com(
                lambda: setattr(self.app, "screen_updating", False),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "display_alerts", False),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "calculation", "manual"),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "enable_events", False),
                retries=20,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError("Bật Excel fast mode thất bại") from e

    def restore_user_mode(self) -> None:
        """
        Restore Excel về trạng thái bình thường để UX không bị lỗi giao diện.
        """
        if not self.app:
            return

        try:
            retry_excel_com(
                lambda: setattr(self.app, "screen_updating", True),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "display_alerts", True),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "calculation", "automatic"),
                retries=20,
                delay=0.5,
            )

            retry_excel_com(
                lambda: setattr(self.app, "enable_events", True),
                retries=20,
                delay=0.5,
            )

        except Exception:
            # Không raise ở restore để tránh che lỗi chính
            pass

    def get_sheet(self, sheet_name: str) -> WorkSheetsManager:
        try:
            return WorkSheetsManager(sheet_name, self)

        except Exception as e:
            raise RuntimeError(
                f"Excel đang bận hoặc tên sheet không đúng: {sheet_name}"
            ) from e

    def refresh(self) -> None:
        try:
            self.enter_fast_mode()

            retry_excel_com(
                lambda: self.wb.api.RefreshAll(),
                retries=40,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError("Refresh workbook thất bại") from e

        finally:
            self.restore_user_mode()

    def close(self) -> None:
        try:
            # Quan trọng: restore trước khi close để Excel không bị tật UI
            self.restore_user_mode()

            if self.wb:
                retry_excel_com(
                    lambda: self.wb.close(),
                    retries=20,
                    delay=0.5,
                )

            if self.app:
                try:
                    books_count = retry_excel_com(
                        lambda: self.app.books.count,
                        retries=10,
                        delay=0.5,
                    )
                except Exception:
                    books_count = 1

                if books_count < 1:
                    retry_excel_com(
                        lambda: self.app.quit(),
                        retries=20,
                        delay=0.5,
                    )

        except Exception as e:
            raise RuntimeError("Đóng Excel workbook thất bại") from e

    def create_empty_book(self) -> tuple[xw.App, xw.Book]:
        try:
            app: xw.App = xw.App(add_book=False, visible=False)
            wb: xw.Book = app.books.add()

            retry_excel_com(
                lambda: wb.api.SaveAs(self.path),
                retries=40,
                delay=0.5,
            )

            return app, wb

        except Exception as e:
            raise RuntimeError("Tạo workbook rỗng thất bại") from e

    def save_workbook(self) -> None:
        """
        Dùng COM API Save trực tiếp để tránh xlwings wrapper tự đụng display_alerts.
        """
        try:
            retry_excel_com(
                lambda: self.wb.api.Save(),
                retries=60,
                delay=0.5,
            )

        except Exception as e:
            raise RuntimeError("Save workbook thất bại") from e