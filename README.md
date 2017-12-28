# mispAttributeTransform

This script use pymisp module to export attributes from Misp based on specific criteria. Its main reason is to export attribute and forward them for monitoring such as Elastic Search, Splunk or other SIEM.


### Features
* Export Misp attributes based on a specific type (ip, domain, email, other type are coming)
* Only export attributes which have a specific tag (send:siem for instance)
* Export only the attributes which has been updated in the last X days

### Help
python mispExport.py -h
```
usage: mispExport.py [-h] -c CATEGORY -d DATERANGE [-s]

Get all the events matching a category and date range

optional arguments:
  -h, --help            show this help message and exit
  -c CATEGORY, --category CATEGORY
                        Parameter to search (ip, email, domain, etc.)
  -d DATERANGE, --daterange DATERANGE
                        Only get the last X days updated attributes (5, 10, etc.)
  -s, --siem            Get only events with tag siem - Default: None
```

### Installation
* Create a repository named "private"
* Modify the file "keys.py" with your Misp instance details
* Move this file to your private directory
