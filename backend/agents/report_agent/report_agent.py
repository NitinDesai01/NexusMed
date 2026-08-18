import logging

logger = logging.getLogger(__name__)

class ReportAgent:
    def __init__(self):
        pass
        
    def process_report(self, file, user_id):
        return {"message": "Report processed", "report_id": 1, "summary": "Analysis complete"}
