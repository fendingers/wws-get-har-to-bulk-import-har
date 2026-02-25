"""
Applies XSLT transformations to XML chunks.
"""

from lxml import etree
from utils.xml_utils import get_settings
from utils.logger import get_logger
import os

logger = get_logger(__name__)

class XSLTTransformer:
    def __init__(self):
        self.settings = get_settings()
        self.xslt_path = self.settings["xslt_path"]

        xslt_doc = etree.parse(self.xslt_path)
        self.transform = etree.XSLT(xslt_doc)

    def apply_xslt(self, xml_path):
        logger.info(f"Transforming {xml_path}")

        doc = etree.parse(xml_path)
        result = self.transform(doc)

        out_path = xml_path.replace(".xml", "_transformed.xml")
        result.write(out_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        return out_path
