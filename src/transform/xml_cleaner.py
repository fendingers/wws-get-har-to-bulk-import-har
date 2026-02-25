"""
Optional cleanup utilities for XML:
- Remove empty nodes
- Normalize namespaces
"""

from lxml import etree

def remove_empty_elements(root):
    for elem in list(root):
        remove_empty_elements(elem)
        if (elem.text is None or not elem.text.strip()) and len(elem) == 0:
            root.remove(elem)
