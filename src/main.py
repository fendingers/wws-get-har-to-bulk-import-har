"""
Main pipeline orchestrator.
"""

from splitting.splitter import XMLSplitter
from transform.xslt_transformer import XSLTTransformer
from excel.xml_to_excel import XMLToExcel
from utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    logger.info("Starting Workday XML pipeline")

    # 1. Split XML
    splitter = XMLSplitter()
    chunk_files = splitter.split()

    # 2. Transform each chunk
    transformer = XSLTTransformer()
    transformed_files = [transformer.apply_xslt(f) for f in chunk_files]

    # 3. Convert to Excel (optional)
    converter = XMLToExcel()
    for f in transformed_files:
        converter.convert(f)

    logger.info("Pipeline complete")

if __name__ == "__main__":
    run_pipeline()
