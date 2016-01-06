### About 
The toolset leverages the Hitachi HiCommand CLI or API interface, collects information from the desired storage arrays in XML, processes the information (using another project of mine, xmldataset), stores all of the information in an in memory database (SQLlite), actions the desired reports and sends the results to the desired output filter (includes screen, html email and text email).

### Configuration
All configuration is within the hds_storage_compliance_tool.config file.

### Customisation of reports and output
Where desired, custom/additional reports can be made through the implementation of SQLalchemy based queries, see storageninja/reports/hds_cs.py for examples. 

If a specific output is required, the examples in storageninja/outputs can be used as a reference.  

### Supporting the project
I welcome all manner of enhancements to the project, please feel free to send me pull requests or contact via github

### Installation
Tested on Python 3.5.0, build a corresponding virtual environment and install the requirements listed in requirements.txt ( pip -r install requirements.txt )

### Execution
Configure hds_storage_compliance_tool.config and run hds_storage_compliance_tool.py

### Authors and Contributors
Developed by James Spurin (@spurin).

### Support or Contact
Where possible I will always do my best to help with support, drop me a message or raise an issue via github





HDS Storage Compliance Tool - James Spurin
===================
The HDS Storage Compliance Tool is a Python utility for ensuring that Hitachi based storage environments conform to desired standards.  

The toolset leverages the Hitachi HiCommand CLI or API interface, collects information from the desired storage arrays in XML, processes the information (using another project of mine, xmldataset), stores all of the information in an in memory database (SQLlite), actions the desired reports and sends the results to the desired output filter (includes screen, html email and text email).

All configuration is within the hds_storage_compliance_tool.config file.

Where desired, custom/additional reports can be made through the implementation of SQLalchemy based queries, see storageninja/reports/hds_cs.py for examples. 

If a specific output is required, the examples in storageninja/outputs can be used as a reference.

( Pull requests welcome )

----------

Installation
-------------

Tested on Python 3.5.0, build a corresponding virtual environment and install the requirements listed in requirements.txt ( pip -r install requirements.txt )

Execution
-------------

Configure hds_storage_compliance_tool.config
