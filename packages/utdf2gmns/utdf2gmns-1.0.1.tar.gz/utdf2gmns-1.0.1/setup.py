'''
##############################################################
# Created Date: Saturday, February 1st 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

import setuptools
with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    # if have requirements.txt file inside the folder
    with open("requirements.txt", "r", encoding="utf-8") as f:
        modules_needed = [i.strip() for i in f.readlines()]
except Exception:
    modules_needed = []

setuptools.setup(
    name="utdf2gmns",  # Replace with your own username
    version="1.0.1",
    author="Xiangyong Luo, Xuesong Simon Zhou",
    author_email="luoxiangyong01@gmail.com",
    description="Convert Synchro UTDF data format to other formats, such as GMNS, SUMO, etc...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyluo25/utdf2gmns",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=modules_needed,

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.xls', '*.xlsx', '*.csv'],
                  "test_data": ['*.xls']},
    project_urls={
        'Homepage': 'https://github.com/xyluo25/utdf2gmns',
        'Documentation': 'https://github.com/xyluo25/utdf2gmns',
        # 'Bug Tracker': '',
        # 'Source Code': '',
        # 'Download': '',
        # 'Publication': '',
        # 'Citation': '',
        # 'License': '',
        # 'Acknowledgement': '',
        # 'FAQs': '',
        # 'Contact': '',
    }
)
