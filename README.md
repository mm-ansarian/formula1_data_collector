## Introduction
This repository contains several Python modules for collecting various types of information about Formula 1.
The project's main purpose is to gather Python scripts that can retrieve most of the important information about Formula 1. 
These scripts can be reused in larger projects. We also plan to convert this repository into a Python package that will be available to everyone.

## How to run
This repository is code-based; we do not provide a GUI.
This repository is intended for developers and programmers (not typical end users).
Each filename indicates its purpose. Browse the filenames, find the script that collects the information you need, and run it.
We plan to create a main module that ties these scripts together so you can access all information by running a single file (which is more convenient).
You can follow these steps to run the modules:

1. Install `python3` on your system.

2. Clone the project repository using `git`:

    ```git clone git@github.com:mm-ansarian/formula1_data_collector.git```

    or 

    ```git clone https://github.com/mm-ansarian/formula1_data_collector.git```

3. Open the project folder.

4. Install the required packages into a virtual environment (recommended) or system-wide:

    ```python -m pip install -r requirements.txt```

5. Find the script that collects the information you need and run it.

## Details
- Programming language: Python
- API: [Jolpica F1](https://github.com/jolpica/jolpica-f1)

## TODO
- [ ] Cover all important F1 data.
- [ ] Making description for each part of the scripts.
- [ ] Create the main module.
- [ ] Create an official python library based on this repository.
