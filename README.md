This is where I will put the README. This program aims to take the output from the Workday Web Service Data Source for Get Historical Academic Records, reformat the XML, and split it into multiple Excel files that can be uploaded to the EIB with the Workday Web Service of Bulk Import Put Historical Academic Record.

"wws-get-har-to-bulk-import-har"/
│
├── README.md
├── pyproject.toml          # or requirements.txt
├── config/
│   ├── settings.yaml
│   └── logging.conf
│
├── data/
│   ├── input/
│   ├── output/
│   └── temp/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── splitting/
│   │   ├── __init__.py
│   │   ├── splitter.py
│   │   └── size_monitor.py
│   │
│   ├── transform/
│   │   ├── __init__.py
│   │   ├── xslt_transformer.py
│   │   └── xml_cleaner.py
│   │
│   ├── excel/
│   │   ├── __init__.py
│   │   ├── xml_to_excel.py
│   │   └── flatten.py
│   │
│   ├── utils/
│       ├── __init__.py
│       ├── file_utils.py
│       ├── xml_utils.py
│       └── logger.py
│
└── tests/
    ├── test_splitter.py
    ├── test_transformer.py
    └── test_excel.py

- Introduction:
- Use case:
- How to run:
- Dependencies:
- Architecture:

Sample:
# Workday XML Pipeline 
This project provides a maintainable Python pipeline for: 
- Splitting large Workday outbound XML files 
- Transforming XML using XSLT 
- Converting XML to Excel for auditing 
## Structure See `src/` for all processing modules: 
- `splitting/` handles XML chunking 
- `transform/` handles XSLT and cleanup 
- `excel/` handles XML → Excel conversion 
- `utils/` contains shared helpers ## Running Run the