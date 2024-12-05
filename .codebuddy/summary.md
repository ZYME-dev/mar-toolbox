# Project Summary

## Overview
The project is designed to assist users in assembling a dossier for MPRA (MaPrimeRénov' - a French energy renovation aid program). It provides a web-based interface using Streamlit, allowing users to input various details related to their renovation projects, and generates a filled PDF form based on the provided data. The application also supports filling forms from Excel files and utilizes templates for generating documents.

## Languages, Frameworks, and Libraries Used
- **Languages**: Python
- **Frameworks**: Streamlit
- **Main Libraries**:
  - `pydantic`: For data validation and settings management.
  - `PyPDFForm`: For handling PDF forms.
  - `openpyxl`: For reading Excel files.
  - `python-calamine`: For reading Excel files.
  - `tablib`: For data handling and exporting.
  - `docxtpl`: For handling and generating Word documents.

## Purpose of the Project
The main purpose of this project is to facilitate the creation of a dossier required for applying for the MPRA program. Users can input their personal and project-related information, which is then used to fill out a PDF form. The application also allows for the import of data from Excel files to streamline the process.

## Build and Configuration Files
- **Configuration and Build Files**:
  - `/requirements.txt`: Contains the list of dependencies required for the project.

## Source Files Location
- The source files can be found in the root directory:
  - `/app.py`: Main application file for the Streamlit interface.
  - `/app2.py`: A secondary application file for handling URL fragments.
  - `/fill_from_excel.py`: Contains functionality for filling forms from Excel data.
  - `/models.py`: Contains data models using Pydantic.
  - `/test.py`: Contains test functions for PDF handling.
  
## Documentation Files Location
- The documentation file is located at:
  - `/README.md`: Provides an overview of the project and its purpose.

## Assets and Templates
- **Assets Directory**:
  - `/assets`: Contains Excel files and templates used in the project.
  - `/assets/templates`: Contains various PDF templates for generating documents.
  - `/assets/templates/blank`: Contains blank templates for various documents.
  - `/assets/templates/cccps`: Contains specific templates related to the CCCPS project. 

This summary encapsulates the essential components and structure of the project, providing a clear understanding of its functionality and organization.