from __future__ import annotations
import win32com.client
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel
from utils.config_loader import GRN10Config, GRN16Config
from utils.excel_manager import WorkBookManager, WorkSheetsManager
import time
import os
import subprocess
from pywintypes import com_error
from datetime import timedelta
from datetime import date, datetime

T = TypeVar("T", bound=BaseModel)


class SapConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        try:
            self.sap_path: str = r"C:\Program Files (x86)\SAP\FrontEnd\SAPGUI\saplogon.exe"
            self.engine: any = win32com.client.GetObject("SAPGUI").GetScriptingEngine

            try:
                self.session = self.engine.Children(0).Children(0)
            except com_error as e:
                if e.hresult == -2147352567:
                    self.connection = self.engine.OpenConnection(
                        "100| Jabil SAP - Commercial - PRD [Production]",
                        True,
                    )
                    self.session = self.connection.Children(0)

        except com_error as e:
            if e.hresult == -2147221020:
                subprocess.Popen(["explorer.exe",self.sap_path])
                #os.startfile(self.sap_path)
                time.sleep(7)
                self.engine: any = win32com.client.GetObject("SAPGUI").GetScriptingEngine
                self.connection = self.engine.OpenConnection(
                    "100| Jabil SAP - Commercial - PRD [Production]",
                    True,
                )
                self.session = self.connection.Children(0)


class GRNProcessor(Generic[T], ABC):
    def __init__(self, context: T, session: any):
        self.context: T = context
        self.session = session

    def process(self):
        pass


class GRN10Processor(GRNProcessor[GRN10Config]):
    def process(self):
        self.session.StartTransaction(self.context.tcode.upper())
        self.session.findById("wnd[0]/usr/ctxtSO_WERKS-LOW").Text = "VN01"
        self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-LOW").Text = f"{self.context.posting_date_start}"
        self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-HIGH").Text = f"{self.context.posting_date_end}"
        self.session.findById("wnd[0]/usr/btn%_SO_MJAHR_%_APP_%-VALU_PUSH").press()
        self.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/txtRSCSEL_255-SLOW_I[1,0]").Text = self.context.year
        self.session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/txtRSCSEL_255-SLOW_I[1,1]").Text = self.context.year
        self.session.findById("wnd[1]/tbar[0]/btn[8]").press()
        self.session.findById("wnd[0]/usr/ctxtSO_CPUDT-LOW").Text = self.context.entered_date_start
        self.session.findById("wnd[0]/usr/ctxtSO_CPUDT-HIGH").Text = self.context.entered_date_end
        self.session.findById("wnd[0]/usr/ctxtSO_BWART-LOW").Text = "101"
        self.session.findById("wnd[0]/usr/ctxtSO_BWART-HIGH").Text = "102"
        self.session.findById("wnd[0]/usr/btn%_SO_UNAME_%_APP_%-VALU_PUSH").press()
        self.session.findById("wnd[1]/tbar[0]/btn[24]").press()
        self.session.findById("wnd[1]/tbar[0]/btn[8]").press()
        self.session.findById("wnd[0]/usr/ctxtP_LAY01").Text = "/QUANTITY"
        self.session.findById("wnd[0]/tbar[1]/btn[8]").press()
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectedRows = "0"
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").contextMenu()
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectContextMenuItem("&XXL")
        self.session.findById("wnd[1]/usr/ssubSUB_CONFIGURATION:SAPLSALV_GUI_CUL_EXPORT_AS:0512/txtGS_EXPORT-FILE_NAME").Text = self.context.file_name
        self.session.findById("wnd[1]/tbar[0]/btn[20]").press()
        self.session.findById("wnd[1]/tbar[0]/btn[11]").press()


class GRN16Processor(GRNProcessor[GRN16Config]):
    def process(self):
        self.session.StartTransaction("ZLGRNS1")
        self.session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").Text = "VN01"
        self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-LOW").Text = self.context.entered_date_start
        self.session.findById("wnd[0]/usr/ctxtSO_BUDAT-HIGH").Text = self.context.entered_date_end
        self.session.findById("wnd[0]/usr/btn%_S_MBLNR_%_APP_%-VALU_PUSH").press()
        self.session.findById("wnd[1]/tbar[0]/btn[16]").press()
        self.session.findById("wnd[1]/tbar[0]/btn[24]").press()
        self.session.findById("wnd[1]/tbar[0]/btn[8]").press()
        self.session.findById("wnd[0]/usr/ctxtP_LAYOUT").Text = "/CUONG1"
        self.session.findById("wnd[0]/tbar[1]/btn[8]").press()
        self.session.findById("wnd[0]/usr/cntlCNTNR/shellcont/shell").pressToolbarContextButton("&MB_EXPORT")
        self.session.findById("wnd[0]/usr/cntlCNTNR/shellcont/shell").selectContextMenuItem("&XXL")
        self.session.findById("wnd[1]/usr/ssubSUB_CONFIGURATION:SAPLSALV_GUI_CUL_EXPORT_AS:0512/txtGS_EXPORT-FILE_NAME").Text = self.context.file_name
        self.session.findById("wnd[1]/tbar[0]/btn[20]").press()
        self.session.findById("wnd[1]/tbar[0]/btn[11]").press()