import mmap
import win32event
import struct
import win32con


class CommunicationToCSharp:
    def __init__(self):
        try:
            self.SRM_NAME: str = r"Local\python_connect_to_CSharp"
            self.REQ_EVENT_NAME: str = r"Local\request_to_python"
            self.INIT_APP_SUCCESS : str = r"Local\init_python_success"
            self.RES_EVENT_NAME: str = r"Local\respone_to_Csharp"
            self.MUTEX_NAME: str = r"Local\Mutex_connect"

            self.BUF_SIZE: int = 4096

            self.shared_memo: mmap.mmap = mmap.mmap(
                -1,
                self.BUF_SIZE,
                tagname=self.SRM_NAME,
            )

            self.req_event: int = win32event.OpenEvent(
                win32event.EVENT_ALL_ACCESS,
                False,
                self.REQ_EVENT_NAME,
            )

            self.res_event: int = win32event.OpenEvent(
                win32event.EVENT_ALL_ACCESS,
                False,
                self.RES_EVENT_NAME,
            )
            
            self.init_event_success : int = win32event.OpenEvent(
                win32event.EVENT_ALL_ACCESS,
                False,
                self.INIT_APP_SUCCESS,
            )
            
            self.muxtext_locker: int = win32event.OpenMutex(
                win32event.SYNCHRONIZE,
                False,
                self.MUTEX_NAME,
            )
            

        except Exception as e:
            raise RuntimeError("Khởi tạo IPC kết nối C# thất bại") from e

    def read_memo(self) -> str:
        try:
            wait_result = win32event.WaitForSingleObject(
                self.muxtext_locker,
                win32event.INFINITE,
            )

            if wait_result != win32event.WAIT_OBJECT_0:
                raise RuntimeError(f"Không lấy được mutex IPC. Wait result: {wait_result}")

            try:
                self.shared_memo.seek(0)

                length: int = struct.unpack("<I", self.shared_memo.read(4))[0]

                if length < 0 or length > self.BUF_SIZE - 4:
                    raise ValueError(
                        f"Độ dài dữ liệu IPC không hợp lệ: {length}. "
                        f"BUF_SIZE={self.BUF_SIZE}"
                    )

                self.shared_memo.seek(4)
                data: bytes = self.shared_memo.read(length)

                return data.decode()

            finally:
                win32event.ReleaseMutex(self.muxtext_locker)

        except Exception as e:
            raise RuntimeError("Đọc dữ liệu từ shared memory IPC thất bại") from e

    def waiting_request_event(self) -> None:
        try:
            wait_result = win32event.WaitForSingleObject(
                self.req_event,
                win32event.INFINITE,
            )

            if wait_result != win32event.WAIT_OBJECT_0:
                raise RuntimeError(
                    f"Chờ request event từ C# thất bại. Wait result: {wait_result}"
                )

        except Exception as e:
            raise RuntimeError("Chờ request event IPC thất bại") from e

    def set_respone_event(self) -> None:
        try:
            win32event.SetEvent(self.res_event)

        except Exception as e:
            raise RuntimeError("Set response event IPC thất bại") from e
        
        
    def set_init_successed(self) -> None:
        try:
            win32event.SetEvent(self.init_event_success)
        except Exception as e:
            raise RuntimeError("Set init python event IPC thất bại") from e