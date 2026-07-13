from utils.data_utils import DataIngestor
from utils.excel_manager import WorkBookManager
from core.data_processor import DataProcessBase, DataProcessVerify, DataProcessGrn10Number, DataVerifyProcessForReportDashboard,DataReceiptsProcessForReportDashboard,DataProcessGrn16Number
from utils.config_loader import DailyConfig, VerifyConfig, GRN10Config, GRN16Config, create_profile, Profile
from getpass import getuser
import sys
from core.sap_connector import SapConnector, GRN10Processor, GRN16Processor


class ConfigComponent:
    def __init__(self):
        self.profile: Profile = create_profile()
        self.daily_report_config: DailyConfig = self.profile.daily_report_config
        self.verify_config: VerifyConfig = self.profile.daily_report_config.verify_config
        self.grn10_config: GRN10Config = self.profile.daily_report_config.grn_10_numbers_config
        self.grn16_config: GRN16Config = self.profile.daily_report_config.grn_16_numbers_config


class SapProcessComponent:
    def __init__(self, config: ConfigComponent):
        if not config.daily_report_config.run_sap:
            return

        self.sap: SapConnector = SapConnector()
        self.session = self.sap.session
        self.sap_grn10: GRN10Processor = GRN10Processor(config.grn10_config, self.session)
        self.sap_grn16: GRN16Processor = GRN16Processor(config.grn16_config, self.session)


class UtilsComponent:
    def __init__(self, config_component: ConfigComponent):
        self.verify_data_ingestor: DataIngestor = DataIngestor(config_component.verify_config.path_local_mapping)
        self.grn10_data_ingestor: DataIngestor = DataIngestor(None, True)
        self.grn16_data_ingestor: DataIngestor = DataIngestor(None, True)


class CoreComponent:
    def __init__(self, config_component: ConfigComponent):
        self.data_process_verify: DataProcessBase = DataProcessVerify(config_component.verify_config)
        self.data_process_grn10: DataProcessBase = DataProcessGrn10Number(config_component.grn10_config)
        self.data_process_grn16: DataProcessBase = DataProcessGrn16Number(config_component.grn16_config)
        
        self.cache_verify_process : DataProcessBase = DataVerifyProcessForReportDashboard(None)
        
        self.cache_receipt_process : DataProcessBase = DataReceiptsProcessForReportDashboard(None)

class CombaineComponent:
    def __init__(self):
        self.config = None
        self.sap = None
        self.uls = None
        self.core = None

    def combaine(self) -> None:
        self.config = ConfigComponent()

        if self.config.daily_report_config.run_sap:
            self.sap = SapProcessComponent(self.config)

        self.uls = UtilsComponent(self.config)
        self.core = CoreComponent(self.config)