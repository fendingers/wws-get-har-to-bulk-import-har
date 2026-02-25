"""
Converts XML to Excel for auditing.
"""

import pandas as pd
import xmltodict
from utils.logger import get_logger

logger = get_logger(__name__)

class XMLToExcel:
    def convert(self, xml_path):
        logger.info(f"Converting XML to Excel: {xml_path}")

        with open(xml_path, "r", encoding="utf-8") as f:
            data = xmltodict.parse(f.read())

        df = pd.json_normalize(data)
        excel_path = xml_path.replace(".xml", ".xlsx")
        df.to_excel(excel_path, index=False)

        return excel_path
