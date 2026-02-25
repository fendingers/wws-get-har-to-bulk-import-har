"""
Splits large XML files into smaller chunks based on:
- Repeating XML element (e.g., <Worker>)
- Maximum file size
"""

import os
from lxml import etree
from utils.logger import get_logger
from utils.file_utils import ensure_dir
from utils.xml_utils import get_settings
from .size_monitor import SizeMonitor

logger = get_logger(__name__)

class XMLSplitter:
    def __init__(self):
        self.settings = get_settings()
        self.split_element = self.settings["split_element"]
        self.max_size = self.settings["max_file_size_mb"] * 1024 * 1024

    def split(self):
        input_dir = self.settings["input_dir"]
        output_dir = self.settings["output_dir"]
        ensure_dir(output_dir)

        input_file = next(iter(os.listdir(input_dir)), None)
        if not input_file:
            raise FileNotFoundError("No XML file found in input directory")

        input_path = os.path.join(input_dir, input_file)
        logger.info(f"Splitting XML: {input_path}")

        context = etree.iterparse(input_path, events=("end",), tag=self.split_element)
        chunk_files = []
        monitor = SizeMonitor(self.max_size)

        chunk_index = 1
        chunk_path = os.path.join(output_dir, f"chunk_{chunk_index}.xml")
        chunk_files.append(chunk_path)
        chunk = open(chunk_path, "wb")

        for _, elem in context:
            xml_bytes = etree.tostring(elem)

            if monitor.would_exceed(xml_bytes):
                chunk.close()
                chunk_index += 1
                chunk_path = os.path.join(output_dir, f"chunk_{chunk_index}.xml")
                chunk_files.append(chunk_path)
                chunk = open(chunk_path, "wb")
                monitor.reset()

            chunk.write(xml_bytes)
            monitor.add(xml_bytes)

            elem.clear()

        chunk.close()
        logger.info(f"Created {len(chunk_files)} chunk files")
        return chunk_files
