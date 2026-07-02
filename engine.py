import sys
import traceback
from step.stage import CombaineStepMachine, CombaineComponent
from communication.ipc import CommunicationToCSharp
from getpass import getuser
import os
import traceback
from datetime import datetime, date


if getattr(sys, "frozen", False):
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")

    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")



class FileLogger:
    def __init__(self,open_after_write: bool = True):
        self.log_dir = fr"C:\Users\{getuser()}\Documents\LoggerException"

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)


        self.open_after_write = open_after_write

    def exception(self, ex: BaseException, message: str = "Unhandled exception") -> None:
        path : str = fr"C:\Users\{getuser()}\Documents\LoggerException\log_exception_{date.today().strftime('%Y-%m-%d')}.txt"
        with open(path, "a", encoding="utf-8") as f:
            f.write("=" * 100)
            f.write("\n")
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
            f.write("\n")
            f.write(
                "".join(
                    traceback.format_exception(
                        type(ex),
                        ex,
                        ex.__traceback__,
                    )
                )
            )
            f.write("\n")

        if self.open_after_write:
            self.open_log_file(path)

    def open_log_file(self,path) -> None:
        try:
            os.startfile(path)
        except Exception:
            # Không raise ở đây để tránh logger tự làm crash app lần nữa
            pass

class DailyReportExportMachine:
    def __init__(
        self,
        combaine_step_machine_cls: type[CombaineStepMachine] = CombaineStepMachine,
        combaine_component_cls: type[CombaineComponent] = CombaineComponent,
    ):
        self.combaine_step_machine: CombaineStepMachine = combaine_step_machine_cls(combaine_component_cls)
        self.combaine_step_machine.combaine()

    def run(self) -> None:
        if self.combaine_step_machine.run_sap:
            self.combaine_step_machine.run_sap.run()

        self.combaine_step_machine.writer_excel.run()


if __name__ == "__main__":
    logger = FileLogger(open_after_write=True)
    try:
        event_control: CommunicationToCSharp = CommunicationToCSharp()
    except Exception as e:
        logger.exception(e,"IPC init failed!")
        sys.exit(1)
    event_control.set_init_successed()
    
    
    while True:
        
        print("Dang cho lenh....")

        event_control.waiting_request_event()
        command: str = event_control.read_memo().split(":")[1]

        try:
            app: DailyReportExportMachine = DailyReportExportMachine(CombaineStepMachine, CombaineComponent)
        except Exception as e:
            logger.exception(e,"App Init Failed!")

        if command == "run_app":
            print("Dang chay....")

            try:
                app.run()

            except Exception as e :
                logger.exception(e,"Run app failed")
                app.combaine_step_machine.writer_excel.writer_daily_report.close()

            finally:
                event_control.set_respone_event()
                

        else:
            print("Lenh khong hop le!")

        # os.system("cls")