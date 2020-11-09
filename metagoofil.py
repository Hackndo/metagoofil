import argparse
import os
import random
import sys
import time
import warnings

import downloader
import htmlExport
import processor
from discovery import googlesearch
from extractors import *

print("\n******************************************************")
print("*     /\/\   ___| |_ __ _  __ _  ___   ___  / _(_) | *")
print("*    /    \ / _ \ __/ _` |/ _` |/ _ \ / _ \| |_| | | *")
print("*   / /\/\ \  __/ || (_| | (_| | (_) | (_) |  _| | | *")
print("*   \/    \/\___|\__\__,_|\__, |\___/ \___/|_| |_|_| *")
print("*                         |___/                      *")
print("* Metagoofil Ver 0.0.1                               *")
print("* Original Author                                    *")
print("*    Christian Martorella                            *")
print("*    Edge-Security.com                               *")
print("*    cmartorella_at_edge-security.com                *")
print("* Fork author                                        *")
print("*    pixis                                           *")
print("*    https://hackndo.com                             *")
print("******************************************************")

version = "0.0.1"

def doprocess():
    all_results = []
    parser = argparse.ArgumentParser(
        prog="Metagoofil",
        description='Metagoofil v{} - Metadata harvester'.format(version)
    )

    parser.add_argument('domain', action='store', help='Domain to search')
    parser.add_argument('-t', '--types', action='store', default='pdf,doc,xls,ppt,docx,xlsx,pptx', help='Filetype to download (pdf,doc,xls,ppt,docx,xlsx,pptx)')
    parser.add_argument('--inurl', action='store_true', help='Set "inurl" filter instead of "site" filter on Google. Might find some false positives')
    parser.add_argument('-r', '--results-limit', type=int, action='store', default=200,
                            help='Limit of results to search (Default 200)')
    parser.add_argument('-s', '--results-start', type=int, action='store', default=0,
                        help='Offset to look for results (Default 0)')
    parser.add_argument('-l', '--local', action='store_true',
                            help='Local analysis of documents in working directory')
    parser.add_argument('-f', '--files-limit', type=int, action='store', default=5, help='Limit of files to download')
    parser.add_argument('-w', '--working-dir', action='store', default='.', help='Working directory')
    parser.add_argument('--html', action='store', default='output.html', help='Output HTML filename')
    parser.add_argument('--force', action='store_true', help='Force download even if files exists')
    parser.add_argument('--wait', action='store', type=int, default=1,
                        help='Time to wait between requests (Default: 1s)')
    parser.add_argument('--jitter', action='store', type=int, default=0,
                        help='Jitter to apply to wait between request (0 to 100, default: 0)')
    parser.add_argument('-V', '--version', action='store', help='Version')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    domain = args.domain
    filetypes = [t.strip() for t in args.types.split(',')]
    results_limit = args.results_limit
    files_limit = args.files_limit
    local_analysis = args.local
    working_directory = args.working_dir
    html_file = args.html

    failed_files = []
    emails = []

    if os.path.exists(working_directory):
        pass
    else:
        os.mkdir(working_directory)
    if not local_analysis:
        print("\n[-] Starting online search...")
        for filetype in filetypes:
            if filetype not in "pdf,doc,xls,ppt,docx,xlsx,pptx".split(","):
                print(f"Filetype {filetype} is not supported")
                continue

            print(f"\n[-] Searching for {filetype} files, with a results_limit of {results_limit}")
            search = googlesearch.search_google(
                domain,
                offset=args.results_start,
                results_limit=results_limit,
                filetype=filetype,
                inurl=args.inurl
            )
            search.process_files()
            files = search.get_files()
            if len(files) == 0:
                print("No file found.")
                continue
            print(f"Results: {len(files)} files found")
            print(f"Starting to download {files_limit} of them:")
            print("----------------------------------------\n")
            counter = 1
            for x in files:
                if counter <= files_limit:
                    print(f"[{counter}/{files_limit}] " + x)
                    getfile = downloader.downloader(x, working_directory, filetype)

                    if not getfile.down(wait=args.wait, jitter=args.jitter, force=args.force):
                        print("Download failed.")
                        continue

                    filename = getfile.name()
                    if filename != "":
                        if filetype == "pdf":
                            current_file = metadataPDF.metapdf(working_directory + "/" + filename)
                        elif filetype == "doc" or filetype == "ppt" or filetype == "xls":
                            current_file = metadataMSOffice.metaMs2k(working_directory + "/" + filename)
                            if os.name == "posix":
                                current_file = metadataExtractor.metaExtractor(working_directory + "/" + filename)
                        elif filetype == "docx" or filetype == "pptx" or filetype == "xlsx":
                            current_file = metadataMSOfficeXML.metaInfoMS(working_directory + "/" + filename)
                        else:
                            print("Unexpected error.")
                            continue
                        if current_file.getData():
                            raw = current_file.getRaw()
                            users = current_file.getUsers()
                            paths = current_file.getPaths()
                            soft = current_file.getSoftware()
                            email = []
                            if filetype == "pdf" or filetype == "docx":
                                if current_file.getTexts():
                                    email = current_file.getEmails()
                                    for em in email:
                                        emails.append(em)
                                else:
                                    email = []
                                    failed_files.append(x + ":" + str(res))
                            respack = [x, users, paths, soft, raw, email]
                            all_results.append(respack)
                        else:
                            failed_files.append(x + ":" + str(res))
                            print("\t [x] Error in the parsing process")  # A error in the parsing process
                    else:
                        pass
                counter += 1
    else:
        print("[-] Starting local analysis in directory " + working_directory)
        dirList = os.listdir(working_directory)
        for filename in dirList:
            print("[*] Analysis started for {}".format(filename))
            if filename != "":
                filetype = str(filename.split(".")[-1])
                if filetype == "pdf":
                    current_file = metadataPDF.metapdf(working_directory + "/" + filename)
                elif filetype == "doc" or filetype == "ppt" or filetype == "xls":
                    current_file = metadataMSOffice.metaMs2k(working_directory + "/" + filename)
                    if os.name == "posix":
                        current_file_extracted = metadataExtractor.metaExtractor(working_directory + "/" + filename)
                elif filetype == "docx" or filetype == "pptx" or filetype == "xlsx":
                    current_file = metadataMSOfficeXML.metaInfoMS(working_directory + "/" + filename)
                else:
                    print("[!] File extension {} not supported".format(filetype))
                    continue
                if current_file.getData():
                    raw = current_file.getRaw()
                    users = current_file.getUsers()
                    paths = current_file.getPaths()
                    soft = current_file.getSoftware()
                    if (filetype == "doc" or filetype == "xls" or filetype == "ppt") and os.name == "posix":
                        current_file_extracted.runExtract()
                        current_file_extracted.getData()
                        paths.extend(current_file_extracted.getPaths())
                        respack = [filename, users, paths, soft, raw, emails]
                        all_results.append(respack)

                    elif filetype == "docx" or filetype == "pdf" or filetype == "xlsx":
                        if current_file.getTexts():
                            email = current_file.getEmails()
                            for x in email:
                                emails.append(x)
                            all_results.append([filename, users, paths, soft, raw, emails])
                        else:
                            print("Error while extracting text")
                    else:
                        print("pass")
            else:
                pass
    proc = processor.Processor(all_results)
    userlist = proc.sort_users()
    softlist = proc.sort_software()
    pathlist = proc.sort_paths()

    try:
        html = htmlExport.htmlExport(userlist, softlist, pathlist, all_results, html_file, working_directory, failed_files,
                                     domain, emails)
        html.writehtml()
    except Exception as e:
        print(e)
        print("Error creating the file")
    print("\n[+] List of users found:")
    print("--------------------------")
    for x in userlist:
        print(x)
    print("\n[+] List of software found:")
    print("-----------------------------")
    for x in softlist:
        print(x)
    print("\n[+] List of paths and servers found:")
    print("---------------------------------------")
    for x in pathlist:
        print(x)
    print("\n[+] List of e-mails found:")
    print("----------------------------")
    for x in emails:
        print(x)
    # print("\n[+] List of errors:")
    # print("---------------------")
    # for x in failedfiles:
    #   print(x)


if __name__ == "__main__":
    doprocess()
