from step.stage import ProcessDataStep


class CacheDataframeForReportDashboard:
        def __init__(self,process_step:ProcessDataStep):
            self.source_cache_data = process_step
            
            
        def _get_field_from_process_step(self):
            fields: dict = self.source_cache_data.__dict__
            for k,v in fields.items():
                setattr(self,k,v)
                