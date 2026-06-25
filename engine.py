import sys
import os
import time
import traceback
from datetime import datetime,date
from step.stage import CombaineStepMachine, CombaineComponent
from communication.ipc import CommunicationToCSharp
from getpass import getuser


class FileLogger:
    def __init__(self, log_path: str = f"log_exception{date.today()}.txt"):
        self.log_dir = fr"C:\Users\{getuser()}\Documents\LoggerException"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir,exist_ok=True)
        self.log_path = os.path.join(self.log_dir,log_path)

    def exception(self, ex: BaseException, message: str = "Unhandled exception") -> None:
        with open(self.log_path, "a", encoding="utf-8") as f:
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
    logger = FileLogger()
    try:
        event_control: CommunicationToCSharp = CommunicationToCSharp()
    except Exception as e:
        logger.exception(e,"IPC init failed!")

    while True:
        
        print("Dang cho lenh....")
        event_control.waiting_request_event()

        command: str = event_control.read_memo().split(":")[1]
        app: DailyReportExportMachine = DailyReportExportMachine(CombaineStepMachine, CombaineComponent)

        if command == "run_app":
            print("Dang chay....")

            try:
                app.run()

            except Exception:
                logger.exception("Run app failed")

            finally:
                event_control.set_respone_event()

        else:
            print("Lenh khong hop le!")

        # os.system("cls")