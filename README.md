# Metagoofil - Python3+

## Original Author

Coded by Christian Martorella 

www.edge-security.com

cmartorella@edge-security.com

## What is it?

Metagoofil is a tool for extracting metadata of public documents (pdf,doc,xls,ppt,etc) availables in the target websites.This information could be useful because you can get valid usernames, people names, for using later in bruteforce password attacks (vpn, ftp, webapps), the tool will also extracts interesting "paths" of the documents, where we can get shared resources names, server names, etc.

This new version will also extract emails addresses from PDF and Word documents content.

## How it works

The tool first perform a query in Google requesting different filetypes that can have useful metadata (pdf, doc, xls,ppt,etc), then will download those documents to the disk and extracts the metadata of the file using specific libraries for parsing different file types (Hachoir, Pdfminer, etc)

## Example

```
# Simple use
python metagoofil.py -w /tmp/mydomain my.domain.com

# Detection only (no download)
python metagoofil.py -w /tmp/mydomain -f 0 my.domain.com 

# Stealth
python metagoofil.py -w /tmp/mydomain --results-limit 20 --results-start 0 --files-limit 10 --wait 15 --jitter 30 -t doc,docx,xls,xlsx,pdf my.domain.com

# Local analysis
python metagoofil.py -w /tmp/mydomain -l LOCAL
```
